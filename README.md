# Intelivox Backend

REST API for resident management system with telephony webhook integration. Built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features
- Resident CRUD operations (Create, Read, Update)
- Support for individuals, organizations, and institutions
- Multiple contact types (mobile, home, work phone, email)
- Status tracking (new, active, pending, inactive)
- Full-text search capabilities
- SQLite/PostgreSQL database support
- Auto-generated API documentation

## Tech Stack
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## Run Locally

### Prerequisites
- Python 3.11+
- pip

### Setup
1. Install dependencies:
   ```bash
   py -m pip install -r requirements.txt
   ```

2. Create `.env` file:
   ```bash
   copy .env.example .env
   ```

3. Run database migrations:
   ```bash
   alembic upgrade head
   ```

4. Start the API server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

5. Open the interactive API docs:
   - Swagger UI: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

### Residents
- `POST /api/residents` - Create a new resident
- `GET /api/residents` - List all residents
- `GET /api/residents?q=search` - Search residents by name/phone/email
- `GET /api/residents/{resident_id}` - Get resident by ID
- `PATCH /api/residents/{resident_id}` - Update resident

### Example Request
```json
{
  "type": "individual",
  "status": "active",
  "first_name": "John",
  "last_name": "Doe",
  "mobile_phone": "+1234567890",
  "email": "john@example.com"
}
```

## Database
- **Development**: SQLite (`data/dev.db`)
- **Production**: PostgreSQL (configure via `DATABASE_URL`)
- Data paths are created automatically on startup

## Docker

### Run with Docker Compose (Recommended)
Runs both backend and frontend together:

```bash
docker-compose up --build
```

**Access:**
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:5173

**Stop containers:**
```bash
docker-compose down
```

### Run Backend Only with Docker

1. Build the image:
   ```bash
   docker build -t intelivox-backend .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 -v ./data:/app/data intelivox-backend
   ```

## Project Structure
```
app/
├── api/
│   └── endpoints.py       # API routes
├── models/
│   ├── resident.py        # SQLAlchemy models
│   └── schemas.py         # Pydantic schemas
├── services/
│   ├── resident_service.py
│   └── storage_service.py
├── config.py              # App configuration
├── db.py                  # Database setup
└── main.py                # FastAPI app

alembic/
└── versions/              # Database migrations

data/
├── dev.db                 # SQLite database
└── residents.json         # JSON storage (legacy)
```
