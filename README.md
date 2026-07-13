# AUVA AI Commerce Ops Demo

[![CI](https://github.com/moses-shenassa/auva-ai-commerce-ops-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/moses-shenassa/auva-ai-commerce-ops-demo/actions/workflows/ci.yml)

AUVA is a public-safe portfolio scaffold for an AI-assisted commerce operations assistant.

This repository is not the private production workspace. It is a sanitized demo that shows the product architecture and implementation style behind AUVA without exposing customer records, merchant data, credentials, private databases, or internal operating artifacts.

## What AUVA Demonstrates

AUVA models a merchant-facing AI operations layer for commerce teams. The demo focuses on a narrow but realistic wedge:

- assemble support context from synthetic customer, order, product, and policy data
- classify support intent
- choose a safe business action
- assign a human-review approval tier
- produce a short operator-facing recommendation and customer reply draft

The key idea is not "AI writes emails." The key idea is a supervised operating loop that sees commerce truth, sees conversations, remembers policy, and helps a human operator move work safely.

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
python -m auva_demo.cli --case data/synthetic_cases.jsonl
python -m unittest
```

No network access, API keys, databases, or external services are required.

## Example Output

```text
Case: delayed-delivery-001
Intent: tracking_delay
Action: tracking_investigation
Approval: review_required
Confidence: 0.84

Operator note:
Customer is asking about a delayed paid order. Order is in transit and beyond the expected delivery window. Recommend checking tracking, acknowledging the delay, and offering follow-up if the carrier status does not move.
```

## Repository Map

- `auva_demo/` - small Python package for the demo workflow
- `data/synthetic_cases.jsonl` - public-safe synthetic support cases
- `docs/architecture.md` - architecture and design notes
- `docs/evaluation.md` - synthetic evaluation plan and public scoreboard language
- `scripts/run_demo.py` - convenience runner
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

Built AUVA, a sanitized AI commerce-operations demo showing supervised support triage, context-bundle assembly, policy-aware action routing, human-review approvals, synthetic evaluation, and CI/CD-ready packaging.

## Status

Portfolio scaffold. Public-safe and intentionally small.
