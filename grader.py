from abc import ABC, abstractmethod
from interaction import append_message, chat
from validator import ValidationStrategy, PythonValidation, JsonValidation, RegexValidation 


VALIDATORS: dict[str, ValidationStrategy] = {
    'python': PythonValidation(),
    'json': JsonValidation(),
    'regex': RegexValidation()
}

class GradingStrategy(ABC):
    @abstractmethod
    def grade(self, test_case: dict[str, str], output: str) -> int:
        ...

class CodeGrader(GradingStrategy):
    """
    Code grading is useful for evaluating 'Format' and 'Valid Syntax'.
    e.g: output should be Python and the code syntax is valid.
    """
    def grade(self, text_case: dict[str, str], output: str) -> int:
        format = text_case['format']
        return VALIDATORS[format].validate(output)


class ModelGrader(GradingStrategy):
    """
    Model grading is useful for evaluating 'Task Following': check if addresses the user's tasks and if the generated
    code is accurate
    """
    def grade(self, test_case: dict[str, str], output: str) -> int:
        prompt = f"""
        Given the task: {test_case['task']} and the output for the task produced by a model:
        <solution>
        {output}
        </solution>
        
        The criteria to evaluate the solution is the following:
        <solution_criteria>
        {test_case['solution_criteria']}
        </solution_criteria>

        > Evaluate giving a score value if the 'output' directly and clearly addresses the user's task.
        Generated code should be accurate.

        * You should give an integer score value between 1 and 10 (higher is better).
        * Respond only with the score value. Not any kind of justification.
        """
        messages = []
        append_message(messages, 'user', prompt)

        return int(chat(messages)) # Dangerous (not running an eval to check if the response is '<int>')
    

from statistics import mean

class CombinedGrader(GradingStrategy):
    def __init__(self, graders: list[GradingStrategy] = [CodeGrader(), ModelGrader()]):
        self.graders = graders
        
    def grade(self, test_case: dict[str, str], output: str) -> float:
        return mean(grader.grade(test_case, output) for grader in self.graders)
