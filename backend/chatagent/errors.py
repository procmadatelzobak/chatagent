"""Custom error types for ChatAgent."""


class ChatAgentError(Exception):
    """Base error for ChatAgent."""


class ConfigError(ChatAgentError):
    """Raised when configuration is invalid."""


class ProviderError(ChatAgentError):
    """Raised when an LLM provider fails or is misconfigured."""
