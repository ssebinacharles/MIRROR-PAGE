# MIRROR Frontend

Professional React + TypeScript control plane for MIRROR, the intent firewall for the agentic web.

## Stack

- React 19
- TypeScript
- Vite
- React Router
- Axios
- Lucide React
- WebMCP Imperative API adapter

## Run

```bash
npm install
npm run dev
```

Production build:

```bash
npm run build
```

Tests:

```bash
npm test
```

## Environment

Copy `.env.example` to `.env.local`.

```env
VITE_API_URL=http://127.0.0.1:8000/api
VITE_MIRROR_DEMO_MODE=true
```

## Backend

The frontend expects the Django API under `/api/`. Start the backend first and seed demo data:

```bash
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

## WebMCP

WebMCP-specific code lives under `src/webmcp/`. The adapter registers the MIRROR tools when `document.modelContext` is available. Consequential actions call the MIRROR authorization endpoint before execution.

## UI direction

The interface intentionally uses a restrained, near-monochrome control-plane aesthetic. Semantic color is reserved for authorization state, risk and system status.
