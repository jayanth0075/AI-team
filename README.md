# SUTRA AI Agents API

6 AI Agents for Industry Requirement Extraction, Technology Discovery, Fit Evaluation, Compliance, Commercialization, and Citation Verification.

## Tech Stack

- **Framework**: FastAPI (Python 3.14)
- **Database**: PostgreSQL (Supabase with pgvector)
- **LLM**: OpenAI GPT-4.1 / Gemini 2.5 Flash
- **Cache**: Redis (optional)

---

## Prerequisites

- Python 3.14+
- PostgreSQL 15+ (with pgvector extension for vector search)
- Redis (optional, for caching)
- OpenAI API key or Gemini API key

---

## Quick Start

### 1. Clone & Setup

```bash
git clone <repo-url>
cd <project-folder>

# Create virtual environment
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your settings:

| Variable | Description |
|---|---|
| `DATABASE_URL` | Supabase PostgreSQL connection string |
| `OPENAI_API_KEY` | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4.1` (recommended) or `gpt-4o-mini` |
| `LLM_PROVIDER` | `openai` (recommended) or `gemini` |

### 3. Supabase Database Setup

1. Create a project on [supabase.com](https://supabase.com)
2. Enable the pgvector extension in Supabase SQL Editor:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
3. Get your connection string from Supabase Dashboard → Project Settings → Database → Connection string (URI)
4. Set it as `DATABASE_URL` in `.env`

### 4. Run Database Migrations

```bash
alembic upgrade head
```

### 5. Start the Server

```bash
python run.py
```

API runs at `http://localhost:8000`. Docs at `http://localhost:8000/docs`.

---

## LLM Provider Options

| Provider | Model | Speed | Notes |
|---|---|---|---|
| **OpenAI** | **gpt-5.5** | **16s** | **Recommended — most detailed, passes all tests** |
| OpenAI | gpt-4.1 | 1.0s | Fast alternative, good quality |
| Gemini | gemini-3.5-flash | 6.2s | Alternative option, faster |
| Gemini | gemini-2.5-pro | 14.8s | Slower but detailed |

Set `LLM_PROVIDER=openai` or `LLM_PROVIDER=gemini` in `.env`.

---

## Agents Overview

| Agent | Endpoint | File |
|---|---|---|
| **Industry Requirement Extractor** | `POST /company/register` | `app/agents/industry_extractor.py` |
| **Technology Discovery** | `POST /technology/match` | `app/agents/technology_discovery.py` |
| **Industry Fit Evaluator** | `POST /technology/industry-fit` | `app/agents/industry_fit_evaluator.py` |
| **Compliance Advisor** | `POST /technology/compliance` | `app/agents/compliance_advisor.py` |
| **Commercialization Advisor** | `POST /technology/license` | `app/agents/commercialization_advisor.py` |
| **Citation Verifier** | `POST /evidence/verify` | `app/agents/citation_verifier.py` |

---

## Testing

```bash
pytest tests/ -v
```

---

## Deployment

### Render / Railway / Fly.io

1. Set the environment variables from `.env.example` in your hosting dashboard
2. Ensure `DATABASE_URL` points to your Supabase instance
3. Run `alembic upgrade head` as a release command
4. Start command: `python run.py`

### Docker (Coming Soon)

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `GET` | `/health/` | Detailed health status |
| `POST` | `/company/register` | Register company & extract requirements |
| `GET` | `/company/{id}` | Get company profile |
| `POST` | `/technology/register` | Register a technology |
| `POST` | `/technology/match` | Match technologies to requirements |
| `POST` | `/technology/industry-fit` | Evaluate industry fit |
| `POST` | `/technology/compliance` | Check compliance requirements |
| `POST` | `/technology/license` | Analyze commercialization |


## Architecture

See `AGENT_TECHNICAL_GUIDE.md` for detailed technical architecture of all 6 agents.
