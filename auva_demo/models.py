from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


Intent = Literal[
    "tracking_delay",
    "change_shipping_address",
    "refund_request",
    "product_question",
    "damaged_item",
    "unknown",
]

Action = Literal[
    "tracking_investigation",
    "escalate_review",
    "draft_reply",
    "replace_item",
    "refund_review",
]

Approval = Literal["auto_draft", "review_required", "manager_review"]


@dataclass(frozen=True)
class Case:
    case_id: str
    message: str
    order_status: str
    payment_status: str
    fulfillment_status: str
    carrier_status: str
    days_since_fulfillment: int
    customer_tier: str
    product_type: str
    policy_hint: str
    expected_intent: Intent | None = None
    expected_action: Action | None = None
    expected_approval: Approval | None = None


@dataclass(frozen=True)
class ContextBundle:
    case: Case
    risk_flags: tuple[str, ...]
    supporting_facts: tuple[str, ...]


@dataclass(frozen=True)
class Decision:
    case_id: str
    intent: Intent
    action: Action
    approval: Approval
    confidence: float
    operator_note: str
    reply_draft: str
    risk_flags: tuple[str, ...]
