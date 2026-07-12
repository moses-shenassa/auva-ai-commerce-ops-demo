from __future__ import annotations

import argparse

from .workflow import evaluate_cases, load_cases


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the AUVA public-safe demo.")
    parser.add_argument("--case", required=True, help="Path to JSONL synthetic cases.")
    args = parser.parse_args()

    for decision in evaluate_cases(load_cases(args.case)):
        print(f"Case: {decision.case_id}")
        print(f"Intent: {decision.intent}")
        print(f"Action: {decision.action}")
        print(f"Approval: {decision.approval}")
        print(f"Confidence: {decision.confidence:.2f}")
        if decision.risk_flags:
            print(f"Risk flags: {', '.join(decision.risk_flags)}")
        print("\nOperator note:")
        print(decision.operator_note)
        print("\nReply draft:")
        print(decision.reply_draft)
        print("-" * 72)


if __name__ == "__main__":
    main()
