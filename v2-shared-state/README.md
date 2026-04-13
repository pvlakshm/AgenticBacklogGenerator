# Backlog Generator v2-shared-state

The v2 iteration introduces a centralized **Shared State Dictionary**. Unlike the previous version, where information was passed linearly from one function to the next, v2 ensures every "agent" or step in the pipeline has access to the original requirement and all previously generated artifacts.

## Architectural Shift: Shared State

In this version, the pipeline transitions from **Stateless Pipes** to a **Centralized Context**:

* **v1 (Linear):** Requirement -> Epic -> Features.
* **v2 (State-Based):** A central `state` dictionary stores the `requirement`, `epic`, and `features`. Every step updates this dictionary, making the full project history accessible to each LLM call.


## Key Files

* `backlog_gen_v2.py`: Implementation of the state-based orchestrator.
* `test_backlog_gen_v2.py`: Unit tests verifying state persistence and data integrity.

## Testing the "Memory"

The test suite is designed to prove that the pipeline no longer "forgets" initial constraints.

### The Persistence Test
In `test_pipeline_data_chaining`, we don't just check if the output looks correct. We inspect the **arguments** of the second LLM call to confirm that the original requirement was actually included in the prompt alongside the Epic. This is a critical check for **context integrity**.

### Running Tests
Execute the suite from your project root:
```bash
pytest test_backlog_gen_v2.py
```

## 📋 Learning Objectives for Students

1.  **State Management:** Understand why a dictionary is more scalable for complex workflows than simple string passing.
2.  **Context Injection:** Learn how to combine multiple pieces of state (e.g., Requirement + Epic) into a single prompt to guide the LLM.
3.  **Advanced Mocking:** Use `call_args_list` to verify not just *what* the LLM returned, but *what it was told* (the input side of the contract).

---

### Suggested Exercise
Try a requirement with a specific constraint:
`python backlog_gen_v2.py "Build a fuel tracker. Constraint: Generate exactly 3 features."`

Compare this to v1. You will notice that the feature list in v2 is far more likely to respect the "Generate exactly 4 features" constraint because it was explicitly provided during that step.