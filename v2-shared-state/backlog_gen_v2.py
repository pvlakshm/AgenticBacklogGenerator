import sys
import os
import ollama

MODEL = "gemma3:1b"

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")


# --- Prompt Loading ---

def load_prompt(name: str) -> dict:
    """
    Load a .prompt.md file from the prompts/ directory.

    Expects standard Markdown with # headings as section markers:
        # Role
        # Task
        # Format

    Returns a dict with keys:
        - 'role'   (str)  content under the # Role heading
        - 'task'   (str)  content under the # Task heading
        - 'format' (str)  content under the # Format heading
    """
    path = os.path.join(PROMPTS_DIR, f"{name}.prompt.md")
    with open(path, "r") as f:
        raw = f.read()

    sections = {}
    current_key = None
    current_lines = []

    for line in raw.splitlines():
        if line.startswith("# "):
            if current_key is not None:
                sections[current_key] = "\n".join(current_lines).strip()
            current_key = line[2:].strip().lower()
            current_lines = []
        else:
            current_lines.append(line)

    if current_key is not None:
        sections[current_key] = "\n".join(current_lines).strip()

    return {
        "role":   sections["role"],
        "task":   sections["task"],
        "format": sections["format"],
    }


def load_system_template() -> str:
    """Load the system prompt skeleton from system.prompt.md."""
    path = os.path.join(PROMPTS_DIR, "system.prompt.md")
    with open(path, "r") as f:
        return f.read()


# --- LLM Interface ---

def ask_llm(prompt_name: str, input_text: str) -> str:
    config = load_prompt(prompt_name)
    skeleton = load_system_template()

    prompt = skeleton.format(
        role=config["role"],
        task=config["task"],
        input_text=input_text,
        format=config["format"],
    )

    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.2},
    )

    return response["message"]["content"].strip()


# --- Specialized Functions ---

def generate_epic(state: dict) -> dict:
    print("Generating epic...")
    state["epic"] = ask_llm("epic", state["requirement"])
    return state


def generate_features(state: dict) -> dict:
    print("Generating features...")
    state["features"] = ask_llm("features", state["epic"])
    return state


# --- Execution ---

def main():
    if len(sys.argv) < 2:
        print("Usage: python backlog_gen_v2.py 'requirement'")
        return

    requirement = sys.argv[1]

    # Initialize the Shared State
    state = {
        "requirement": requirement,
        "epic": None,
        "features": None,
    }

    print(f"\nProcessing Requirement: {state['requirement']}")

    # Run the sequence
    state = generate_epic(state)
    state = generate_features(state)

    # Final Output
    print("\n" + "=" * 60)
    print(f"\nEPIC:\n{state['epic']}")
    print(f"\nFEATURES:\n{state['features']}")


if __name__ == "__main__":
    main()
