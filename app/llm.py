import os
from langchain_openai import ChatOpenAI


def get_llm():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is not set. Check your .env file.")

    return ChatOpenAI(
        openai_api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        model="minimax/minimax-m2.5",
        temperature=float(os.getenv("OPENROUTER_TEMPERATURE", "0.7")),
    )