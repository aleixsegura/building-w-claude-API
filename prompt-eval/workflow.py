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
from interaction import append_message, chat
from .grader import CombinedGrader


def run_prompt(test_case: dict[str, str]) -> str:
    prompt = f"""
        Please provide a solution for the following task:
    {test_case['task']}

    * Respond only with Python, JSON, or a plain Regex
    * Do not add any comments or commentary or explanation

    """

    messages = []
    append_message(messages, 'user', prompt)
    return chat(messages)


def run_test_case(test_case: dict[str, str]) -> dict[str, Any]:
    output = run_prompt(test_case)

    score =  CombinedGrader().grade(test_case, output)

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
            "format": "python | json | regex"
        },
        ...aditional
    ]
    ```
    
    * Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a single regex
    * Focus on tasks that do not require writing much code

    Please generate 3 objects.
    """

    messages = []

    system = "Generate only the json text not any kind of formatting and no markdown instructions like <```language>"

    append_message(messages, 'user', prompt)
    text = chat(messages, system=system)

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
