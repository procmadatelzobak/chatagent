
import httpx, json, math, time
from typing import List, Dict, Any, Optional
from ..settings import settings

GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta"

class GoogleProvider:
    def __init__(self, model: str | None = None):
        self.model = model or settings.google_model_chat
        self.api_key = settings.google_api_key

    def _headers(self):
        return {"x-goog-api-key": self.api_key}

    async def chat(self, messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]] = None, system: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
        """Minimal wrapper for Gemini chat with tool calling (function calling)."""
        mdl = model or self.model
        url = f"{GEMINI_BASE}/models/{mdl}:generateContent?key={self.api_key}"
        contents = []
        if system:
            contents.append({"role":"user","parts":[{"text": f"[SYSTEM]\n{system}"}]})
        for m in messages:
            role = "user" if m["role"]=="user" else "model"
            contents.append({"role": role, "parts":[{"text": m["content"]}]})
        tool_config = {"function_declarations": tools} if tools else None
        payload = {"contents": contents}
        if tool_config:
            payload["tools"] = [ {"function_declarations": tools} ]
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            data = r.json()
        return data

    async def embed(self, texts: List[str], model: Optional[str] = None) -> List[List[float]]:
        mdl = model or settings.google_model_embed
        url = f"{GEMINI_BASE}/models/{mdl}:batchEmbedContents?key={self.api_key}"
        req = {"requests": [{"model": mdl, "content": {"parts":[{"text": t}]}} for t in texts]}
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(url, json=req)
            r.raise_for_status()
            data = r.json()
        return [item["embeddings"][0]["values"] for item in data["responses"]]
