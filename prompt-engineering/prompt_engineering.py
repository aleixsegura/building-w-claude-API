import json
from grader import ModelGrader
from interaction import chat, append_message

def generate_dataset() -> None:
    task = """
    Extract topics out of a passage of text from a scholarly into a list of JSON objects    
    """

    prompt_input = {
        'content': 'One paragraph of text from scholarly journal written in English' 
    }

    output_file = 'prompt-engineering/dataset.json'

    num_cases = 4

    prompt = f"""
    Create a dataset in json based in the description:

    {task}
    Include 'task' as part of the json. Do not include the topics.
    
    {prompt_input} should be included to.
    
    Add a 'solution_criteria' field that is a list of strings each one representing key points for evaluating if the topics are appropiate.

    Generate {num_cases} cases for the dataset.
    """

    messages = []
    append_message(messages, 'user', prompt)
    append_message(messages, 'assistant', '[')
    response = chat(messages)

    try:
        data = json.loads('[' + response)
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
    except json.JSONDecodeError:
        raise ValueError('Not a valid json. Try to format it or check model response')


def gen_response(test_case: dict[str, str]):
    prompt = f"""
    Provide a solution for {test_case['task']} for the following content:
    
    <content>
    {test_case['content']}.
    </content>

    """

    messages = []
    append_message(messages, 'user', prompt)
    response = chat(messages)
    return response


def eval(dataset: list[dict[str, str]]) -> float:
    grades = []
    for test_case in dataset:
        output = gen_response(test_case)
        grade = ModelGrader().grade(test_case, output)
        grades.append(grade)
    return sum(grades) / len(grades)


generate_dataset()

with open('prompt-engineering/dataset.json', 'r') as f:
    data = json.load(f)

score = eval(data)
print(f'Score = {score}')