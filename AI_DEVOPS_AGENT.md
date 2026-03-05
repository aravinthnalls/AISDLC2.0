# AI DevOps Agent

`ai_devops_agent.py` — an autonomous AI agent that scans a codebase, enriches every finding with GPT-4o-mini intelligence, generates all CI/CD and infrastructure files, and opens a fix PR automatically after every merge.

> **OpenAI API token is mandatory.** The agent will not start without one. Provide it via `--openai-token` or the `OPENAI_API_TOKEN` environment variable.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         AI DevOps Agent                          │
│                      ai_devops_agent.py                          │
│                                                                  │
│  ┌──────────────────────┐        ┌──────────────────────────┐   │
│  │    CodeAnalyzer      │──────▶ │    PipelineGenerator     │   │
│  │                      │        │                          │   │
│  │ • Frontend scan      │        │ • GitHub Actions CI/CD   │   │
│  │ • Backend scan       │        │ • Terraform (IaC)        │   │
│  │ • Infra scan         │        │ • variables.tf / tfvars  │   │
│  │ • Security scan      │        │ • suggestions.md report  │   │
│  │ • Best practices     │        │ • Dockerfile fixes       │   │
│  │      │               │        │        │                 │   │
│  │      ▼               │        │        ▼                 │   │
│  │ AI Security Enrich   │        │ AI Pipeline & Infra Recs │   │
│  │ (CVEs, exploits,     │        │ (stages, deployment,     │   │
│  │  top 3 actions)      │        │  optimisations, perf)    │   │
│  │      │               │        │        │                 │   │
│  │      ▼               │        │        ▼                 │   │
│  │ AI Best Practices    │        │   File System Writes     │   │
│  │ (maturity, quick     │        │                          │   │
│  │  wins, effort/impact)│        │ .github/workflows/       │   │
│  └──────────────────────┘        │ terraform/               │   │
│           │                      │ frontend/Dockerfile      │   │
│           ▼                      │ backend/Dockerfile       │   │
│  ┌──────────────────────┐        │ suggestions.md           │   │
│  │   OpenAI gpt-4o-mini │        └──────────────────────────┘   │
│  │   (REQUIRED)         │                                        │
│  │                      │                                        │
│  │  3 calls per run:    │                                        │
│  │  1. Security enrich  │                                        │
│  │  2. BP enrich        │                                        │
│  │  3. Pipeline recs    │                                        │
│  └──────────────────────┘                                        │
└──────────────────────────────────────────────────────────────────┘
```

### GitHub Actions Integration

```
Developer opens PR
        │
        ▼
[ai-generate-workflow.yml]
        │
        ├── analyze-and-comment job (PR open/update)
        │       │
        │       ├── python ai_devops_agent.py --analyze-only
        │       ├── python ai_devops_agent.py --suggest-changes
        │       └── Posts AI-enriched suggestions.md as PR comment
        │
        └── create-fix-pr job (PR merged)
                │
                ├── python ai_devops_agent.py          ← full generation
                ├── python ai_devops_agent.py --suggest-changes
                ├── python ai_devops_agent.py --apply-fixes
                ├── git add -A && git diff --cached
                └── Opens "AI Suggestions" PR with all changes
