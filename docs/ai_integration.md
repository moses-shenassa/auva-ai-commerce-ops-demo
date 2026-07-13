# AI Integration

AUVA now includes an optional live AI classifier for public-safe support intent.

## How It Works

`auva_demo/ai.py` sends a structured classification request to OpenAI's chat
completion API when `OPENAI_API_KEY` is available.

The model returns JSON with:

- `intent`
- `confidence`
- `rationale`

Allowed intents are deliberately narrow:

- `tracking_delay`
- `change_shipping_address`
- `refund_request`
- `product_question`
- `damaged_item`
- `unknown`

The workflow then passes the AI-selected intent into deterministic business
logic. Refund review, replacement review, address-change escalation, manager
review, and auto-draft eligibility are still enforced by code.

## Why The Fallback Exists

The repository should be comfortable to run in an interview, on CI, or on a
machine with no API credentials. If no key is present, or the API call fails,
the workflow falls back to the offline classifier and prints:

```text
Classifier: offline_rules
```

When the OpenAI path is active, it prints:

```text
Classifier: openai
```

## Running The Live AI Path

```bash
OPENAI_API_KEY=... AUVA_AI_MODE=auto make demo
```

To force offline mode:

```bash
AUVA_AI_MODE=offline make demo
```

## Interview Positioning

The useful claim is not that the model can run the business by itself. The
useful claim is that AUVA separates AI interpretation from operational control:

```text
AI classifies messy support language.
Code enforces policy, risk, and approval boundaries.
Humans approve sensitive actions before anything external happens.
```
