from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from auva_demo.models import Case, Decision
from auva_demo.workflow import evaluate_cases, load_cases


@dataclass(frozen=True)
class Scorecard:
    cases: int
    intent_hits: int
    action_hits: int
    approval_hits: int

    @property
    def all_fields(self) -> int:
        return self.cases * 3

    @property
    def field_hits(self) -> int:
        return self.intent_hits + self.action_hits + self.approval_hits

    @property
    def accuracy(self) -> float:
        return self.field_hits / self.all_fields if self.all_fields else 0.0


def score(cases: list[Case], decisions: list[Decision]) -> Scorecard:
    if len(cases) != len(decisions):
        raise ValueError("Case and decision counts do not match.")

    intent_hits = 0
    action_hits = 0
    approval_hits = 0

    for case, decision in zip(cases, decisions, strict=True):
        intent_hits += decision.intent == case.expected_intent
        action_hits += decision.action == case.expected_action
        approval_hits += decision.approval == case.expected_approval

    return Scorecard(
        cases=len(cases),
        intent_hits=intent_hits,
        action_hits=action_hits,
        approval_hits=approval_hits,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run AUVA synthetic evaluation scoreboard.")
    parser.add_argument("--case", required=True, help="Path to JSONL synthetic cases.")
    args = parser.parse_args()

    cases = load_cases(args.case)
    decisions = evaluate_cases(cases)
    scorecard = score(cases, decisions)

    print("AUVA synthetic evaluation")
    print(f"Cases: {scorecard.cases}")
    print(f"Intent accuracy: {scorecard.intent_hits}/{scorecard.cases}")
    print(f"Action accuracy: {scorecard.action_hits}/{scorecard.cases}")
    print(f"Approval accuracy: {scorecard.approval_hits}/{scorecard.cases}")
    print(f"Overall field accuracy: {scorecard.accuracy:.0%}")

    if scorecard.field_hits != scorecard.all_fields:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
