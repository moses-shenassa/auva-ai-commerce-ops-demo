from __future__ import annotations

from .models import Action, Approval, ContextBundle, Intent


def classify_intent(message: str) -> Intent:
    text = message.lower()
    if "broken" in text or "damaged" in text:
        return "damaged_item"
    if any(term in text for term in ("how do i", "instructions", "use this", "care")):
        return "product_question"
    if "address" in text or "ship to" in text:
        return "change_shipping_address"
    if "refund" in text or "money back" in text:
        return "refund_request"
    if any(term in text for term in ("tracking", "where is", "late", "delayed", "not moved")):
        return "tracking_delay"
    return "unknown"


def choose_action(intent: Intent, context: ContextBundle) -> Action:
    flags = set(context.risk_flags)
    case = context.case

    if intent == "tracking_delay":
        return "tracking_investigation"
    if intent == "change_shipping_address":
        return "escalate_review" if "address_change_after_fulfillment" in flags else "draft_reply"
    if intent == "refund_request":
        return "refund_review"
    if intent == "damaged_item":
        return "replace_item" if case.payment_status == "paid" else "escalate_review"
    if intent == "product_question":
        return "draft_reply"
    return "escalate_review"


def approval_tier(action: Action, context: ContextBundle) -> Approval:
    flags = set(context.risk_flags)
    if "merchant_policy_requires_review" in flags:
        return "manager_review"
    if action in {"refund_review", "replace_item", "escalate_review"}:
        return "review_required"
    if flags:
        return "review_required"
    return "auto_draft"


def confidence_score(intent: Intent, context: ContextBundle) -> float:
    if intent == "unknown":
        return 0.42
    score = 0.78
    if context.case.payment_status == "paid":
        score += 0.04
    if context.case.fulfillment_status in {"fulfilled", "unfulfilled"}:
        score += 0.03
    if context.risk_flags:
        score -= min(0.12, len(context.risk_flags) * 0.04)
    return round(max(0.35, min(score, 0.93)), 2)
