from __future__ import annotations

from .models import Case, ContextBundle


def build_context(case: Case) -> ContextBundle:
    """Build a small evidence bundle from synthetic commerce facts."""
    facts = [
        f"payment_status={case.payment_status}",
        f"fulfillment_status={case.fulfillment_status}",
        f"carrier_status={case.carrier_status}",
        f"days_since_fulfillment={case.days_since_fulfillment}",
        f"customer_tier={case.customer_tier}",
        f"product_type={case.product_type}",
    ]
    risk_flags: list[str] = []

    if case.payment_status != "paid":
        risk_flags.append("payment_not_confirmed")
    if case.carrier_status == "in_transit_delayed" or case.days_since_fulfillment >= 8:
        risk_flags.append("shipment_delay_over_threshold")
    if "address" in case.message.lower() and case.fulfillment_status == "fulfilled":
        risk_flags.append("address_change_after_fulfillment")
    if "refund" in case.message.lower():
        risk_flags.append("refund_requested")
    if "broken" in case.message.lower() or "damaged" in case.message.lower():
        risk_flags.append("possible_damaged_item")
    if case.policy_hint == "strict_review":
        risk_flags.append("merchant_policy_requires_review")

    return ContextBundle(
        case=case,
        risk_flags=tuple(risk_flags),
        supporting_facts=tuple(facts),
    )
