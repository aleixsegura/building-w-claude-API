"""
Use message prefilling and stop sequences only to get three different commands in a single response
There shouldn't be any comments or explanation
Hint: message prefilling isn't limited to just characters like ```
"""

# Message prefilling not supported with claude-sonnet-4-6,
# so we add a constraint to our prompt.

from config import client, MODEL, MAX_TOKENS
from interaction import append_message

messages = []

prompt = """
Generate three different sample AWS CLI commands. Each should be very short.
"""

constraint = "Return ONLY the bash code, without markdown formatting."

def chat(messages: list, *, stop_sequences: list[str] = []) -> str:
    message = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=messages,
        stop_sequences=stop_sequences
    )
    return message.content[0].text

append_message(messages, 'user', f'{prompt} {constraint}')


response = chat(messages)
print(response)