```

---

## What the Agent Does

### 1. Code Analysis (`CodeAnalyzer`)
- Detects frontend framework (vanilla-js, Node.js) and port
- Detects backend language/framework (FastAPI, Flask, Django) and port
- Reads `requirements.txt`, `package.json`, Dockerfiles
- Inspects git branch and remote URL

### 2. AI-Enriched Security Scanning
Static checks are run first, then every finding is sent to GPT-4o-mini for enrichment:

| Layer | Static Checks | AI Enrichment |
|---|---|---|
| Frontend | `eval()`, `innerHTML` XSS, hard-coded credentials, missing `package-lock.json` | CVE references, exploit scenario, priority fix |
| Backend | SQL injection, hard-coded secrets, `pickle`, debug mode, missing CORS | CVE references, exploit scenario, priority fix |
| Infrastructure | Root containers, `:latest` tags, `.env` committed | Attack surface summary, top 3 immediate actions |

Risk levels: `HIGH` / `MEDIUM` / `LOW`

### 3. AI-Enriched Best Practices Scoring
Static compliance checks (0–100%) are enriched by AI with:
- **Maturity level**: Beginner / Intermediate / Advanced
- **Quick wins**: immediately actionable improvements
- **Prioritised recommendations**: each with effort (Low/Medium/High), impact (Low/Medium/High), and concrete steps

### 4. Infrastructure Generation (`PipelineGenerator`)
After AI pipeline recommendations are generated, the agent writes or updates:
- `.github/workflows/ci-cd.yml` — validate → test → deploy pipeline
- `.github/workflows/ai-generate-workflow.yml` — the agent's own trigger workflow
- `terraform/main.tf` — EC2, security group, Elastic IP
- `terraform/variables.tf` — driven by `pipeline_request.txt`
- `terraform/outputs.tf` — includes `public_ip` and `application_urls` for CI
- `terraform/terraform.tfvars` — synced from `pipeline_request.txt` on every run
- `terraform/user_data.sh` — EC2 bootstrap script

### 5. Infra Fix Application (`apply_infra_fixes`)
Directly patches files based on security findings:

| Finding | Fix Applied |
|---|---|
| Container runs as root | Adds `USER nginx` / `USER appuser` + `adduser` to Dockerfile |
| `:latest` image tag | Replaces with pinned version (`nginx:1.25-alpine`, `python:3.11-slim`, etc.) |

### 6. AI-Enriched Suggestions Report (`suggest_changes`)
Writes `suggestions.md` with six sections:
1. 🔒 Security Vulnerabilities (sorted HIGH → MEDIUM → LOW)
2. 🤖 AI Security Analysis (CVEs, exploit scenarios, top 3 actions)
3. 🔧 Structural Issues
4. 📋 Best Practices Recommendations
5. 🤖 AI Best Practices Insights (maturity, quick wins, effort/impact matrix)
6. 🤖 AI Pipeline & Infrastructure Recommendations (stages, deployment, optimisations, performance)

---

## OpenAI API Calls Per Run

| Call | Triggered by | System Role | Output Keys |
|---|---|---|---|
| Security enrichment | `CodeAnalyzer.analyze_project` | Senior AppSec engineer | `enriched_findings`, `attack_surface_summary`, `top_3_actions` |
| Best practices enrichment | `CodeAnalyzer.analyze_project` | DevOps best-practices expert | `prioritised_recommendations`, `maturity_level`, `quick_wins` |
| Pipeline recommendations | `PipelineGenerator._ai_enhance_analysis` | Expert DevOps engineer | `pipeline_stages`, `testing_strategy`, `deployment_recommendations`, `infra_optimisations`, `performance_tips` |

---

## CLI Usage

```bash
# Full pipeline generation (all 3 AI calls + file writes)
python ai_devops_agent.py --openai-token YOUR_TOKEN

# Via environment variable (recommended for CI)
OPENAI_API_TOKEN=your_token python ai_devops_agent.py

# Analyze only — prints AI-enriched report, no file writes
python ai_devops_agent.py --openai-token YOUR_TOKEN --analyze-only

# Verbose — includes raw JSON output
python ai_devops_agent.py --openai-token YOUR_TOKEN --analyze-only --verbose

# Write AI-enriched suggestions.md
python ai_devops_agent.py --openai-token YOUR_TOKEN --suggest-changes

# Apply security fixes to Dockerfiles
python ai_devops_agent.py --openai-token YOUR_TOKEN --apply-fixes

# Generate + auto-commit (used by CI)
python ai_devops_agent.py --openai-token YOUR_TOKEN --auto-commit
```

> Without `--openai-token` or `OPENAI_API_TOKEN`, the agent exits immediately with an error.

---

## Configuration (`pipeline_request.txt`)

```
pipeline_name: qr-generator-auto-pipeline
environment: production
target: aws_ec2
instance_type: t2.micro
ami: latest-ubuntu
deploy_using: docker-compose
labels: [ai-generated, demo, qr-generator]
email_notification: true
email_recipient: demo@example.com
frontend_port: 3000
backend_port: 8000
```

Changes to this file are automatically picked up — `variables.tf` and `terraform.tfvars` are regenerated on every agent run.

---

## GitHub Secrets Required

| Secret | Purpose | Required |
|---|---|---|
| `OPENAI_API_TOKEN` | All AI enrichment and recommendations | **Mandatory** |
| `PAT_TOKEN` | Create branches and PRs from the workflow | **Mandatory** |
| `AWS_ACCESS_KEY_ID` | Terraform AWS provider | **Mandatory** |
| `AWS_SECRET_ACCESS_KEY` | Terraform AWS provider | **Mandatory** |
| `EMAIL_USERNAME` | Deployment notifications | Optional |
| `EMAIL_PASSWORD` | Deployment notifications | Optional |

---

## Generated File Map

```
.github/workflows/
├── ci-cd.yml                  ← generated by agent (validate → test → deploy)
└── ai-generate-workflow.yml   ← agent's own trigger (preserved after first write)

terraform/
├── main.tf                    ← generated once (EC2 + SG + EIP)
├── variables.tf               ← regenerated on every run from pipeline_request.txt
├── outputs.tf                 ← generated once (includes public_ip, application_urls)
├── terraform.tfvars           ← regenerated on every run from pipeline_request.txt
├── terraform.tfvars.example   ← regenerated alongside tfvars
└── user_data.sh               ← generated once (EC2 bootstrap)

suggestions.md                 ← written by --suggest-changes, committed in fix PR
frontend/Dockerfile            ← patched by --apply-fixes (USER, image pins)
backend/Dockerfile             ← patched by --apply-fixes (USER, image pins)
```

---

## Dependencies

```
pyyaml
requests
```

Install: `pip install pyyaml requests`

Python 3.11+ required. OpenAI API token required.
