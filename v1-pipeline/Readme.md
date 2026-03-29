# v1-pipeline

## What this version does
The simplest possible backlog generator. Takes a requirement string, generates an Epic, then passes the Epic to generate 3 Features. Each step is a plain function call.

## What's new
- Everything. This is the baseline.
- `ask_llm()` - the core LLM call, driven by prompt templates
- `generate_epic()` and `generate_features()` - two specialized functions
- A hardcoded sequential pipeline: epic -> features

## Key concepts
- Prompt templates (`TEMPLATES` dict)
- Sequential pipeline
- LLM chaining (output of one step feeds the next)

## Limitations
- No shared state - outputs are passed as raw strings between functions
- No dynamic planning - the sequence is always epic -> features
- No quality control - whatever the LLM generates is accepted as-is

## How to run
```bash
python backlog_gen_v1.py "Grandma has a car and wants to know when she should refill fuel"
```

## Testing

### Install dependencies
```bash
pip install pytest pytest-cov
```

### Run tests
```bash
python -m pytest test_backlog_gen_v1.py -v
```

### Run with coverage
```bash
python -m pytest test_backlog_gen_v1.py --cov=backlog_gen_v1 --cov-report=term-missing
```

### What the tests cover
- `ask_llm` calls `ollama.chat` with the configured `MODEL`
- `ask_llm` includes the template role, task, and input text in the prompt
- `ask_llm` strips whitespace from the LLM response
- `ask_llm` raises `KeyError` for an unknown template key
- `generate_epic` passes the requirement to the LLM and returns the response
- `generate_features` passes the epic to the LLM and returns the response
- The pipeline makes exactly 2 LLM calls in the correct order (epic then features)
- The epic output is passed as input to the features step

### What the tests do NOT cover
- LLM output quality - no real LLM calls are made; `ollama` is mocked
- Prompt effectiveness - use evals for that
- The `main()` function - CLI argument handling is not unit tested