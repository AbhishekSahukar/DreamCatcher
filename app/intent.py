from langchain_core.messages import HumanMessage
from app.llm import get_llm


def is_dream(user_input: str) -> bool:
    llm = get_llm()

    prompt = (
        "Your only job is to decide if the user's message describes a dream they had while sleeping.\n"
        "Reply with only YES or NO. Nothing else.\n\n"
        "Examples:\n"
        "- 'I was flying over mountains' → YES\n"
        "- 'I saw my dead grandmother in a forest' → YES\n"
        "- 'hi' → NO\n"
        "- 'what is the weather' → NO\n"
        "- 'I dreamed I was being chased' → YES\n"
        "- 'tell me a joke' → NO\n\n"
        f"User message: {user_input}\n"
        "Answer (YES or NO):"
    )

    response = llm.invoke([HumanMessage(content=prompt)])
    answer = response.content.strip().upper()
    return answer.startswith("YES")