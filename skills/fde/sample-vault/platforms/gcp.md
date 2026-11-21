# GCP defaults

Made-up sample data. Updated 2026-02-02.

Every project uses these unless its `project.md` says otherwise.

## Orgs and projects
| Org | Used for | Sandbox project |
|---|---|---|
| Our company's org | Demos and spikes, no client data | `fde-sandbox-01` |
| The client's own org | Anything that touches client data | One per client, set up by the client |

## Defaults
- Region: `us-central1`.
- Access: the client's org grants us roles on its project. Internal apps sit behind IAP, and Domain Restricted Sharing blocks sharing with accounts outside the client's domain.
- Models: Gemini on Vertex AI in every project, called with the runtime service account. No key to store.

## What agents cannot do
- Change DNS or certificates.
- Write to Secret Manager. They may check that a secret exists by name, never read its value.
- Grant IAM roles. The client's admin does that.
