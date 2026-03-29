# Point Estimator API

FastAPI REST API generated from the point estimator notebook.

## Endpoints

- `GET /`
- `GET /health`
- `POST /estimate-points`
- `GET /docs`

## Local setup

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn point_estimator_api.main:app --reload
```

Open `http://127.0.0.1:8000/docs`

## Example request

```json
{
  "stars": 5,
  "task_title": "Emergency Plumbing Help",
  "task_description": "Excellent and fast support. The helper was professional, kind, and clear while fixing the issue late at night.",
  "timestamp": "2026-03-29T02:30:00Z",
  "location": "West Haven, CT"
}
```

## Optional API key protection

If you set the `API_KEY` environment variable, the API will require the header:

```text
X-API-Key: your-secret-value
```

## Vercel deployment

1. Push this project to GitHub.
2. Import the repo into Vercel.
3. In Vercel Project Settings -> Environment Variables, add `API_KEY` if you want to protect the API.
4. Redeploy.

### Hosted URLs

After deployment, your URLs will look like:

- `https://your-project-name.vercel.app/`
- `https://your-project-name.vercel.app/health`
- `https://your-project-name.vercel.app/docs`
- `https://your-project-name.vercel.app/estimate-points`

## cURL example

Without API key:

```bash
curl -X POST "https://your-project-name.vercel.app/estimate-points" \
  -H "Content-Type: application/json" \
  -d '{
    "stars": 5,
    "task_title": "Emergency Plumbing Help",
    "task_description": "Excellent and fast support. The helper was professional, kind, and clear while fixing the issue late at night.",
    "timestamp": "2026-03-29T02:30:00Z",
    "location": "West Haven, CT"
  }'
```

With API key:

```bash
curl -X POST "https://your-project-name.vercel.app/estimate-points" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-value" \
  -d '{
    "stars": 5,
    "task_title": "Emergency Plumbing Help",
    "task_description": "Excellent and fast support. The helper was professional, kind, and clear while fixing the issue late at night.",
    "timestamp": "2026-03-29T02:30:00Z",
    "location": "West Haven, CT"
  }'
```
