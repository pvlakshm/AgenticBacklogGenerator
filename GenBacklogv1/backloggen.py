import sys
import ollama
from rich import print

MODEL = "gemma3:1b"

def call_llm(prompt):
  response = ollama.chat(
    model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
  return response["message"]["content"]


def analyze_requirement(req):
    prompt = f"""
You are a product analyst.

Analyze this requirement and summarize the product goal.

Requirement:
{req}

Return a short structured explanation.
"""
    return call_llm(prompt)


def generate_epic(req):
    prompt = f"""
You are a product manager.

Create ONE Epic for the following requirement.

Requirement:
{req}

Format:
Epic Title:
Epic Description:
"""
    return call_llm(prompt)


def generate_features(epic):
    prompt = f"""
Break the following Epic into Features.

{epic}

Return 3-5 Features.

Format:
Feature:
Description:
"""
    return call_llm(prompt)


def generate_user_stories(features):
    prompt = f"""
Generate Agile User Stories for the following Features.

{features}

Format each as:

User Story:
As a <user>
I want <goal>
So that <benefit>
"""
    return call_llm(prompt)


def generate_test_cases(stories):
    prompt = f"""
Generate Test Cases for the following User Stories.

{stories}

Format:

Test Case:
Steps:
Expected Result:
"""
    return call_llm(prompt)


def main():

    if len(sys.argv) < 2:
        print("Usage: python agentic_backlog_1.py 'your requirement'")
        sys.exit()

    requirement = sys.argv[1]

    print("\n[bold yellow]Requirement[/bold yellow]")
    print(requirement)

    analysis = analyze_requirement(requirement)
    print("\n[bold cyan]Analysis[/bold cyan]")
    print(analysis)

    epic = generate_epic(requirement)
    print("\n[bold green]Epic[/bold green]")
    print(epic)

    features = generate_features(epic)
    print("\n[bold blue]Features[/bold blue]")
    print(features)

    stories = generate_user_stories(features)
    print("\n[bold magenta]User Stories[/bold magenta]")
    print(stories)

    tests = generate_test_cases(stories)
    print("\n[bold red]Test Cases[/bold red]")
    print(tests)


if __name__ == "__main__":
    main()