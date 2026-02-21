import httpx
from app.config import settings
from pathlib import Path

PROMPT = Path("app/prompts/grounded_answer.md").read_text(encoding="utf-8")

def build_sources(passages: list[dict]) -> str:
    blocks = []
    for p in passages:
        tag = f'[{p["doc_id"]}:p{p["page"]}#{p["chunk_id"]}]'
        blocks.append(f"{tag}\n{p['text']}\n")
    return "\n---\n".join(blocks)

async def generate(question: str, passages: list[dict]) -> str:
    sources = build_sources(passages)
    prompt = PROMPT.replace("{{question}}", question).replace("{{sources}}", sources)

    headers = {"Authorization": f"Bearer {settings.llm_api_key}"}
    payload = {
        "model": settings.llm_model,
        "messages": [
            {"role": "system", "content": "You follow the rules strictly."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
        "max_tokens": 600
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(f"{settings.llm_base_url}/chat/completions", json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]