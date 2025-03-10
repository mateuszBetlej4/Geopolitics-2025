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
├── .gitignore
├── README.md
```

## Dependencies

### Backend (Python)

Create a `backend/requirements.txt` file with the following dependencies:

```
fastapi==0.104.1
uvicorn==0.23.2
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

Create a `frontend/package.json` file with the following dependencies:

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
- Node.js 18+
- PostgreSQL 14+
- Redis (optional, for caching)
- Docker and Docker Compose (optional, for containerization)

### Backend Setup

1. Create a virtual environment:

   ```bash
   cd backend
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the backend directory:

   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/geopolitics
   REDIS_URL=redis://localhost:6379/0
   SECRET_KEY=your_secret_key_here
   DEBUG=True
   ```

4. Run the development server:
   ```bash
   uvicorn app:app --reload
   ```

### Frontend Setup

1. Install dependencies:

   ```bash
   cd frontend
   npm install
   ```

2. Create a `.env` file in the frontend directory:

   ```
   VITE_API_URL=http://localhost:8000
   VITE_WS_URL=ws://localhost:8000/ws
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

### Database Setup

1. Create a PostgreSQL database:

   ```bash
   createdb geopolitics
   ```

2. The database tables will be automatically created when you first run the backend application.

### Docker Setup (Optional)

1. Build and run the containers:

   ```bash
   docker-compose up -d
   ```

2. Access the application at `http://localhost:8080`

## Development Workflow

1. Start the backend server
2. Start the frontend development server
3. Access the application at `http://localhost:5173` (or the port specified by Vite)

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

For production deployment, consider using:

- Backend: Gunicorn with Uvicorn workers
- Frontend: Nginx serving static files
- Database: Managed PostgreSQL service
- Caching: Managed Redis service
- Container Orchestration: Kubernetes or Docker Swarm
