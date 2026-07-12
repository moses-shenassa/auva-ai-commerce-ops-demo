# GitHub Publish Notes

This repo is ready to be published as a public-safe portfolio artifact after Moses chooses the GitHub repository name.

Recommended public repo name:

```text
auva-ai-commerce-ops-demo
```

Alternative names:

```text
auva-ai-operations-case-study
auva-commerce-ops-ai-demo
auva-human-in-the-loop-commerce-ai
```

## Pre-publish checklist

Run these from the repo root:

```bash
python -m unittest discover -s tests
python -m auva_demo.cli --case data/synthetic_cases.jsonl
rg -n "GOLEM|Nightstalker|Ravenmother|Hoodoo|Holy Mountain|Rue|gmail|shopify|secret|password|customer@|@gmail|sqlite|\\.db|real_support|Northstar|gwu1w1|hoodoomoses" . --glob '!docs/github_publish.md'
```

The `rg` command should return no matches. A no-match exit code is expected.

## Publish routes

### Route A: GitHub website

1. Create a new empty GitHub repo named `auva-ai-commerce-ops-demo`.
2. Do not initialize it with README, license, or `.gitignore`.
3. Add the remote locally:

```bash
git remote add origin git@github.com:moses-shenassa/auva-ai-commerce-ops-demo.git
git branch -M main
git push -u origin main
```

### Route B: GitHub CLI

This workspace currently does not have `gh` installed. If installed and authenticated later:

```bash
gh repo create moses-shenassa/auva-ai-commerce-ops-demo --public --source=. --remote=origin --push
```

## Public positioning

Use this as the pinned GitHub repo description:

```text
Public-safe AUVA demo: AI-assisted commerce support triage, context bundles, human-review guardrails, synthetic evals, and CI/CD scaffold.
```

Use this for LinkedIn Featured:

```text
AUVA AI Commerce Ops Demo - a public-safe portfolio scaffold showing support-intent routing, context-bundle assembly, policy-aware guardrails, human-review approval tiers, synthetic evaluation data, and GitHub Actions CI.
```
