# v5-multi-agent

## What this version does
Refactors the generator functions into self-contained agent classes. Each agent owns its own generation logic and critic loop. A Coordinator orchestrates the agents using the Planner's output.

## What's new
- **`EpicAgent`** class - owns `generate_epic()` and its critic loop
- **`FeaturesAgent`** class - owns `generate_features()` and its critic loop
- **`Coordinator`** class - initializes shared state, runs the Planner, and dispatches to agents
- **`AGENT_MAP`** - maps planner output strings to agent classes (replaces `TASK_MAP`)
- Each agent's `run()` method provides a uniform interface; the named `generate_*()` methods contain the actual logic

## Key concepts
- Agent as a self-contained unit of responsibility
- Uniform agent interface (`run(state) -> state`)
- Coordinator as the orchestration layer
- Planner retained - the LLM still decides which agents to run

## Why this matters
As systems grow, functions become hard to manage. Encapsulating generation + quality control into an agent class makes each unit independently testable, replaceable, and extensible. This is how real multi-agent frameworks like CrewAI and AutoGen are structured.

## What's unchanged from v4
- Critic loop logic
- All prompt templates
- Shared state pattern
- Planner logic (now inside `Coordinator._run_planner()`)

## How to run
```bash
python backlog_gen_v5.py "Grandma has a car and wants to know when she should refill fuel"
```

## Testing

### Install dependencies
```bash
pip install pytest pytest-cov
```

### Run tests
```bash
python -m pytest test_backlog_gen_v5.py -v
```

### Run with coverage
```bash
python -m pytest test_backlog_gen_v5.py --cov=backlog_gen_v5 --cov-report=term-missing
```

### What the tests cover
- `EpicAgent.run` populates `state["epic"]` and returns the updated state
- `EpicAgent.run` does not modify `state["requirement"]`
- `EpicAgent` uses the epic template task in the LLM prompt
- `FeaturesAgent.run` populates `state["features"]` and returns the updated state
- `FeaturesAgent.run` reads from `state["epic"]` and does not modify it
- `AGENT_MAP` contains `epic` and `features` keys routing to the correct agent classes
- `Coordinator._run_planner` parses the plan and writes it to state
- `Coordinator._run_planner` normalizes step names to lowercase
- `Coordinator._run_planner` raises `ValueError` when no valid steps are found

### What the tests do NOT cover
- LLM output quality — no real LLM calls are made; `ollama` is mocked
- The full `Coordinator.run()` end-to-end flow — individual agents and planner are tested separately
- The `main()` function — CLI argument handling is not unit tested