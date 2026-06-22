"""
Exercise:
    1. Prompt the user to enter some input using
        the built-in 'input' function.
    2. Add it to a list of messages
    3. Call the API
    4. Add generated text to the lsit of messages
    5. Print the generated text
    6. repeat from #1
"""

from dotenv import load_dotenv
from interaction import append_message
from config import client, MODEL, MAX_TOKENS

load_dotenv()


def chat(messages: list) -> str:
    message = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=messages
        )
    return message.content[0].text

try:
    messages = []
    turn = 1

    while True:
        query = input('> Please, enter your message: \n')
        append_message(messages, 'user', query)
        response = chat(messages)
        append_message(messages, 'assistant', response)
        print(f'Message: {response}, turn: {turn}')
        turn += 1

except KeyboardInterrupt:
    print('\nControl + C has been pressed. Exiting.')
    exit(0)