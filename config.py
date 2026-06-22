from typing import Final
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

MODEL: Final[str] = 'claude-haiku-4-5'
MAX_TOKENS: Final[int] = 1000