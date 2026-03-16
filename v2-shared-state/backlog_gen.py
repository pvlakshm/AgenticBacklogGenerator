import sys
import ollama

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

def generate_epic(state):
    requirement = state["requirement"]
    result = ask_llm(
        role="Product Manager",
        task="Create exactly ONE epic from the requirement and define business-level acceptance criteria.",
        input_text=requirement,
        output_format="""
Epic:
<short epic title>

Description:
<1-2 sentence description>

Acceptance Criteria:
- criterion 1
- criterion 2
- criterion 3
""",
    )
    state["epic"] = result
    return state

def generate_features(state):
    epic = state["epic"]
    result = ask_llm(
        role="Product Manager",
        task="Break the epic into 3 to 5 features. Each feature must have acceptance criteria.",
        input_text=epic,
        output_format="""
Features:

Feature: <feature name>
Description: <short description>
Acceptance Criteria:
- criterion
- criterion

Feature: <feature name>
Description: <short description>
Acceptance Criteria:
- criterion
- criterion
""",
    )
    state["features"] = result
    return state

def generate_stories(state):
    features = state["features"]
    result = ask_llm(
        role="Product Owner",
        task="Create user stories for the features with acceptance criteria.",
        input_text=features,
        output_format="""
User Stories:

Story:
As a <user>
I want <goal>
So that <benefit>

Acceptance Criteria:
- criterion
- criterion

Story:
As a <user>
I want <goal>
So that <benefit>

Acceptance Criteria:
- criterion
- criterion
""",
    )
    state["stories"] = result
    return state

def generate_tests(state):
    stories = state["stories"]
    result = ask_llm(
        role="QA Engineer",
        task="Generate one test case per user story.",
        input_text=stories,
        output_format="""
Test Cases:

Test:
Name: <short name>
Steps:
1. step
2. step

Expected Result:
<expected outcome>
""",
    )
    state["tests"] = result
    return state

def main():
    if len(sys.argv) < 2:
        print("Usage: python backlog_gen.py 'requirement'")
        return

    state = {
        "requirement": sys.argv[1],
        "epic": None,
        "features": None,
        "stories": None,
        "tests": None
    }

    print("\nRequirement")
    print("-----------")
    print(state['requirement'])

    print("\nEpic")
    print("----")
    state = generate_epic(state)
    print(state["epic"])
    
    print("\nFeatures")
    print("--------")
    state = generate_features(state)
    print(state["features"])
    
    print("\nUser Stories]")
    print("------------")
    state = generate_stories(state)
    print(state["stories"])
    
    print("\nTest Cases")
    print("----------")
    state = generate_tests(state)
    print(state["tests"])

if __name__ == "__main__":
    main()