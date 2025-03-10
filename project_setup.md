# Geopolitical Strategy Game - Project Setup

## Project Structure

```
geopolitics-2025/
├── backend/
│   ├── app.py                      # Main API entry point (FastAPI)
│   ├── requirements.txt            # Python dependencies
│   ├── game_logic/
│   │   ├── __init__.py
│   │   ├── economy.py              # GDP, trade, and financial systems
│   │   ├── military.py             # Military power, research, and warfare mechanics
│   │   ├── diplomacy.py            # AI-driven alliances and diplomatic relations
│   │   ├── nuclear_war.py          # Nuclear warfare logic and consequences
│   │   ├── reputation.py           # Global reputation system
│   │   ├── events.py               # Dynamic world events and triggers
│   │   ├── skill_tree.py           # Skill tree logic and progression
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py               # Database schemas for nations, leaders, and alliances
│   │   ├── queries.py              # Database queries for game state management
│   │   ├── db_config.py            # Database connection configuration
│   │   ├── initialize_all_nations.py # Script to initialize database with nations
│   │   ├── initialize_redis.py     # Script to initialize Redis with game state
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── ai_helpers.py           # AI decision-making utilities
│   │   ├── game_state.py           # Game state management
│   │   ├── websocket_manager.py    # WebSocket connection management
│   ├── tests/
│       ├── __init__.py
│       ├── test_economy.py
│       ├── test_military.py
│       ├── test_diplomacy.py
├── frontend/
│   ├── package.json                # Node.js dependencies
│   ├── vite.config.js              # Vite configuration
│   ├── index.html                  # Entry HTML file
│   ├── src/
│   │   ├── main.js                 # Main entry point
│   │   ├── App.vue                 # Main application component
│   │   ├── assets/                 # Static assets (images, fonts, etc.)
│   │   ├── components/
│   │   │   ├── Map.vue             # Interactive world map component
│   │   │   ├── Dashboard.vue       # Player overview and statistics
│   │   │   ├── Events.vue          # Game notifications and event logs
│   │   │   ├── SkillTree.vue       # Skill tree visualization
│   │   │   ├── Diplomacy.vue       # Diplomacy and alliances visualization
│   │   │   ├── NuclearWar.vue      # Nuclear warfare visualization
│   │   │   ├── Reputation.vue      # Reputation system visualization
│   │   │   ├── UI/                 # Reusable UI components
│   │   ├── views/
│   │   │   ├── GameView.vue        # Main game view
│   │   │   ├── MenuView.vue        # Game menu view
│   │   │   ├── SettingsView.vue    # Settings view
│   │   ├── store/                  # Vuex/Pinia store for state management
│   │   │   ├── index.js
│   │   │   ├── modules/
│   │   │       ├── game.js
│   │   │       ├── nations.js
│   │   │       ├── diplomacy.js
│   │   ├── services/
│   │   │   ├── api.js              # API service for backend communication
│   │   │   ├── websocket.js        # WebSocket service
│   │   ├── router/
│   │       ├── index.js            # Vue Router configuration
│   ├── public/
├── docker/
│   ├── docker-compose.yml          # Docker Compose configuration
│   ├── Dockerfile.backend          # Backend Dockerfile
│   ├── Dockerfile.frontend         # Frontend Dockerfile
├── scripts/
│   ├── deploy.py                   # Deployment script for all components
│   ├── status.py                   # Status checking script
│   ├── reset.py                    # Data reset script
│   ├── README.md                   # Documentation for scripts
├── .gitignore
├── README.md
```

## Dependencies

### Backend (Python)

The backend uses the following dependencies (defined in `backend/requirements.txt`):

```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.4.2
psycopg2-binary==2.9.9
python-dotenv==1.0.0
websockets==12.0
pytest==7.4.3
httpx==0.25.1
redis==5.0.1
numpy==1.26.1
pandas==2.1.2
```

### Frontend (Vue.js)

The frontend uses the following dependencies (defined in `frontend/package.json`):

