import sys
import ollama
import json

MODEL = "gemma3:1b"

def ask_llm(role, task, input_text, output_format):
    prompt = f"""
You are a professional {role}.

Task:
{task}

INPUT:
{input_text}

OUTPUT FORMAT:
{output_format}

Rules:
- Follow the output format exactly
- Do not add explanations
- Do not add extra sections
"""
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.2},
    )
    return response["message"]["content"].strip()

# def plan_backlog(state):
#     """The Planner Agent: Decides what needs to be generated."""
#     requirement = state["requirement"]
#     result = ask_llm(
#         role="Solution Architect",
#         task="Analyze the requirement and create a 2-step execution plan: 'generate_epic' then 'generate_features'.",
#         input_text=requirement,
#         output_format='{"plan": ["generate_epic", "generate_features"]}'
#     )
#     # Basic parsing to extract the list; gemma3:1b is usually good with clean JSON strings.
#     try:
#         plan_data = json.loads(result)
#         state["plan"] = plan_data.get("plan", [])
#     except:
#         # Fallback if the LLM adds markdown or formatting
#         state["plan"] = ["generate_epic", "generate_features"]
    
#     return state


def plan_backlog(state):
    """The Autonomous Planner: Decides the sequence based on goals, not hints."""
    requirement = state["requirement"]
    
    # We describe the 'Tools' available to the agent
    capabilities = """
    1. generate_epic: Use this to create a high-level goal and criteria.
    2. generate_features: Use this to break an existing epic into smaller pieces.
    """

    result = ask_llm(
        role="Technical Program Manager",
        task=f"Given these capabilities: {capabilities}\nCreate a logical execution plan to transform the requirement into a structured backlog.",
        input_text=requirement,
        output_format='{"plan": ["step_1", "step_2"]}'
    )
    
    try:
        plan_data = json.loads(result)
        state["plan"] = plan_data.get("plan", [])
    except:
        # Fallback logic remains essential for local 1b models
        state["plan"] = ["generate_epic", "generate_features"]
    
    return state


def generate_epic(state):
    print("\n[Planner executing: generate_epic]")
    requirement = state["requirement"]
    result = ask_llm(
        role="Product Manager",
        task="Create exactly ONE epic from the requirement and define business-level acceptance criteria.",
        input_text=requirement,
        output_format="Epic: <title>\nDescription: <desc>\nAcceptance Criteria:\n- criterion",
    )
    state["epic"] = result
    print(result)
    return state

def generate_features(state):
    print("\n[Planner executing: generate_features]")
    epic = state["epic"]
    result = ask_llm(
        role="Product Manager",
        task="Break the epic into 3 features. Each feature must have acceptance criteria.",
        input_text=epic,
        output_format="Features:\n\nFeature: <name>\nDescription: <desc>\nAcceptance Criteria:\n- criterion",
    )
    state["features"] = result
    print(result)
    return state

def main():
    if len(sys.argv) < 2:
        print("Usage: python backlog_gen.py 'requirement'")
        return

    state = {
        "requirement": sys.argv[1],
        "plan": [],
        "epic": None,
        "features": None,
    }

    print(f"Requirement: {state['requirement']}")

    # 1. Let the Planner decide the steps
    state = plan_backlog(state)
    print(f"Plan Created: {state['plan']}")

    # 2. Execute the plan dynamically
    # This maps the string name from the plan to the actual function
    actions = {
        "generate_epic": generate_epic,
        "generate_features": generate_features
    }

    for task in state["plan"]:
        if task in actions:
            state = actions[task](state)

if __name__ == "__main__":
    main()