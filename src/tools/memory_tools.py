from src.memory.storage import MemoryManager

# Note: In a real multi-user scenario, we need a way to pass the current user_id 
# to these tools implicitly or explicitly. For now, since the Agent loop is 
# stateless regarding the tool definitions, we might need to rely on the 
# prompt context or pass user_id as an argument. 
# 
# However, `tool_registry` registers static functions. 
# A common pattern is to having the LLM generate the tool call WITH the user_id 
# if it knows it. But simpler is to have a "Context" variabled set during execution.
#
# For simplicity in this milestone, we will assume a single-user local context 
# or that the LLM is instructed to pass 'me' or we retrieve it from a global context var.
#
# Let's try ContextVar for handling the "current user" within the async execution flow.

import contextvars

current_user_id = contextvars.ContextVar("current_user_id", default="default_user")

def set_current_user(user_id: str):
    current_user_id.set(user_id)

def remember(key: str, value: str) -> str:
    """Remembers a user preference or fact. Key should be a short identifier."""
    user = current_user_id.get()
    storage = MemoryManager.get_instance()
    storage.set_pref(user, key, value)
    return f"I have remembered that {key} is {value}."

def recall(key: str) -> str:
    """Recalls a previously stored user preference or fact."""
    user = current_user_id.get()
    storage = MemoryManager.get_instance()
    val = storage.get_pref(user, key)
    if val:
        return f"{key} is {val}."
    else:
        return f"I don't have any memory of {key}."
