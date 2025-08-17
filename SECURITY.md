# Security Policy

## Reporting a Vulnerability

If you discover a security issue, please report it responsibly.

- Email: security@example.com
- Alternatively, open a private issue labeled "security".

We will respond as soon as possible and work to address the issue promptly.

## Secrets

Do not commit API keys or other credentials to the repository. LLM adapters
must read secrets such as `OPENAI_API_KEY` from environment variables or
external secret managers.
