# Confessions Backend API

FastAPI backend for the Confessions application with PostgreSQL database and OCR text processing capabilities.

## Tech Stack

- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Primary database (via asyncpg)
- **uv** - Fast Python package manager
- **Tesseract OCR** - Text extraction from images
- **OpenCV** - Image processing

## Quick Start

### 1. Install uv (if not already installed)

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Or via scoop:**

```powershell
scoop install uv
```

**macOS/Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install dependencies

```bash
# Creates .venv and installs all dependencies
uv sync
```

### 3. Setup environment

Copy `.env.template` to `.env` and configure:

```bash
# CORS allowed origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# PostgreSQL Database
DATABASE_URL=postgresql://username:password@localhost:5432/confessions_db
DB_SCHEMA=confessions
DATABASE_SSL=false

# Self-ping (optional - for keeping server alive)
SELF_PING_ENABLED=false
HEALTHCHECK_URL=http://127.0.0.1:8000/health
```

### 4. Setup PostgreSQL Database

**Create the schema and tables:**

```bash
uv run --env-file .env python db/migrate.py
```

**Optional - Migrate data from Firebase:**

```bash
# Requires: uv pip install firebase-admin
# And FIREBASE_SERVICE_ACCOUNT_JSON_B64 in .env
uv run --env-file .env python db/migrate_from_firebase.py
```

### 5. Run the API

```bash
# Development mode with hot reload
uv run --env-file .env uvicorn main:app --reload
```

Access the API at:

- **API Root**: http://127.0.0.1:8000/
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## UV Package Management

```bash
# Add a new package
uv add package-name

# Remove a package
uv remove package-name

# Sync dependencies
uv sync

# Update lock file
uv lock

# List installed packages
uv pip list
```

## Docker Deployment

Build and run with Docker:

```bash
# Build image
docker build -t confessions-api .

# Run container
docker run -p 8000:8000 --env-file .env confessions-api
```

## API Endpoints

### Confessions

- **GET** `/` - Get all confessions from database
- **POST** `/addConfession` - Add a new confession
  - Request Body: `{ "confession": "string", "location": "string" }`
  - Response: `{ "status": 200, "message": "...", "data": {...} }`

### Export

- **GET** `/myconfessions-json/` - Generate and download MyConfessions.json file
  - Returns formatted JSON file for content generation

### Health Check

- **GET** `/health` - API health status
  - Response: `{ "status": "ok" }`

## Project Structure

```
backend/
├── db/
│   ├── schema.sql              # PostgreSQL schema definition
│   └── migrate.py              # Create database tables
├── src/
│   ├── connection.py           # Database connection pool
│   ├── models.py               # Pydantic models
│   ├── image_processing.py     # OCR image processing
│   ├── text_processing.py      # Text cleaning utilities
│   └── ocr_functions.py        # Tesseract OCR wrapper
├── main.py                     # FastAPI application
├── pyproject.toml              # Project dependencies
├── uv.lock                     # Locked dependencies
├── Dockerfile                  # Docker configuration
├── .env.template               # Environment template
└── README.md                   # This file
```

## Development

The API uses:

- **Async PostgreSQL** connection pooling for performance
- **Pydantic** models for request/response validation
- **CORS** middleware for frontend integration
- **Health check** endpoint for monitoring

## Notes

- Image processing endpoints removed - will be handled in admin frontend
- Firebase dependencies removed in favor of PostgreSQL
- Uses uv for faster dependency management
