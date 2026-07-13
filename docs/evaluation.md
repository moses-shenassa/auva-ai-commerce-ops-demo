# Evaluation

The production AUVA work used larger support-routing evaluation passes. This public scaffold does not include private eval artifacts or support-message data.

Instead, it includes a small synthetic evaluation pattern that demonstrates how the workflow can be tested.

## How To Run The Public Scoreboard

```bash
python3 scripts/evaluate_demo.py --case data/synthetic_cases.jsonl
```

Expected output:

```text
AUVA synthetic evaluation
Cases: 5
Intent accuracy: 5/5
Action accuracy: 5/5
Approval accuracy: 5/5
Overall field accuracy: 100%
```

## What The Tests Cover

- delayed orders route to `tracking_investigation`
- address changes after fulfillment require review
- refund requests require refund review and do not auto-send
- damaged paid items route toward replacement review
- low-risk product questions can become draft replies
- the OpenAI classifier can drive intent classification inside deterministic policy guardrails
- offline fallback remains available when no API key is present

## Why This Matters

The evaluation target is behavioral reliability, not demo theater. The important checks are:

- risky money-movement paths do not auto-send
- post-fulfillment address changes are escalated
- product questions can be drafted without pretending they are already sent
- support recommendations are tied to order, payment, fulfillment, and policy facts

That is the transferable implementation pattern: convert vague AI assistant behavior into testable workflow expectations.

## Public Scoreboard Language

Use public wording like this:

> Built a synthetic evaluation scaffold for AUVA showing AI-assisted intent classification, policy-aware support routing, human-review approvals, and guardrail tests for refund, replacement, address-change, tracking-delay, and product-question workflows.

Do not publish private production scoreboard artifacts, raw real support cases, or customer-derived eval rows.
