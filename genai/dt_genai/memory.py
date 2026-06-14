# dt_genai/memory.py

conversation_memory = []


def add_to_memory(role, content):

    conversation_memory.append({
        "role": role,
        "content": content
    })

    # Keep last 10 messages
    if len(conversation_memory) > 10:
        conversation_memory.pop(0)


def get_memory():

    return conversation_memory


def clear_memory():

    conversation_memory.clear()