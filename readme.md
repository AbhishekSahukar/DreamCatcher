# DreamCatcher 🌙

An AI-powered dream interpretation chatbot that analyzes your dreams in real time. Describe what you dreamed, and DreamCatcher searches the web for symbolic meanings and returns a warm, thoughtful interpretation — no static datasets, no canned responses.

![Chat Interface](./assets/Chat.png)


![Example](./assets/Example.png)

---

## How it works

1. You describe your dream in the chat.
2. The backend searches the web via the **Tavily API** to find current symbolic meanings related to your dream.
3. Those results are passed to an LLM (**minimax-m2.5** via OpenRouter) along with a carefully crafted prompt.
4. The model returns a human, non-clinical interpretation that you see in the chat.

---

## Tech stack

| Layer    | Technology                         |
|----------|------------------------------------|
| Frontend | React + Vite                       |
| Backend  | FastAPI                            |
| Search   | Tavily Web Search API              |
| LLM      | minimax-m2.5 via Openrouter        |
| Styling  | CSS3 with glassmorphism            |

---

## Getting started

### Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- A [Tavily API key](https://tavily.com) (free tier available)
- An [OpenRouter API key](https://openrouter.ai) (free credits on signup)

---

### 1. Clone the repository

```bash
git clone https://github.com/AbhishekSahukar/DreamCatcher.git
cd DreamCatcher
```

---

### 2. Set up the backend

**Create your environment file:**

```bash
cp .env.example .env
```

Open `.env` and fill in your API keys:

```
TAVILY_API_KEY=your_tavily_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_TEMPERATURE=0.7
```

**Install dependencies and start the server:**

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will be running at `http://localhost:8000`. You can verify it by visiting that URL — you should see `{"status": "DreamCatcher API is running"}`.

---

### 3. Set up the frontend

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

The app will be running at `http://localhost:5173`.


## Project structure

```
DreamCatcher/
├── app/
│   ├── main.py          # FastAPI app, routes
│   ├── interpreter.py   # Orchestrates search + LLM
│   ├── llm.py           # OpenRouter / LangChain setup
│   └── search.py        # Tavily web search
├── frontend/
│   └── src/
│       ├── components/
│       │   └── DreamForm.jsx   # Chat UI
│       ├── App.jsx
│       ├── App.css
│       └── index.css
├── .env.example
├── requirements.txt
└── readme.md
```

---

## License

MIT — free to use, fork, or build upon.

## Author

Built by [Abhishek Sahukar Srinivas](https://github.com/AbhishekSahukar)
