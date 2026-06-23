"""
Our prompt needs to assist users in writing three specific types of output for AWS use cases:

- Python code
- JSON configuration files
- Regular expressions

The key requirement is that when a user requests help with a task, 
we return clean output in one of these formats without any extra explanations, 
headers, or footers.
"""

import json
from typing import Any
from grader import CombinedGrader
from interaction import append_message, chat


def run_prompt(test_case: dict[str, str]) -> str:
    prompt = f"""
        Please provide a solution for the following task:
    {test_case['task']} using the format: {test_case['format']}

    * Respond only with Python, JSON, or a plain Regex
    * If the format is python, produce python code only, if the format is json, produce json text only, and if the format is
    regex produce regex expressions only.
    * Do not add any comments or commentary or explanation
    * Do not include formatting code fences like ```python or ```json
    """

    messages = []
    append_message(messages, 'user', prompt)
    return chat(messages)
    # A function to ensure no code fences are returned should be applied before return llm response


def run_test_case(test_case: dict[str, str]) -> dict[str, Any]:
    output = run_prompt(test_case)

    score = CombinedGrader().grade(test_case, output)
    return {
        'output': output,
        'test_case': test_case,
        'score': score
    }


from statistics import mean

def run_eval(dataset: list[dict[str, str]]) -> int:
    results = []

    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)

    return mean(result['score'] for result in results)


def generate_dataset() -> None:
    prompt = """
        Generate an evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts that generate Python, JSON, 
        or Regex specifically for AWS-related tasks. Generate an array of JSON objects, each representing task that requires Python, 
        JSON, or a Regex to complete.
    
    Example Output:
    ```json
    [
        {
            "task": "Description of task",
            "format": "python | json | regex",
            "solution_criteria": "e.g: Must include runtime, memory size, timeout, and basic structure for AWS Lambda configuration.",
        },
        ...aditional
    ]
    ```
    * Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a single regex
    * Focus on tasks that do not require writing much code

    Please generate 3 objects.
    """

    messages = []

    # !! IMPORTANT: A lot of Json used in training come with ```json, so its difficult to enforce the response to not contain
    # this characters, even with a system prompt.
    system = "Do NOT include markdown formatting keywords in you final response. Produce ONLY the text to generate the json."

    append_message(messages, 'user', prompt)
    append_message(messages, 'assistant', '[') # Prefill
    text = '[' + chat(messages, system=system)

    # Deserializes raw model text to python obj (list)
    data = json.loads(text)

    # Save obj to .json
    with open('prompt-eval/dataset.json', 'w') as f:
        json.dump(data, f, indent=2)


generate_dataset()

with open('prompt-eval/dataset.json', 'r') as f:
    dataset = json.load(f)

score = run_eval(dataset)

print('Mean score = ', round(score, 2))
