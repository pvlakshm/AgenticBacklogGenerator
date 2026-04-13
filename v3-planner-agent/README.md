This `README.md` details the transition to an **Agentic Planner Architecture** in version 3. This iteration introduces dynamic orchestration and the formal use of a **System Prompt** to separate operational policy from user data.

---

# Backlog Generator v3-planner-agent

Version 3 transforms the backlog generator from a static script by intrducing a dynamic planning loop and utilizes the **System/User role distinction** to enforce rigorous orchestration.

## Key Architectural Evolutions

### 1. Dynamic Planning Loop
In v1 and v2, the order of execution was hard-coded. In v3, the orchestrator uses a `while` loop that consults the current `state` and the `history` of actions to decide the next step. This allows the system to be more adaptive to the state of the project.


### 2. System Prompt Integration
We have introduced a formal **System Prompt** (`planner_system.prompt.md`). In rigorous software engineering, this acts as the "Instruction Manual" or "Policy Kernel" for the LLM:
* **System Role:** Defines the persona (Project Orchestrator), available tools, and operational constraints (e.g., "Do not ask for confirmation").
* **User Role:** Provides the specific context and data for the current task.

## Testing the Orchestrator

The test suite has been expanded to verify the integrity of the agent's "brain" and its audit trail.

* **Contract Verification:** `test_pipeline_uses_system_prompt` ensures that the orchestration policy is correctly transmitted to the LLM's system role.
* **Auditability:** `test_pipeline_execution_history` verifies that the agent maintains a chronological record of its decisions (e.g., `["epic", "features"]`).

### Running the Suite
```bash
pytest test_backlog_gen_v3.py
```

## Project Components

* `backlog_gen_v3.py`: The agentic orchestrator with a dynamic planning loop.
* `test_backlog_gen_v3.py`: Tests for system prompt adherence and execution history.
* `prompts/planner_system.prompt.md`: The externalized policy defining the agent's behavior.

## Learning Objectives for Students

1.  **Orchestration vs. Automation:** Understand the difference between a fixed script and an agent that "plans" its work.
2.  **Role-Based Prompting:** Learn how to use the `system` role to lock down agent behavior, preventing conversational "drift" or unauthorized deviations.
3.  **Tracking:** Recognize the importance of the `history` key as a mechanism for debugging and auditing autonomous systems.

---

### Suggested Exercise
Modify the `planner_system.prompt.md` to change the agent's "Operational Rules." For instance, instruct it to generate a "Risk Assessment" instead of "Features" when a requirement is flagged as "Urgent." Observe how the `history` in `run_pipeline` reflects this change in the agent's dynamic decision-making (e.g., "Urgent: The fuel sensor is leaking on the main tank.").

#### Step 1: Update the Policy (Prompt)
Modify `prompts/planner_system.prompt.md` to define the new business logic:
* **Add Rule:** "If the user requirement includes the word 'Urgent', skip GENERATE_FEATURES and perform a RISK_ASSESSMENT."

#### Step 2: Update the Execution (Implementation)
Update the loop in `backlog_gen_v3.py` to allow the orchestrator to act on this branch:
```python
# Inside run_pipeline loop
if "Urgent" in state["requirement"] and state.get("epic"):
    current_step = "risk_assessment"
else:
    current_step = "epic" if not state.get("epic") else "features"
```

#### Step 3: Update the Verification (Tests)
Add a test case to `test_backlog_gen_v3.py` to ensure the **Tracking** reflects this specific path. This ensures the agentic logic remains deterministic and measurable:
```python
def test_pipeline_urgent_branching(standard_mock_llm, prompts):
    """Verify the agent tracks the 'risk_assessment' path when 'Urgent' is present."""
    result = v3.run_pipeline("Urgent: Sensor leak", prompts, standard_mock_llm)
    
    # Assert the Tracking history shows the correct alternate path
    assert "risk_assessment" in result["history"]
    assert "features" not in result["history"]
```

**Goal:** Observe how the **Tracking** history in the returned `state` changes from `["epic", "features"]` to `["epic", "risk_assessment"]` based solely on the input string and the updated policy.