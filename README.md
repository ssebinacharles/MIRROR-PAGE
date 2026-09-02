# MIRROR Backend

Django REST Framework backend for MIRROR, an intent-aware authorization layer for WebMCP agents.

## Current stack

- Python 3.12+ recommended
- Django 5.2 LTS line
- Django REST Framework 3.18.x
- SQLite for MVP

DRF's current requirements list supports Django 5.2 and later supported Python versions; the 3.18 series is current as of August 2026. See the official DRF docs before upgrading. 

## Run locally

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

Health check:

```text
GET http://127.0.0.1:8000/api/health/
```

Evaluate a WebMCP action:

```text
POST /api/policies/evaluate/
```

Example payload:

```json
{
  "intent_contract_id": "...",
  "tool_name": "purchase_product",
  "agent_id": "...",
  "input_payload": {"product_id": "p1"},
  "execute": false
}
```

The backend is deliberately deterministic for authorization. LLMs may help produce candidate intents in the frontend, but the backend remains the authoritative policy decision point.
