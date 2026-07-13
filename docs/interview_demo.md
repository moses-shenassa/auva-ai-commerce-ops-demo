# Interview Demo Guide

This is the short version to use when sharing AUVA in a live interview.

## One-Minute Framing

AUVA is a public-safe version of a commerce operations assistant. The demo is intentionally narrow: post-purchase support triage for delayed shipments, address changes, refunds, damaged items, and low-risk product questions.

The important product pattern is not "AI writes emails." It is a supervised operating loop:

```text
message -> context bundle -> intent -> policy/risk -> action -> approval
```

That pattern matters because support operations touch money, fulfillment, customer trust, and policy exceptions. The system should help an operator move faster without pretending every generated answer is safe to send.

## Run It Live

```bash
python3 scripts/interview_demo.py
```

Optional deeper checks:

```bash
python3 -m auva_demo.cli --case data/synthetic_cases.jsonl
python3 scripts/evaluate_demo.py --case data/synthetic_cases.jsonl
python3 -m unittest discover -s tests
```

## What To Point Out

- The demo runs locally with no API keys, databases, network calls, or private data.
- The workflow separates recommendation from external action.
- Risk flags push delayed shipments, refunds, replacements, and post-fulfillment address changes into human review.
- The synthetic evaluation file contains expected behavior, not just input samples.
- GitHub Actions runs tests, the CLI demo, the interview demo, and the evaluation scoreboard on push.

## Strong Interview Language

Use this phrasing:

> I built this as a public-safe demo of the implementation pattern behind AUVA. The private system worked with real commerce context, but this repo uses synthetic data so I can show the workflow without exposing customer records. What I want to show here is the operating discipline: context assembly, policy-aware routing, human approval, repeatable tests, and CI.

## Avoid Overclaiming

Do not call this a production app by itself. It is a runnable portfolio demo that preserves the product pattern and safety posture of the larger AUVA work.
