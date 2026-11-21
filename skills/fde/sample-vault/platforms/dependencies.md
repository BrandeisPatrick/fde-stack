# Shared dependencies

Made-up sample data. Updated 2026-02-02.

| What | Base URL | Where the key lives | Known traps |
|---|---|---|---|
| Gemini on Vertex AI | the project's Vertex endpoint | No key: the runtime service account | Quota is per project; a new project starts low |
| Model gateway | `https://gateway.example.com/v1` | Secret Manager `model-gateway-key` in `fde-sandbox-01` | Sandbox only, never for client data |
| Docs search MCP server | `https://mcp.example.com/docs` | No key | Read-only; returns public docs only |

Never write a key, token or password here. Record where it lives and who can grant it.
