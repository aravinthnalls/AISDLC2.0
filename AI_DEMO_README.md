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

### Step 4 — Open a PR and watch the AI analyze it

Make a small code change (e.g., add a comment to `backend/main.py`), commit, push, and open a PR to `main`.

**Stage 1: AI Analysis on PR Open**

GitHub Actions automatically triggers `ai-generate-workflow.yml`:

```
PR opened
        ↓
GitHub Actions: analyze-and-comment job fires
        ↓
Agent analyzes the PR branch
        ↓
Agent runs --analyze-only  →  detects issues
        ↓
Agent runs --suggest-changes  →  generates suggestions.md
        ↓
Bot posts analysis as a PR comment with:
  • High/Medium/Low priority issues
  • Specific recommendations
  • LLM insights (if OpenAI enabled)
```

Point: Developers see potential issues **before merging** — early feedback loop.

### Step 5 — Merge the PR and watch AI create a fix PR

After reviewing the AI comment, merge the PR into `main`.

**Stage 2: Automated Fix PR on Merge**

```
PR merged into main
        ↓
GitHub Actions: create-fix-pr job fires
        ↓
Agent re-analyzes the main branch
        ↓
If issues remain: creates new branch + PR with fixes
        ↓
PR title: "🤖 AI Suggestions: Post-merge fixes for PR #N"
```

Point: a human developer reviews and merges AI suggestions — the agent proposes, the human approves.

### Step 6 — Show both PRs

**Original PR**: Shows AI comment with analysis findings
**AI-generated PR**: Contains actual code fixes and detailed explanation

This demonstrates the two-stage approach:
1. Early warning (comment on original PR)
2. Automated remediation (new PR with fixes)

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

When `OPENAI_API_TOKEN` is set in GitHub Secrets, the agent calls GPT-4o-mini (OpenAI's most cost-effective model) with the full project analysis as context and asks for:

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
| **Event-driven AI action** | Agent fires on real GitHub events (PR open **and** PR merge), not manual triggers |
| **Shift-left testing** | Issues detected and surfaced as PR comments **before** merge — early feedback prevents bugs |
| **Multi-stage automation** | Stage 1: analyze & comment on PR; Stage 2: auto-generate fixes after merge |
| **Human-in-the-loop** | Agent comments on PRs and opens fix PRs — humans review and approve all changes |
| **Graceful degradation** | Works without OpenAI (rule-based), upgrades with it (LLM reasoning) |
| **Structured output** | Agent produces `suggestions.md` — a machine-readable, human-readable artifact used in comments and PRs |

---

## GitHub Secrets Required

| Secret | Required | Purpose |
|--------|----------|---------|
| `PAT_TOKEN` | **Yes** | Personal Access Token for creating PRs and posting comments |
| `AWS_ACCESS_KEY_ID` | For deployment | Terraform AWS access |
| `AWS_SECRET_ACCESS_KEY` | For deployment | Terraform AWS access |
| `OPENAI_API_TOKEN` | Optional | Enables LLM-enhanced suggestions |

**Note**: `PAT_TOKEN` must be a GitHub Personal Access Token with `repo` and `workflow` scopes. The default `GITHUB_TOKEN` cannot create PRs.

---

## Files Involved in the AI Loop

```
generate_workflow.py          ← the agent
pipeline_request.txt          ← human intent input
.github/workflows/
  ai-generate-workflow.yml    ← triggers agent on PR open AND PR merge (two stages)
  ci-cd.yml                   ← generated by agent, runs tests + deploys
suggestions.md                ← agent output, posted as PR comment + fix PR body
analysis_output.txt           ← detailed analysis logs
```

---

## What This Is NOT

- This is not a chatbot. The agent does not wait for prompts — it acts on events.
- This is not a code generator that replaces developers. It surfaces issues and proposes changes; humans approve.
- This is not locked to OpenAI. The rule-based analysis works standalone; the LLM layer is additive.
