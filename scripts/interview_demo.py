from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from auva_demo.workflow import evaluate_cases, load_cases
from scripts.evaluate_demo import score


CASE_PATH = Path("data/synthetic_cases.jsonl")


def main() -> None:
    cases = load_cases(CASE_PATH)
    decisions = evaluate_cases(cases)
    scorecard = score(cases, decisions)

    print("AUVA interview demo")
    print("=" * 72)
    print("A public-safe commerce support workflow:")
    print("message -> context bundle -> intent -> policy/risk -> action -> approval")
    print()

    for decision in decisions[:2]:
        print(f"Case: {decision.case_id}")
        print(f"Intent: {decision.intent}")
        print(f"Action: {decision.action}")
        print(f"Approval: {decision.approval}")
        print(f"Confidence: {decision.confidence:.2f}")
        print(f"Classifier: {decision.classification_source}")
        if decision.risk_flags:
            print(f"Risk flags: {', '.join(decision.risk_flags)}")
        print(f"Operator note: {decision.operator_note}")
        print("-" * 72)

    print("Evaluation gate")
    print(f"Cases: {scorecard.cases}")
    print(f"Intent accuracy: {scorecard.intent_hits}/{scorecard.cases}")
    print(f"Action accuracy: {scorecard.action_hits}/{scorecard.cases}")
    print(f"Approval accuracy: {scorecard.approval_hits}/{scorecard.cases}")
    print(f"Overall field accuracy: {scorecard.accuracy:.0%}")
    print()
    print("Safety boundary: synthetic data only; no customer records, no credentials, no external sends.")

    if scorecard.field_hits != scorecard.all_fields:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
