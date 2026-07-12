# Evaluation

The production AUVA work used larger support-routing evaluation passes. This public scaffold does not include private eval artifacts or support-message data.

Instead, it includes a small synthetic evaluation pattern that demonstrates how the workflow can be tested.

## What The Tests Cover

- delayed orders route to `tracking_investigation`
- address changes after fulfillment require review
- refund requests require refund review and do not auto-send
- damaged paid items route toward replacement review
- low-risk product questions can become draft replies

## Public Scoreboard Language

Use public wording like this:

> Built a synthetic evaluation scaffold for AUVA showing policy-aware support routing, human-review approvals, and guardrail tests for refund, replacement, address-change, tracking-delay, and product-question workflows.

Do not publish private production scoreboard artifacts, raw real support cases, or customer-derived eval rows.
