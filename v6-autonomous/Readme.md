# v6-autonomous

## What this version does
Adds a global critic that reviews the full backlog (epic + features together) after all agents complete. If the full backlog fails review, the global critic decides which agent to re-run - and the Coordinator selectively re-executes from that point forward, without discarding work that was already approved.

## What's new
- **`global_critic` template** - reviews the full backlog holistically using objective, countable rules. Returns one of: `APPROVED`, `REDO: epic`, or `REDO: features` with a reason
- **`MAX_GLOBAL_RETRIES`** constant - controls the maximum number of global retry cycles, independent of `MAX_REVISIONS`
- **Global critic loop** in `Coordinator.run()` - runs after all agents complete, routes re-execution based on the verdict
- **`_run_global_critic()`** - assembles the full backlog into a single input and calls the global critic
- **`_parse_redo()`** - extracts the agent key from a `REDO` verdict, keeping routing logic in the LLM
- **Selective re-execution** - if `REDO: features`, only FeaturesAgent re-runs. If `REDO: epic`, both EpicAgent and FeaturesAgent re-run (since features depend on the epic)

## Key concepts
- Holistic quality review across multiple artifacts
- LLM-driven routing - the model decides where to re-enter the pipeline
- Selective re-execution - don't discard good work, only redo what failed
- Two-level quality control: per-artifact critic loop (v4) + global backlog critic (v6)
- Autonomous termination - the system decides when the backlog is done

## Why this matters
In real agentic systems, individual artifact quality is not enough - the outputs must also be coherent with each other. A global critic that can route re-execution to the right agent, without restarting the entire pipeline, is a key pattern in production systems like LangGraph.

## What's unchanged from v5
- All agent classes and their internal critic loops
- Coordinator structure and Planner logic
- All prompt templates except the addition of `global_critic`
- Shared state pattern

## How to run
```bash
python backlog_gen_v6.py "Grandma has a car and wants to know when she should refill fuel"
```

## Testing

### Install dependencies
```bash
pip install pytest pytest-cov
```

### Run tests
```bash
python -m pytest test_backlog_gen_v6.py -v
```

### Run with coverage
```bash
python -m pytest test_backlog_gen_v6.py --cov=backlog_gen_v6 --cov-report=term-missing
```

### What the tests cover
- `_parse_redo` returns `"epic"` for `REDO: epic` verdicts
- `_parse_redo` returns `"features"` for `REDO: features` verdicts
- `_parse_redo` is case-insensitive
- `_parse_redo` returns `None` for `APPROVED` and unparseable verdicts
- `_run_global_critic` includes the requirement, epic, and features in the LLM input
- `_run_global_critic` uses the `global_critic` template task
- `_run_global_critic` returns the raw LLM verdict
- `REDO: epic` causes re-execution of both `EpicAgent` and `FeaturesAgent`
- `REDO: features` causes re-execution of only `FeaturesAgent`
- `_run_planner` normalizes step names to lowercase and raises on invalid output

### What the tests do NOT cover
- LLM output quality — no real LLM calls are made; `ollama` is mocked
- The global critic loop retry count — `MAX_GLOBAL_RETRIES` enforcement is not unit tested
- The `main()` function — CLI argument handling is not unit tested