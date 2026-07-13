from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass

from .models import ClassificationSource, ContextBundle, Intent


ALLOWED_INTENTS: tuple[Intent, ...] = (
    "tracking_delay",
    "change_shipping_address",
    "refund_request",
    "product_question",
    "damaged_item",
    "unknown",
)


@dataclass(frozen=True)
class IntentClassification:
    intent: Intent
    confidence: float
    source: ClassificationSource
    rationale: str


def classify_intent_with_openai(
    message: str,
    context: ContextBundle,
    *,
    api_key: str | None = None,
    model: str | None = None,
) -> IntentClassification | None:
    """Classify support intent with a live LLM when credentials are available.

    The demo intentionally uses the standard library instead of an SDK so the
    repository stays interview-runnable without dependency installation.
    """

    mode = os.getenv("AUVA_AI_MODE", "auto").lower()
    if mode in {"offline", "rules", "disabled"}:
        return None

    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        return None

    selected_model = model or os.getenv("AUVA_OPENAI_MODEL", "gpt-4o-mini")
    payload = {
        "model": selected_model,
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [
            {
                "role": "system",
                "content": (
                    "You classify public-safe ecommerce support cases. "
                    "Return only JSON with keys intent, confidence, and rationale. "
                    f"intent must be one of: {', '.join(ALLOWED_INTENTS)}. "
                    "Use unknown when the message does not clearly match."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "customer_message": message,
                        "order_context": {
                            "order_status": context.case.order_status,
                            "payment_status": context.case.payment_status,
                            "fulfillment_status": context.case.fulfillment_status,
                            "carrier_status": context.case.carrier_status,
                            "days_since_fulfillment": context.case.days_since_fulfillment,
                            "customer_tier": context.case.customer_tier,
                            "product_type": context.case.product_type,
                            "policy_hint": context.case.policy_hint,
                        },
                        "risk_flags": context.risk_flags,
                        "supporting_facts": context.supporting_facts,
                    },
                    sort_keys=True,
                ),
            },
        ],
    }

    request = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            response_payload = json.loads(response.read().decode("utf-8"))
    except (OSError, urllib.error.HTTPError, json.JSONDecodeError):
        return None

    try:
        content = response_payload["choices"][0]["message"]["content"]
        raw = json.loads(content)
    except (KeyError, IndexError, TypeError, json.JSONDecodeError):
        return None

    intent = raw.get("intent")
    if intent not in ALLOWED_INTENTS:
        return None

    confidence = _clamp_confidence(raw.get("confidence"))
    rationale = str(raw.get("rationale", "No model rationale returned."))[:300]
    return IntentClassification(
        intent=intent,
        confidence=confidence,
        source="openai",
        rationale=rationale,
    )


def _clamp_confidence(value: object) -> float:
    try:
        confidence = float(value)
    except (TypeError, ValueError):
        return 0.7
    return round(max(0.0, min(confidence, 1.0)), 2)
