.PHONY: demo evaluate test check
PYTHON ?= python3

demo:
	$(PYTHON) scripts/interview_demo.py

evaluate:
	$(PYTHON) scripts/evaluate_demo.py --case data/synthetic_cases.jsonl

test:
	$(PYTHON) -m unittest discover -s tests

check: test evaluate
	$(PYTHON) -m auva_demo.cli --case data/synthetic_cases.jsonl >/dev/null
	$(PYTHON) scripts/interview_demo.py >/dev/null
