from langchain_core.messages import HumanMessage
from app.llm import get_llm
from app.search import search_dream_symbols

def interpret_dream(user_dream: str) -> str:

    search_context = search_dream_symbols(user_dream)

    prompt = (
        "You are a gentle AI dream psychologist who has intense and huge information gathered about dreams.\n\n"
        f"The user described this dream:\n\n{user_dream}\n\n"
        f"Here are some symbolic interpretations from online sources:\n\n{search_context}\n\n"
        "Based on the dream and the symbols, give a thoughtful, non-clinical interpretation. "
        "Use symbolic language, avoid diagnosing, and keep it warm and supportive."
    )

    llm = get_llm()
    response = llm.invoke([HumanMessage(content=prompt)])

    return response.content.strip()