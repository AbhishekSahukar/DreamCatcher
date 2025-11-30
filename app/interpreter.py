from langchain_core.messages import HumanMessage, SystemMessage
from app.llm import get_llm
from app.search import search_dream_symbols
from app.intent import detect_intent

def interpret_dream(user_message: str) -> str:

    intent = detect_intent(user_message)

    # ------------------------------------------------------
    # DREAM DESCRIPTION → Interpret immediately
    # ------------------------------------------------------
    if intent == "dream_description":

        symbols = search_dream_symbols(user_message)

        prompt = (
            "You are a gentle dream psychologist who ONLY interprets sleep dreams.\n"
            "Interpret the following sleep dream warmly, symbolically, and supportively.\n"
            "Avoid talking about goals, ambitions, or future desires.\n\n"
            f"Dream:\n{user_message}\n\n"
            f"Symbol meanings from online sources:\n{symbols}\n\n"
            "Give a non-clinical, symbolic interpretation."
        )

        llm = get_llm()
        res = llm.invoke([HumanMessage(content=prompt)])
        return res.content.strip()

    # ------------------------------------------------------
    # GENERAL CHAT → Ask for sleep dream
    # ------------------------------------------------------
    llm = get_llm()

    system = SystemMessage(
        content=(
            "The user is not describing a sleep dream.\n"
            "Respond kindly but invite them to share a dream they saw while sleeping "
            "so you can interpret it."
        )
    )

    res = llm.invoke([system, HumanMessage(content=user_message)])
    return res.content.strip()
