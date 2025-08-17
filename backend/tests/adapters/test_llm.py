import asyncio

import pytest

from adapters.llm import MockLLM, OpenAILLM


def test_mock_llm_returns_response():
    llm = MockLLM(response="hi")
    assert asyncio.run(llm.predict("hello")) == "hi"


def test_openai_requires_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        OpenAILLM()


def test_openai_predict_not_implemented(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "x")
    llm = OpenAILLM()
    with pytest.raises(NotImplementedError):
        asyncio.run(llm.predict("hello"))
