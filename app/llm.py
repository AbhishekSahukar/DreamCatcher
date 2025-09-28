import os
from langchain_openai import ChatOpenAI


def get_llm():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is not set in environment")

    return ChatOpenAI(
        openai_api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        model="mistralai/mixtral-8x7b-instruct",  # or any supported model
        temperature=float(os.getenv("OPENROUTER_TEMPERATURE", "0.7")),
    )
