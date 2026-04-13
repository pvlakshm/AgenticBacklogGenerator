import os
import sys
import ollama

# -----------------------------
# Prompt Loading
# -----------------------------
def load_prompts(prompt_dir):
    prompts = {}
    for filename in os.listdir(prompt_dir):
        if filename.endswith(".md"):
            key = filename.replace(".prompt.md", "")
            with open(os.path.join(prompt_dir, filename), "r", encoding="utf-8") as f:
                prompts[key] = f.read()
    return prompts

# -----------------------------
# LLM Abstraction
# -----------------------------
class OllamaLLM:
    def __init__(self, model=None, temperature=0.2):
        self.model = model or os.environ.get("MODEL", "gemma3:1b")
        self.temperature = temperature

    def generate(self, prompt):
        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": self.temperature}
        )
        return response["message"]["content"].strip()

# -----------------------------
# v2 Shared State Pipeline
# -----------------------------
def run_pipeline(requirement, prompts, llm_client):
    # Initialize shared state
    state = {"requirement": requirement}

    # Step 1: Epic (Accesses requirement from state)
    epic_prompt = prompts["epic"].format(input=state["requirement"])
    state["epic"] = llm_client.generate(epic_prompt)

    # Step 2: Features (Accesses BOTH requirement and epic from state)
    # This prevents the "context loss" seen in v1
    feature_input = f"Requirement: {state['requirement']}\nEpic: {state['epic']}"
    feature_prompt = prompts["feature"].format(input=feature_input)
    state["features"] = llm_client.generate(feature_prompt)

    return state

# -----------------------------
# Execution
# -----------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: python pipeline.py \"<requirement>\"")
        sys.exit(1)

    requirement = sys.argv[1]
    prompts = load_prompts("prompts")
    llm = OllamaLLM()

    result = run_pipeline(requirement, prompts, llm)

    print("=== EPIC ===\n", result["epic"])
    print("\n=== FEATURES ===\n", result["features"])

if __name__ == "__main__":
    main()