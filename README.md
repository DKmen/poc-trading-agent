LangGraph project - quick setup

This project uses Python. These instructions assume macOS with zsh (your default shell).

Checklist
- [ ] Create and activate a virtual environment
- [ ] Install dependencies from `requirements.txt`
- [ ] Fill `.env` with your API keys (OpenAI, LangGraph)
- [ ] (Optional) Run a local LangGraph instance or connect to hosted service

1) Create & activate venv (zsh)

```zsh
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

2) Fill `.env`

Open the `.env` file at the repo root and set `OPENAI_API_KEY`, `LANGGRAPH_API_KEY`, and `LANGGRAPH_API_URL` (if using hosted LangGraph).

3) Running a local LangGraph dev server

If you want to run LangGraph locally, follow the official LangGraph instructions. If there's a Docker image, a typical flow is:

```zsh
# Example only - replace with LangGraph official commands
docker pull langgraph/langgraph:latest
docker run -p 8080:8080 -e LANGGRAPH_API_KEY=your_key langgraph/langgraph:latest
```

4) Using LangGraph via HTTP API from Python

Example pattern (requests):

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv('LANGGRAPH_API_URL')
API_KEY = os.getenv('LANGGRAPH_API_KEY')

resp = requests.post(
    f"{API_URL}/v1/run",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={"input":"Hello"},
)
print(resp.json())
```

5) Helpful commands

```zsh
# format, lint, run tests (if present)
# Example: run main
python main.py
```

Notes
- If you know the exact LangGraph SDK package name, add it to `requirements.txt` and run `pip install -r requirements.txt`.
- Keep secrets out of Git. Use environment variables or a secrets manager for production.

If you want, I can:
- Add a minimal `src/langgraph_client.py` wrapper to call LangGraph
- Add a small example FastAPI endpoint that proxies requests to LangGraph
- Add tests and a GitHub Actions workflow to run them

Tell me which of the above you'd like me to implement next.
