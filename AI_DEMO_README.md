# AI-Powered DevOps Agent — Demo Guide

This document explains **what the AI agent does**, **how it works**, and **how to demo it** to a leadership audience.

---

## What Problem Are We Solving?

In a traditional SDLC, DevOps setup is manual and reactive:
- Engineers write CI/CD pipelines by hand after code is already written
- Infrastructure is configured separately from the application
- Post-merge issues (missing tests, misconfigured ports, no Dockerfiles) are caught late or not at all

This demo shows an AI agent that **watches your codebase, understands it, and acts on it automatically** — without a human writing a single pipeline file.

---

## The Agent: What It Is

The agent is `generate_workflow.py` — a Python script that acts as an autonomous DevOps engineer. It is triggered by GitHub Actions and operates in two modes:

| Mode | Flag | What it does |
|------|------|-------------|
| Analysis | `--analyze-only` | Reads the codebase, detects stack, ports, frameworks, infra |
| Suggestion | `--suggest-changes` | Writes a `suggestions.md` report with prioritized findings |
| Generation | _(default)_ | Generates GitHub Actions workflows, Terraform, Docker configs |

When an OpenAI API token is present (`OPENAI_API_TOKEN` secret), the agent upgrades from rule-based analysis to **LLM-powered recommendations** — asking GPT to reason about the specific tech stack and suggest pipeline optimizations, security hardening, and deployment strategies.

---

## The Demo Flow

This is the exact sequence to walk through with leadership:

### Step 1 — Show the running app
```bash
docker-compose up -d
# Open http://localhost:3000 — QR code generator is live
```
Point: this is a real full-stack app (FastAPI backend + vanilla JS frontend) deployed via Docker Compose.

### Step 2 — Show the intent file
Open `pipeline_request.txt`. This is the only human input the agent needs:
```
pipeline_name: qr-generator-auto-pipeline
environment: production
target: aws_ec2
instance_type: t2.micro
deploy_using: docker-compose
```
Point: a developer describes *what they want*, not *how to build it*.

### Step 3 — Show the agent analyzing the codebase
```bash
python generate_workflow.py --analyze-only --verbose
```
The agent scans the repo and outputs:
- Detected framework: FastAPI (Python)
- Detected frontend: Vanilla JS
- Ports: backend 8000, frontend 3000
- Terraform: exists ✅
- Dockerfiles: found ✅

Point: the agent reads code the same way a senior engineer would during an onboarding review.

### Step 4 — Trigger the full loop via a PR merge

Make a small code change (e.g., add a comment to `backend/main.py`), open a PR, and merge it into `main`.

GitHub Actions automatically triggers `ai-generate-workflow.yml`:

```
PR merged into main
        ↓
GitHub Actions: ai-generate-workflow.yml fires
        ↓
Agent runs --analyze-only  →  logs full analysis
        ↓
Agent runs --suggest-changes  →  writes suggestions.md
        ↓
If suggestions exist: new branch created, new PR opened automatically
        ↓
PR title: "AI Suggestions: Post-merge analysis of PR #N"
```

### Step 5 — Show the AI-generated PR

Open the PR that the agent created. The PR body is the `suggestions.md` report:
- Prioritized issues (High / Medium / Low)
- Specific file-level fixes
- If OpenAI is enabled: LLM-generated recommendations for the exact stack

Point: a human developer reviews and merges AI suggestions — the agent proposes, the human approves.

---

## What the Agent Can Detect (Rule-Based)

These run without any API key:

- Missing `Dockerfile` for frontend or backend
- Missing `docker-compose.yml`
- No test file (`test_main.py`) when pytest is configured in CI
- Missing Terraform configuration
- Missing `requirements-dev.txt` (linting tools not declared)

---

## What the Agent Can Recommend (AI-Enhanced)

When `OPENAI_API_TOKEN` is set in GitHub Secrets, the agent calls GPT-3.5-turbo with the full project analysis as context and asks for:

1. Optimal CI/CD pipeline stages for this specific stack
2. Testing strategies (what to test, how to structure it)
3. Deployment recommendations (instance sizing, health checks)
4. Security considerations (secrets handling, network exposure)
5. Performance optimization suggestions

The LLM response is included verbatim in the `suggestions.md` PR body.

---

## Key AI Concepts Being Demonstrated

| Concept | How it shows up in this demo |
|---------|------------------------------|
| **Autonomous code analysis** | Agent reads and understands the repo without being told what's in it |
| **Context-aware generation** | Terraform, Docker, and workflow files are generated based on what the agent found, not from a template |
| **Event-driven AI action** | Agent fires on a real GitHub event (PR merge), not a manual trigger |
| **Human-in-the-loop** | Agent opens a PR — a human still reviews and approves before anything merges |
| **Graceful degradation** | Works without OpenAI (rule-based), upgrades with it (LLM reasoning) |
| **Structured output** | Agent produces `suggestions.md` — a machine-readable, human-readable artifact that becomes the PR body |

---

## GitHub Secrets Required

| Secret | Required | Purpose |
|--------|----------|---------|
| `AWS_ACCESS_KEY_ID` | For deployment | Terraform AWS access |
| `AWS_SECRET_ACCESS_KEY` | For deployment | Terraform AWS access |
| `OPENAI_API_TOKEN` | Optional | Enables LLM-enhanced suggestions |

---

## Files Involved in the AI Loop

```
generate_workflow.py          ← the agent
pipeline_request.txt          ← human intent input
.github/workflows/
  ai-generate-workflow.yml    ← triggers agent on PR merge
  ci-cd.yml                   ← generated by agent, runs tests + deploys
suggestions.md                ← agent output, becomes PR body (auto-deleted after PR)
```

---

## What This Is NOT

- This is not a chatbot. The agent does not wait for prompts — it acts on events.
- This is not a code generator that replaces developers. It surfaces issues and proposes changes; humans approve.
- This is not locked to OpenAI. The rule-based analysis works standalone; the LLM layer is additive.
