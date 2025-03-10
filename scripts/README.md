# Geopolitics-2025 Deployment Scripts

This directory contains scripts for deploying, managing, and monitoring the Geopolitics-2025 game.

## Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose
- Required Python packages: `sqlalchemy`, `psycopg2-binary`, `redis`, `requests`, `tabulate`

You can install the required packages with:

```bash
pip install -r ../backend/requirements.txt
pip install tabulate requests
```

## Available Scripts

These scripts can be run from any directory - they use absolute paths to find the necessary files.

### 1. Deploy Script (`deploy.py`)

Deploys the game components (database, Redis, backend, frontend).

```bash
# Deploy all components
python scripts/deploy.py deploy all

# Deploy specific components
python scripts/deploy.py deploy database
python scripts/deploy.py deploy redis
python scripts/deploy.py deploy backend
python scripts/deploy.py deploy frontend

# Stop all containers
python scripts/deploy.py stop
```

### 2. Status Script (`status.py`)

Checks the status of all game components.

```bash
python scripts/status.py
```

This will display:

- Docker container status
- PostgreSQL database status and data summary
- Redis status and data summary
- Backend API status
- Frontend application status

### 3. Reset Script (`reset.py`)

Resets the game data to its initial state.

```bash
# Reset all game data
python scripts/reset.py all

# Reset specific components
python scripts/reset.py database
python scripts/reset.py redis
```

## Typical Workflow

1. **First-time setup**:

   ```bash
   python scripts/deploy.py deploy all
   ```

2. **Check status**:

   ```bash
   python scripts/status.py
   ```

3. **Reset game data** (if needed):

   ```bash
   python scripts/reset.py all
   ```

4. **Stop all containers** (when done):
   ```bash
   python scripts/deploy.py stop
   ```

## Accessing the Game

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Troubleshooting

If you encounter issues:

1. Check the status of all components:

   ```bash
   python scripts/status.py
   ```

2. Try resetting the data:

   ```bash
   python scripts/reset.py all
   ```

3. Restart all containers:
   ```bash
   python scripts/deploy.py stop
   python scripts/deploy.py deploy all
   ```
