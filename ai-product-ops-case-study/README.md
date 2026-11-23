# Agent Toolkit Landscape - take-home case study

This folder is a self-contained submission for the AI Product Ops Intern take-home.

## Open the case study

Serve the folder with `python -m http.server` and open `http://localhost:8000`. It is deliberately dependency-free, so it can also be deployed as a static site (GitHub Pages, Netlify, Vercel, etc.). The page contains the complete 100-app matrix, filters, source links, research workflow, and a transparent verification sample.

## Run the research pipeline

```powershell
cd ai-product-ops-case-study
python research_agent.py --check-links
python verify.py
```

`research_agent.py` is a reproducible research harness. It reads the seeded research set in `data/apps.json`, checks every official evidence URL, and writes a timestamped evidence-status report to `output/`. It intentionally does **not** silently infer a conclusion when a source is unavailable. Records needing a fresh judgement are emitted to a review queue.

For a production version, the `enrich` stage is where a browser/LLM worker would extract the auth, access, API, and MCP claims from the official documentation. The model output must be returned as structured JSON with source excerpts; the deterministic rules in the script then reject claims without an official URL or an explicit uncertainty flag. This small version keeps the researched seed data inspectable and runnable without requiring an API key.

## Method notes

- **As-of date:** 23 November 2026.
- **Evidence standard:** first-party developer docs, product documentation, or official repositories only.
- **Self-serve:** a developer can create credentials in a free/trial developer account. “Gated” includes partner-only, enterprise-only, sales-contact, or admin-provisioned routes.
- **MCP:** “Yes” means an official/maintained MCP or explicitly supported server was found; “Community” means a third-party/community server; “No” means none was found in the reviewed official docs. It is not a claim that no implementation exists anywhere.
- **Buildable now:** credentials and a documented API are sufficient for a useful initial toolkit. “Conditional” means a legitimate integration can be built but account/admin/approval friction is material. “No” means the public API surface is absent or materially unsuitable.

The verification numbers on the page are a deliberately small, manual spot-check sample rather than a claim of perfect ground truth. See `data/verification_sample.json` for every adjudication.
