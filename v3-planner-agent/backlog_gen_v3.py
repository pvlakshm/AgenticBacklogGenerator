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
# ... (load_prompts remains identical) ...

class OllamaLLM:
    def __init__(self, model=None, temperature=0.2):
        self.model = model or os.environ.get("MODEL", "gemma3:1b")
        self.temperature = temperature

    # Minimal Diff: Added system_prompt parameter and role handling
    def generate(self, prompt, system_prompt=None):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = ollama.chat(
            model=self.model,
            messages=messages,
            options={"temperature": self.temperature}
        )
        return response["message"]["content"].strip()

# -----------------------------
# v3 Agentic Planner Pipeline
# -----------------------------
def run_pipeline(requirement, prompts, llm_client):
    state = {"requirement": requirement, "history": []}
    
    # The System Prompt acts as the "Instruction Manual" or Policy
    system_prompt = prompts["planner_system"]
    
    # Planner loop: Decides actions dynamically
    while len(state["history"]) < 2:  # Minimal logic to ensure Epic then Features
        current_step = "epic" if not state.get("epic") else "features"
        
        user_input = f"Current State: {state}\nNext Task: Generate {current_step}"
        output = llm_client.generate(user_input, system_prompt=system_prompt)
        
        state[current_step] = output
        state["history"].append(current_step)

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