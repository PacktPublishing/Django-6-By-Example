from django.conf import settings
from google import genai
from google.genai import types

from .catalog import TOOLS


def generate_reply(history):
    """Return the model's answer to a conversation history ending with the user's message.

    The SDK runs the catalog functions the model asks for and sends their results
    back to it, until the model writes its answer.

    Raises google.genai.errors.APIError when the API call fails.
    """
    *previous, last = history
    # Retry briefly when Gemini is overloaded (429, 503...) before giving up.
    client = genai.Client(
        api_key=settings.GEMINI_API_KEY,
        http_options=types.HttpOptions(retry_options=types.HttpRetryOptions(attempts=3)),
    )
    chat = client.chats.create(
        model=settings.GEMINI_MODEL,
        config=types.GenerateContentConfig(system_instruction=settings.ASSISTANT_SYSTEM_PROMPT, tools=TOOLS),
        history=[types.Content(role=message.role, parts=[types.Part(text=message.text)]) for message in previous],
    )
    response = chat.send_message(last.text)
    return response.text or ""
