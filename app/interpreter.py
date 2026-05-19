from typing import Generator
from langchain_core.messages import HumanMessage
from app.llm import get_llm
from app.search import search_dream_symbols


def stream_interpret_dream(user_dream: str) -> Generator[str, None, None]:
    search_context = search_dream_symbols(user_dream)

    prompt = (
        "You are DreamCatcher, a warm and gentle AI dream interpreter.\n\n"
        "First, decide if the user's message describes a dream they had while sleeping.\n\n"
        "If it is NOT a dream (e.g. greetings, questions, random text), respond only with:\n"
        "'I can only interpret dreams. Try describing something you experienced while sleeping, "
        "like: I was flying over a city, or I dreamed I was being chased.'\n\n"
        "If it IS a dream, give a thoughtful, symbolic, and warm interpretation based on the dream "
        "and the following context from online sources:\n\n"
        f"{search_context}\n\n"
        "Avoid clinical language. Be supportive and use symbolic meaning.\n\n"
        f"User message: {user_dream}"
    )

    llm = get_llm()
    for chunk in llm.stream([HumanMessage(content=prompt)]):
        if chunk.content:
            yield chunk.content