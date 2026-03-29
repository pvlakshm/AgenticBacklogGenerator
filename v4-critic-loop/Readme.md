# v4-critic-loop

## What this version does
Adds a critic-revise loop around each generated artifact. After generation, a critic LLM reviews the artifact and either approves it or requests specific revisions. The generator revises based on the feedback, up to `MAX_REVISIONS` times.

## What's new
- **`critic` template** - reviews an artifact against the original requirement, returns `APPROVED` or `REVISION NEEDED: <issues>`
- **`revise` template** - rewrites an artifact based on critic feedback
- **`critic_loop()`** - runs up to `MAX_REVISIONS` critique-revise cycles for a single artifact
- **`MAX_REVISIONS`** constant - controls the maximum number of revision attempts
- Each generator function now wraps its output in `critic_loop()` before storing in state

## Key concepts
- Self-correction loop
- Separation of generation and evaluation
- Fail loudly - if the critic cannot approve after `MAX_REVISIONS`, the pipeline halts with an error rather than passing a substandard artifact downstream

## Why this matters
A bad epic will produce bad features. Quality gating at each step prevents errors from propagating. This pattern - generate, critique, revise - is one of the most common patterns in production agentic systems.

## What's unchanged from v3
- Planner and dynamic execution
- Shared state pattern
- Prompt templates for epic and features

## How to run
```bash
python backlog_gen_v4.py "Grandma has a car and wants to know when she should refill fuel"
```

## Testing

### Install dependencies
```bash
pip install pytest pytest-cov
```

### Run tests
```bash
python -m pytest test_backlog_gen_v4.py -v
```

### Run with coverage
```bash
python -m pytest test_backlog_gen_v4.py --cov=backlog_gen_v4 --cov-report=term-missing
```

### What the tests cover
- `critic_loop` returns the artifact unchanged on immediate approval
- `critic_loop` makes exactly 1 LLM call when the critic approves immediately
- `critic_loop` approval detection is case-insensitive
- `critic_loop` calls the revise template when revision is needed
- `critic_loop` includes the critic feedback in the revise prompt
- `critic_loop` returns the revised artifact after a successful revision cycle
- `critic_loop` returns the last revised artifact when `MAX_REVISIONS` is reached
- `critic_loop` never exceeds `MAX_REVISIONS` LLM calls
- `generate_epic` stores the approved artifact in `state["epic"]`
- `generate_epic` stores the revised artifact when revision was needed
- `run_planner` correctly parses the plan and raises on invalid output

### What the tests do NOT cover
- LLM output quality - no real LLM calls are made; `ollama` is mocked
- Whether the critic's feedback is meaningful - use evals for that
- The `main()` function - CLI argument handling is not unit tested