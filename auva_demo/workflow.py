from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .ai import IntentClassification, classify_intent_with_openai
from .context import build_context
from .models import Case, ContextBundle, Decision
from .routing import approval_tier, choose_action, classify_intent, confidence_score


def load_cases(path: str | Path) -> list[Case]:
    cases: list[Case] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            cases.append(Case(**json.loads(line)))
    return cases


def evaluate_case(case: Case) -> Decision:
    context = build_context(case)
    classification = _classify_case(case, context)
    intent = classification.intent
    action = choose_action(intent, context)
    approval = approval_tier(action, context)
    return Decision(
        case_id=case.case_id,
        intent=intent,
        action=action,
        approval=approval,
        confidence=classification.confidence,
        classification_source=classification.source,
        operator_note=_operator_note(case, intent, action, approval),
        reply_draft=_reply_draft(case, intent, action, approval),
        risk_flags=context.risk_flags,
    )


def evaluate_cases(cases: Iterable[Case]) -> list[Decision]:
    return [evaluate_case(case) for case in cases]


def _classify_case(case: Case, context: ContextBundle) -> IntentClassification:
    ai_classification = classify_intent_with_openai(case.message, context)
    if ai_classification is not None:
        return ai_classification

    intent = classify_intent(case.message)
    return IntentClassification(
        intent=intent,
        confidence=confidence_score(intent, context),
        source="offline_rules",
        rationale="Offline fallback classifier used because no live AI classification was available.",
    )


def _operator_note(case: Case, intent: str, action: str, approval: str) -> str:
    if action == "tracking_investigation":
        return (
            "Customer is asking about a delayed paid order. Order is in transit and "
            "beyond the expected delivery window. Recommend checking tracking, "
            "acknowledging the delay, and offering follow-up if the carrier status does not move."
        )
    if action == "refund_review":
        return (
            "Customer is asking for a refund. Refunds affect money movement, so AUVA "
            "prepares the context but routes the decision for human review."
        )
    if action == "replace_item":
        return (
            "Customer reports a damaged item on a paid order. Recommend replacement review "
            "with photo/context check before sending a remedy."
        )
    if action == "draft_reply":
        return (
            "Low-risk support question. AUVA can draft a helpful response while preserving "
            "operator review before any external send."
        )
    return (
        f"Intent classified as {intent}. Recommended action {action} requires {approval} "
        "because the request has operational or policy risk."
    )


def _reply_draft(case: Case, intent: str, action: str, approval: str) -> str:
    if action == "tracking_investigation":
        return (
            "Thanks for checking in. I see your order is in transit, but it looks like it "
            "has taken longer than expected. I am going to check the carrier status and "
            "follow up with the next best step."
        )
    if action == "refund_review":
        return (
            "Thanks for reaching out. I am going to review the order and policy details "
            "before confirming the best next step on the refund request."
        )
    if action == "replace_item":
        return (
            "I am sorry it arrived damaged. Please send a quick photo of the item and "
            "packaging so we can review the best replacement path."
        )
    if intent == "product_question":
        return (
            "Happy to help. Here are the basic care and use notes for this item. If anything "
            "still feels unclear, send a quick follow-up and I will walk you through it."
        )
    return (
        "Thanks for the note. I am going to review the order details and follow up with "
        "the safest next step."
    )
