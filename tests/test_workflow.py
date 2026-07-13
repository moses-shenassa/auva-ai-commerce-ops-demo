import unittest
from unittest.mock import patch

from auva_demo.ai import IntentClassification
from auva_demo.models import Case
from auva_demo.workflow import evaluate_case, load_cases
from scripts.evaluate_demo import score


class WorkflowTests(unittest.TestCase):
    def test_loads_synthetic_cases(self):
        cases = load_cases("data/synthetic_cases.jsonl")
        self.assertEqual(len(cases), 5)
        self.assertEqual(cases[0].case_id, "delayed-delivery-001")
        self.assertEqual(cases[0].expected_action, "tracking_investigation")

    def test_synthetic_scorecard_is_green(self):
        cases = load_cases("data/synthetic_cases.jsonl")
        scorecard = score(cases, [evaluate_case(case) for case in cases])
        self.assertEqual(scorecard.intent_hits, 5)
        self.assertEqual(scorecard.action_hits, 5)
        self.assertEqual(scorecard.approval_hits, 5)

    def test_delayed_delivery_routes_to_tracking_investigation(self):
        case = Case(
            case_id="x",
            message="Where is my order? Tracking is delayed.",
            order_status="open",
            payment_status="paid",
            fulfillment_status="fulfilled",
            carrier_status="in_transit_delayed",
            days_since_fulfillment=9,
            customer_tier="returning",
            product_type="physical_goods",
            policy_hint="standard",
        )
        decision = evaluate_case(case)
        self.assertEqual(decision.intent, "tracking_delay")
        self.assertEqual(decision.action, "tracking_investigation")
        self.assertEqual(decision.approval, "review_required")
        self.assertIn("shipment_delay_over_threshold", decision.risk_flags)

    def test_address_change_after_fulfillment_requires_review(self):
        case = Case(
            case_id="x",
            message="Please change my shipping address.",
            order_status="open",
            payment_status="paid",
            fulfillment_status="fulfilled",
            carrier_status="label_created",
            days_since_fulfillment=1,
            customer_tier="new",
            product_type="physical_goods",
            policy_hint="standard",
        )
        decision = evaluate_case(case)
        self.assertEqual(decision.intent, "change_shipping_address")
        self.assertEqual(decision.action, "escalate_review")
        self.assertEqual(decision.approval, "review_required")
        self.assertIn("address_change_after_fulfillment", decision.risk_flags)

    def test_refund_request_never_auto_sends(self):
        case = Case(
            case_id="x",
            message="I want a refund.",
            order_status="open",
            payment_status="paid",
            fulfillment_status="fulfilled",
            carrier_status="delivered",
            days_since_fulfillment=4,
            customer_tier="new",
            product_type="physical_goods",
            policy_hint="strict_review",
        )
        decision = evaluate_case(case)
        self.assertEqual(decision.intent, "refund_request")
        self.assertEqual(decision.action, "refund_review")
        self.assertEqual(decision.approval, "manager_review")

    def test_product_question_can_be_auto_draft(self):
        case = Case(
            case_id="x",
            message="How do I care for this item?",
            order_status="closed",
            payment_status="paid",
            fulfillment_status="fulfilled",
            carrier_status="delivered",
            days_since_fulfillment=6,
            customer_tier="vip",
            product_type="physical_goods",
            policy_hint="standard",
        )
        decision = evaluate_case(case)
        self.assertEqual(decision.intent, "product_question")
        self.assertEqual(decision.action, "draft_reply")
        self.assertEqual(decision.approval, "auto_draft")

    def test_live_ai_classifier_can_drive_intent_inside_policy_guardrails(self):
        case = Case(
            case_id="x",
            message="This arrived shattered in the box.",
            order_status="open",
            payment_status="paid",
            fulfillment_status="fulfilled",
            carrier_status="delivered",
            days_since_fulfillment=2,
            customer_tier="new",
            product_type="physical_goods",
            policy_hint="standard",
        )

        with patch(
            "auva_demo.workflow.classify_intent_with_openai",
            return_value=IntentClassification(
                intent="damaged_item",
                confidence=0.91,
                source="openai",
                rationale="Customer reports breakage on arrival.",
            ),
        ):
            decision = evaluate_case(case)

        self.assertEqual(decision.intent, "damaged_item")
        self.assertEqual(decision.action, "replace_item")
        self.assertEqual(decision.approval, "review_required")
        self.assertEqual(decision.confidence, 0.91)
        self.assertEqual(decision.classification_source, "openai")

    def test_offline_fallback_remains_available_without_ai(self):
        case = Case(
            case_id="x",
            message="I want a refund.",
            order_status="open",
            payment_status="paid",
            fulfillment_status="fulfilled",
            carrier_status="delivered",
            days_since_fulfillment=4,
            customer_tier="new",
            product_type="physical_goods",
            policy_hint="standard",
        )

        with patch("auva_demo.workflow.classify_intent_with_openai", return_value=None):
            decision = evaluate_case(case)

        self.assertEqual(decision.intent, "refund_request")
        self.assertEqual(decision.action, "refund_review")
        self.assertEqual(decision.classification_source, "offline_rules")


if __name__ == "__main__":
    unittest.main()
