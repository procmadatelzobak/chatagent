import httpx

from ..settings import settings

GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta"


class GoogleProvider:
    def __init__(self, model: str | None = None):
        self.model = model or settings.model_default
        self.api_key = settings.google_api_key

    async def chat(
        self, messages: list[dict], tools=None, system: str | None = None
    ) -> dict:
        if not self.api_key:
            text = "(stub)"
            if messages:
                text += " " + messages[-1].get("content", "")
            return {"candidates": [{"content": text}]}
        url = f"{GEMINI_BASE}/models/{self.model}:generateContent?key={self.api_key}"
        contents = []
        if system:
            contents.append({"role": "user", "parts": [{"text": system}]})
        for m in messages:
            role = "user" if m.get("role") == "user" else "model"
            contents.append({"role": role, "parts": [{"text": m.get("content", "")}]})
        payload = {"contents": contents}
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            data = r.json()
        # Flatten Gemini response to simple candidates list
        if "candidates" in data and data["candidates"]:
            cand = data["candidates"][0]
            if "content" in cand and isinstance(cand["content"], dict):
                parts = cand["content"].get("parts", [])
                text = parts[0].get("text", "") if parts else ""
            else:
                text = cand.get("content", "")
            return {"candidates": [{"content": text}]}
        # Fallback OpenAI-like
        choice = data.get("choices", [{}])[0]
        msg = choice.get("message", {})
        return {"candidates": [{"content": msg.get("content", "")}]}
