# v3-planner-agent

## What this version does
Introduces a Planner - an LLM call that decides which backlog artifacts to generate before any generation happens. The pipeline is no longer hardcoded; the Planner determines the sequence dynamically at runtime.

## What's new
- **Planner** (`run_planner()`) - calls the LLM to decide which steps to run, returning a plan like `['epic', 'features']`
- **`TASK_MAP`** - maps planner output strings to their corresponding generator functions
- **`plan`** added to shared state
- Dynamic execution loop - iterates over the plan rather than calling functions directly

## Key concepts
- LLM-driven control flow
- Dynamic planning vs hardcoded sequencing
- The Planner as a meta-agent that decides what other agents do

## Why this matters
This is the first version where the LLM influences the control flow of the program, not just the content. This is a foundational principle of agentic systems - the model decides what to do, not just what to say.

## What's unchanged from v2
- Prompt templates for epic and features
- Shared state pattern
- No quality control

## How to run
```bash
python backlog_gen_v3.py "Grandma has a car and wants to know when she should refill fuel"
```

## Testing

### Install dependencies
```bash
pip install pytest pytest-cov
```

### Run tests
```bash
python -m pytest test_backlog_gen_v3.py -v
```

### Run with coverage
```bash
python -m pytest test_backlog_gen_v3.py --cov=backlog_gen_v3 --cov-report=term-missing
```

### What the tests cover
- `run_planner` uses the planner template task in the prompt
- `run_planner` correctly parses a full plan (`epic, features`)
- `run_planner` correctly parses a partial plan (`epic` only)
- `run_planner` filters out invalid steps not in `TASK_MAP`
- `run_planner` raises `ValueError` when no valid steps are found
- `run_planner` writes the parsed plan to `state["plan"]` and returns state
- `TASK_MAP` contains `epic` and `features` keys routing to the correct functions
- The full pipeline (planner + epic + features) makes exactly 3 LLM calls
- Steps execute in the order returned by the planner
- All state keys (`plan`, `epic`, `features`) are populated after the full pipeline

### What the tests do NOT cover
- LLM output quality — no real LLM calls are made; `ollama` is mocked
- Prompt effectiveness — use evals for that
- The `main()` function — CLI argument handling is not unit tested