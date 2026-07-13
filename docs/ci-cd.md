# CI/CD Notes

This repo uses GitHub Actions as a lightweight quality gate for the public AUVA demo.

## Current Workflow

`.github/workflows/ci.yml` runs on every push and pull request:

1. Check out the repository
2. Set up Python 3.11
3. Run unit tests
4. Run the CLI demo against synthetic cases
5. Run the synthetic evaluation scoreboard

## Why This Is Included

The goal is to show that the portfolio artifact is not only a static case study. It has a runnable package, repeatable tests, and a CI gate that proves the demo still executes after changes.

For AI implementation and enablement roles, that matters because a useful AI workflow needs operational habits around testing, release checks, and regression control. A good demo should not depend on a private machine, live credentials, or a one-off manual run.

## Commands Mirrored By CI

```bash
python -m unittest discover -s tests
python -m auva_demo.cli --case data/synthetic_cases.jsonl
python scripts/evaluate_demo.py --case data/synthetic_cases.jsonl
```
