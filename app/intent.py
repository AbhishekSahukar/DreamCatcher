from langchain_core.messages import SystemMessage, HumanMessage
from app.llm import get_llm

def detect_intent(user_text: str) -> str:
    """
    Simple and accurate intent classifier.
    ONLY two intents:
      - dream_description
      - general_chat
    """

    llm = get_llm()

    system = SystemMessage(
        content=(
            "You are an intent classifier. Classify the user message into EXACTLY one intent:\n\n"
            "1. dream_description → The user is describing a sleep dream (something that happened while sleeping). "
            "This includes dream scenes, places, people, animals, feelings, events, nightmares, etc.\n\n"
            "2. general_chat → Greetings, normal conversation, questions, goals, ambitions, hopes, "
            "or anything that is NOT a sleep dream.\n\n"
            "IMPORTANT:\n"
            "- DO NOT mistake goals, future plans, or ambitions for dreams. Only classify dream scenes experienced during sleep as 'dream_description'.\n"
            "- DO NOT classify motivation/aspiration as dreams.\n"
            "- Use only semantic meaning.\n"
            "- Output ONLY the intent name."
        )
    )

    res = llm.invoke([
        system,
        HumanMessage(content=user_text)
    ])

    return res.content.strip()
