import ast
import json
import regex as re
from abc import ABC, abstractmethod


class ValidationStrategy(ABC):
    @abstractmethod
    def validate(self, text: str) -> int:
        ...

class PythonValidation(ValidationStrategy):
    def validate(self, text: str) -> int:
        try:
            ast.parse(text.strip())
            return 10
        except SyntaxError:
            return 0

class JsonValidation(ValidationStrategy):
    def validate(self, text: str) -> int:
        try:
            json.loads(text.strip())
            return 10
        except json.JSONDecodeError:
            return 0

class RegexValidation(ValidationStrategy):
    def validate(self, text: str) -> int:
        try:
            re.compile(text.strip())
            return 10
        except re.error:
            return 0
