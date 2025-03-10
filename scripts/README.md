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

### 1. Deploy Script (`deploy.py`)

Deploys the game components (database, Redis, backend, frontend).

```bash
# Deploy all components
python deploy.py deploy all

# Deploy specific components
python deploy.py deploy database
python deploy.py deploy redis
python deploy.py deploy backend
python deploy.py deploy frontend

# Stop all containers
python deploy.py stop
```

### 2. Status Script (`status.py`)

Checks the status of all game components.

```bash
python status.py
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
python reset.py all

# Reset specific components
python reset.py database
python reset.py redis
```

## Typical Workflow

1. **First-time setup**:

   ```bash
   python deploy.py deploy all
   ```

2. **Check status**:

   ```bash
   python status.py
   ```

3. **Reset game data** (if needed):

   ```bash
   python reset.py all
   ```

4. **Stop all containers** (when done):
   ```bash
   python deploy.py stop
   ```

## Accessing the Game

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Troubleshooting

If you encounter issues:

1. Check the status of all components:

   ```bash
   python status.py
   ```

2. Try resetting the data:

   ```bash
   python reset.py all
   ```

3. Restart all containers:
   ```bash
   python deploy.py stop
   python deploy.py deploy all
   ```
