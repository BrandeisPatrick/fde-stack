# Contoso Retail: facts

Updated 2026-03-06. Made-up sample data.

## Workstreams
The progress bars in the status message read from this table and write back to it. Keep the same rows from session to session, and add a row only when new work starts.
| Workstream | Done when | Estimate | As of | Basis |
|---|---|---|---|---|
| SOW | Signed by both sides | 80% | 2026-03-06 | With legal since 3/5 |
| Scope | Phase 1 features agreed in writing | 50% | 2026-03-06 | Returns added 3/3 |
| Access | Client VPN, GitHub and GCP work for both FDEs | 20% | 2026-03-06 | VPN pending |
| First build | The assistant answers order-status questions on the dev deploy | 10% | 2026-03-06 | Chat skeleton live 3/4 |

## Code
| Repo | Default branch | Local clone | Merge owner |
|---|---|---|---|
| contoso/assistant (GitHub) | `main` @ `a1c4e02`, 2026-03-06 | `~/code/assistant`, agent worktrees in `wt/` | Lead FDE |
| Client GitLab, the client's own repo | not known yet | none: needs the client VPN | Client |

## Deployment
| Env | Cloud | Project or account | Region | Services | URL | Live revision |
|---|---|---|---|---|---|---|
| dev | GCP | `contoso-assistant-dev` | `us-central1` | Cloud Run `assistant-web` | [app](https://assistant-web.example.com) | `assistant-web-00012`, image `7d91b3f`, deployed 2026-03-04 |

## Platform overrides
Only where this project differs from [../platforms/gcp.md](../platforms/gcp.md).

- The project lives in the client's own org, not in our sandbox.
- No model gateway: the client's terms allow Vertex in their project only.

## Dependencies
| What | Where the key lives | Notes |
|---|---|---|
| Gemini on Vertex | No key: the runtime service account `assistant-runtime` | Calls stay in `contoso-assistant-dev` |
| Order-status API, client test system | Secret Manager `order-api-test-key` in `contoso-assistant-dev` | Synthetic orders only |

## Access
| Source | Method last used | Notes |
|---|---|---|
| Teams | screenshots | Project core chat |
| Email | screenshots | |
| Transcripts | pasted in | The 3/3 scope call was not recorded |

## People
| Name | Role | Side |
|---|---|---|
| Dana | Lead FDE | Us |
| Sam | Client PM | Client |

## Data rules
No client data outside the client's cloud. Build and test with synthetic orders only.

## Story
None yet. Propose one when the build starts.
