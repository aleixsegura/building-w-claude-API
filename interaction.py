from config import client, MODEL, MAX_TOKENS

def append_message(messages: list, role: str, text: str) -> None:
    message = {
        'role': role,
        'content': text
    }
    messages.append(message)


def chat(messages: list, *, system: str | None = None, temperature: float = 0.0, stop_sequences: list[str] = []):
    params = {
        'model': MODEL,
        'max_tokens': MAX_TOKENS,
        'messages': messages,
        'temperature': temperature
    }

    if system:
        params['system'] = system
    if stop_sequences:
        params['stop_sequences'] = stop_sequences

    response = client.messages.create(**params)

    return response.content[0].text