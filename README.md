# Intelivox
Smart phone book management system, lead management, tasks and smart customer management

## Python REST Server for Auto Update Workflow

### Run locally
1. Install dependencies:
   ```bash
   py -m pip install -r requirements.txt
   ```
2. Run the API:
   ```bash
   py -m uvicorn app.main:app --reload
   ```
3. Open the interactive docs:
   - http://127.0.0.1:8000/docs

### API Endpoints
- `POST /api/residents`
- `GET /api/residents`
- `GET /api/residents/{resident_id}`
- `PATCH /api/residents/{resident_id}`

### Storage
- Local JSON file: `data/residents.json`
- Data paths are created automatically on startup
