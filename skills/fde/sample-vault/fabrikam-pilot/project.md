# Fabrikam pilot: facts

Updated 2026-02-27. Made-up sample data.

## Workstreams
| Workstream | Done when | Estimate | As of | Basis |
|---|---|---|---|---|
| Reorder drafts | Drafts pass review on test data | 70% | 2026-02-27 | Demo passed 2/27 |
| Stock-count sync | Counts match the test warehouse nightly | 30% | 2026-02-27 | Schema agreed 2/20 |

## Code
| Repo | Default branch | Local clone | Merge owner |
|---|---|---|---|
| fabrikam/inventory-agent (GitHub) | `main` @ `5c3e9b1`, 2026-02-26 | `~/code/inventory-agent` | Lead FDE |

## Deployment
| Env | Cloud | Project or account | Region | Services | URL | Live revision |
|---|---|---|---|---|---|---|
| dev | GCP | `fabrikam-inventory-dev` | `us-central1` | Cloud Run `inventory-agent` | [app](https://inventory-agent.example.com) | `inventory-agent-00007`, image `5c3e9b1` |

## Platform overrides
None: the defaults in [../platforms/gcp.md](../platforms/gcp.md).

## Dependencies
| What | Where the key lives | Notes |
|---|---|---|
| Gemini on Vertex | No key: the runtime service account | |

## Access
| Source | Method last used | Notes |
|---|---|---|
| Teams | skipped | The client uses email only |
| Email | screenshots | |
| Transcripts | pasted in | |

## People
| Name | Role | Side |
|---|---|---|
| Ari | Lead FDE | Us |
| Jo | Warehouse lead | Client |

## Data rules
None beyond the defaults.

## Story
None.
