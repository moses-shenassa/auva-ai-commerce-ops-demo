# AUVA AI Commerce Ops Demo

[![CI](https://github.com/moses-shenassa/auva-ai-commerce-ops-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/moses-shenassa/auva-ai-commerce-ops-demo/actions/workflows/ci.yml)

AUVA is a public-safe portfolio demo for an AI-assisted commerce operations assistant.

This repository is not the private production workspace. It is a sanitized demo that shows the product architecture and implementation style behind AUVA without exposing customer records, merchant data, credentials, private databases, or internal operating artifacts.

## At A Glance

- **Domain:** e-commerce support operations, fulfillment, refunds, customer trust
- **Pattern:** context bundle -> intent classification -> policy/risk check -> action recommendation -> human approval
- **Proof:** synthetic evaluation scoreboard, unit tests, CLI demo, GitHub Actions CI
- **Safety stance:** no live data, no external sends, no secrets, no customer records
- **Built for:** AI implementation, AI enablement, product operations, support operations, business systems, and workflow automation roles

## What AUVA Demonstrates

AUVA models a merchant-facing AI operations layer for commerce teams. The demo focuses on a narrow but realistic wedge:

- assemble support context from synthetic customer, order, product, and policy data
- classify support intent
- choose a safe business action
- assign a human-review approval tier
- produce a short operator-facing recommendation and customer reply draft

The key idea is not "AI writes emails." The key idea is a supervised operating loop that sees commerce truth, sees conversations, remembers policy, and helps a human operator move work safely.

This version uses deterministic Python logic so the repo can run anywhere without API keys. In production, the same boundary would support LLM-assisted context interpretation and drafting behind the same approval and evaluation gates.

## Why This Exists

This repo is designed as a portfolio artifact for AI enablement, business systems, support operations, product operations, and applied AI roles. It shows:

- business workflow modeling
- human-in-the-loop AI patterns
- context-bundle design
- guardrail and approval thinking
- synthetic evaluation data
- CI/CD readiness through GitHub Actions
- clear product documentation

## Demo Flow

```text
Synthetic support case
  -> context bundle
  -> intent classification
  -> policy and risk check
  -> recommended action
  -> approval tier
  -> operator summary + reply draft
```

## Quick Start

```bash
python3 scripts/interview_demo.py
python3 -m auva_demo.cli --case data/synthetic_cases.jsonl
python3 scripts/evaluate_demo.py --case data/synthetic_cases.jsonl
python3 -m unittest discover -s tests
```

No network access, API keys, databases, or external services are required.

For a live interview, start with:

```bash
make demo
```

Then point to `docs/interview_demo.md` for the short talk track.

## Example Output

```text
Case: delayed-delivery-001
Intent: tracking_delay
Action: tracking_investigation
Approval: review_required
Confidence: 0.81

Operator note:
Customer is asking about a delayed paid order. Order is in transit and beyond the expected delivery window. Recommend checking tracking, acknowledging the delay, and offering follow-up if the carrier status does not move.
```

## Evaluation Output

```text
AUVA synthetic evaluation
Cases: 5
Intent accuracy: 5/5
Action accuracy: 5/5
Approval accuracy: 5/5
Overall field accuracy: 100%
```

The point of this scoreboard is not to claim production model performance. It shows the evaluation habit employers should care about: define expected behavior, run cases automatically, and keep risky support actions inside human-review boundaries.

## Repository Map

- `auva_demo/` - small Python package for the demo workflow
- `data/synthetic_cases.jsonl` - public-safe synthetic support cases
- `docs/architecture.md` - architecture and design notes
- `docs/ci-cd.md` - CI/CD and quality gate notes
- `docs/evaluation.md` - synthetic evaluation plan and public scoreboard language
- `docs/interview_demo.md` - short screen-share talk track
- `docs/public_safety.md` - what was excluded from the public portfolio version
- `Makefile` - interview-friendly `make demo` and `make check` commands
- `scripts/run_demo.py` - convenience runner
- `scripts/evaluate_demo.py` - synthetic scoreboard runner
- `scripts/interview_demo.py` - no-argument interview demo
- `tests/` - unit tests for routing and guardrails
- `.github/workflows/ci.yml` - GitHub Actions CI scaffold

## Public-Safety Boundary

This repository deliberately excludes:

- real emails
- real customer names
- real order data
- private databases
- `.env` files
- OAuth tokens
- merchant credentials
- private eval artifacts
- internal agent names and private workspace doctrine

All demo data is synthetic.

## Suggested LinkedIn / Resume Wording

Built AUVA, a public-safe AI commerce-operations demo showing support triage, context-bundle assembly, policy-aware action routing, human-review approvals, synthetic evaluation, unit-tested guardrails, and GitHub Actions CI.

## Status

Employer-facing portfolio demo. Public-safe, intentionally small, and designed to show implementation judgment rather than expose private production machinery.