```json
{
  "name": "geopolitics-2025",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "serve": "vite preview",
    "lint": "eslint --ext .js,.vue --ignore-path .gitignore --fix src"
  },
  "dependencies": {
    "vue": "^3.3.8",
    "vue-router": "^4.2.5",
    "pinia": "^2.1.7",
    "axios": "^1.6.2",
    "leaflet": "^1.9.4",
    "d3": "^7.8.5",
    "socket.io-client": "^4.7.2",
    "chart.js": "^4.4.0",
    "vue-chartjs": "^5.2.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.5.0",
    "vite": "^5.0.0",
    "eslint": "^8.54.0",
    "eslint-plugin-vue": "^9.18.1",
    "sass": "^1.69.5"
  }
}
```

## Installation Procedures

### Prerequisites

- Python 3.10+
- Docker and Docker Compose
- Git

### Docker-Based Setup (Recommended)

We use Docker to containerize all components of the application, making it easy to deploy and run consistently across different environments.

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/geopolitics-2025.git
   cd geopolitics-2025
   ```

2. **Install script dependencies**:

   ```bash
   pip install sqlalchemy psycopg2-binary redis requests tabulate
   ```

3. **Deploy all components using the deployment script**:

   ```bash
   python scripts/deploy.py deploy all
   ```

   This script will:

   - Start PostgreSQL container
   - Initialize the database with nations and alliances
   - Start Redis container
   - Initialize Redis with game state
   - Start the backend API server
   - Start the frontend application

4. **Check the status of all components**:

   ```bash
   python scripts/status.py
   ```

5. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### Database Configuration

The PostgreSQL database is configured with the following default settings:

- **Host**: localhost (or postgres inside Docker network)
- **Port**: 5433 (mapped from container port 5432)
- **Database**: geopolitics_2025
- **Username**: admin
- **Password**: admin

The connection string is:

```
postgresql://admin:admin@localhost:5433/geopolitics_2025
```

For applications running inside Docker containers, the connection string is:

```
postgresql://admin:admin@postgres:5432/geopolitics_2025
```

### Redis Configuration

Redis is configured with the following default settings:

- **Host**: localhost (or redis inside Docker network)
- **Port**: 6379
- **URL**: redis://localhost:6379/0

For applications running inside Docker containers, the URL is:

```
redis://redis:6379/0
```

## Development Workflow

### Using Docker (Recommended)

1. **Start all containers**:

   ```bash
   python scripts/deploy.py deploy all
   ```

2. **Make changes to the code**

3. **Restart specific containers if needed**:

   ```bash
   python scripts/deploy.py deploy backend  # Restart only the backend
   python scripts/deploy.py deploy frontend  # Restart only the frontend
   ```

4. **Reset data if needed**:

   ```bash
   python scripts/reset.py all  # Reset all data
   python scripts/reset.py database  # Reset only the database
   python scripts/reset.py redis  # Reset only Redis
   ```

5. **Stop all containers when done**:

   ```bash
   python scripts/deploy.py stop
   ```

### Local Development (Alternative)

If you prefer to develop locally without Docker:

1. **Set up a virtual environment**:

   ```bash
   cd backend
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

2. **Install backend dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file in the backend directory**:

   ```
   DATABASE_URL=postgresql://admin:admin@localhost:5433/geopolitics_2025
   REDIS_URL=redis://localhost:6379/0
   SECRET_KEY=your_secret_key_here
   DEBUG=True
   ```

4. **Run the backend development server**:

   ```bash
   uvicorn app:app --reload
   ```

5. **Install frontend dependencies**:

   ```bash
   cd frontend
   npm install
   ```

6. **Run the frontend development server**:
   ```bash
   npm run dev
   ```

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm run test
```

## Deployment

For production deployment, consider:

- Using the provided Docker setup with appropriate environment variables
- Setting up a reverse proxy (like Nginx) in front of the application
- Using a container orchestration system like Kubernetes for scaling
- Setting up proper monitoring and logging

## Troubleshooting

If you encounter issues:

1. **Check the status of all components**:

   ```bash
   python scripts/status.py
   ```

2. **Try resetting the data**:

   ```bash
   python scripts/reset.py all
   ```

3. **Restart all containers**:

   ```bash
   python scripts/deploy.py stop
   python scripts/deploy.py deploy all
   ```

4. **Check logs**:
   ```bash
   docker logs geopolitics_postgres
   docker logs geopolitics_redis
   docker logs geopolitics_backend
   docker logs geopolitics_frontend
   ```
