# Public-Safety Notes

This repository is intentionally separate from the private AUVA working environment.

## Excluded From This Public Demo

- real customer names, emails, addresses, and order records
- private merchant data
- live support messages
- OAuth tokens, API keys, and `.env` files
- local databases and trace stores
- private evaluation artifacts
- internal agent names, operating doctrine, and workspace notes

## Included Instead

- synthetic support cases
- deterministic workflow logic
- public-safe architecture notes
- unit tests
- a synthetic evaluation scoreboard
- GitHub Actions CI

## Why The Boundary Exists

AUVA's useful product pattern depends on commerce context, but a portfolio repo should not leak commerce data to prove that context exists. This demo preserves the transferable engineering pattern while keeping the real operational workspace private.
