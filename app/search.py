import os
from tavily import TavilyClient


def search_dream_symbols(dream_text: str, num_results: int = 3) -> str:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY is not set. Check your .env file.")

    client = TavilyClient(api_key=api_key)
    query = f"What does it mean when you dream about: {dream_text}?"
    results = client.search(query=query, search_depth="advanced", max_results=num_results)

    context = ""
    for idx, res in enumerate(results["results"], 1):
        context += f"[{idx}] {res['content']}\n"

    return context.strip()