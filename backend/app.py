from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import asyncio
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from database.db_config import engine
from database.models import Nation, Leader

# Create FastAPI app
app = FastAPI(title="Geopolitics 2025 API", 
              description="Backend API for the Geopolitics 2025 strategy game",
              version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Game state
GAME_STATE = {
    "date": "January 1, 2025",
    "speed": "normal",
    "paused": True,
    "nations": [
        {"name": "United States", "leader": "Donald Trump", "gdp": 25000, "military_power": 100},
        {"name": "China", "leader": "Li Qiang", "gdp": 18000, "military_power": 85},
        {"name": "Russia", "leader": "Vladimir Putin", "gdp": 4000, "military_power": 70},
        {"name": "India", "leader": "Narendra Modi", "gdp": 3500, "military_power": 65},
        {"name": "France", "leader": "Emmanuel Macron", "gdp": 3000, "military_power": 60},
        {"name": "Germany", "leader": "Friedrich Merz", "gdp": 4500, "military_power": 55},
        {"name": "United Kingdom", "leader": "Keir Starmer", "gdp": 3200, "military_power": 58},
        {"name": "Poland", "leader": "Sławomir Mentzen", "gdp": 800, "military_power": 30},
        {"name": "Ukraine", "leader": "Volodymyr Zelenskyy", "gdp": 350, "military_power": 25},
        {"name": "North Korea", "leader": "Kim Jong-un", "gdp": 30, "military_power": 20}
    ],
    "alliances": [
        {
            "name": "NATO",
            "members": ["United States", "United Kingdom", "France", "Germany", "Poland"]
        },
        {
            "name": "Shanghai Cooperation",
            "members": ["China", "Russia"]
        }
    ],
    "events": []
}

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        # Send current game state upon connection
        await self.send_personal_message(json.dumps(GAME_STATE), websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def broadcast_game_state(self):
        if self.active_connections:
            await self.broadcast(json.dumps(GAME_STATE))

manager = ConnectionManager()

# Game simulation task
async def simulate_game_progression():
    current_date = datetime.strptime(GAME_STATE["date"], "%B %d, %Y")
    
    # Define speed multipliers
    speed_multipliers = {
        "very_slow": 0.5,
        "slow": 0.8,
        "normal": 1.0,
        "fast": 1.5,
        "very_fast": 2.0
    }
    
    while True:
        try:
            # Skip simulation if game is paused
            if GAME_STATE["paused"]:
                await asyncio.sleep(1)
                continue
                
            # Get speed multiplier
            multiplier = speed_multipliers.get(GAME_STATE["speed"], 1.0)
            
            # Advance date
            current_date += timedelta(days=1)
            GAME_STATE["date"] = current_date.strftime("%B %d, %Y")
            
            # Update nation data
            for nation in GAME_STATE["nations"]:
                # Simulate economic growth
                gdp_change = random.uniform(-0.2, 0.5) * multiplier
                nation["gdp"] = round(max(nation["gdp"] * (1 + gdp_change / 100), 10), 1)
                
                # Simulate military changes
                military_change = random.uniform(-0.1, 0.2) * multiplier
                nation["military_power"] = round(min(max(nation["military_power"] * (1 + military_change / 100), 10), 100), 1)
            
            # Random events (very rare)
            if random.random() < 0.01 * multiplier:
                event_types = ["political", "economic", "military", "disaster"]
                event_type = random.choice(event_types)
                nations = [nation["name"] for nation in GAME_STATE["nations"]]
                affected_nation = random.choice(nations)
                
                events = {
                    "political": [
                        f"Election announced in {affected_nation}",
                        f"Political unrest in {affected_nation}",
                        f"New policy announced by {affected_nation}"
                    ],
                    "economic": [
                        f"Economic boom in {affected_nation}",
                        f"Recession hitting {affected_nation}",
                        f"New trade deal involving {affected_nation}"
                    ],
                    "military": [
                        f"{affected_nation} increases military spending",
                        f"{affected_nation} reduces nuclear arsenal",
                        f"Military exercise by {affected_nation}"
                    ],
                    "disaster": [
                        f"Natural disaster in {affected_nation}",
                        f"Infrastructure failure in {affected_nation}",
                        f"Public health crisis in {affected_nation}"
                    ]
                }
                
                event_text = random.choice(events[event_type])
                GAME_STATE["events"].insert(0, {
                    "date": GAME_STATE["date"],
                    "type": event_type,
                    "text": event_text
                })
                
                # Keep only the last 20 events
                if len(GAME_STATE["events"]) > 20:
                    GAME_STATE["events"] = GAME_STATE["events"][:20]
            
            # Broadcast updated game state
            await manager.broadcast_game_state()
            
            # Sleep based on game speed
            await asyncio.sleep(1.0 / multiplier)
        except Exception as e:
            print(f"Error in game simulation: {str(e)}")
            await asyncio.sleep(5)  # Wait 5 seconds before retrying

# Start game simulation on startup
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(simulate_game_progression())

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to Geopolitics 2025 API"}

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("New WebSocket connection received")
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Process commands from the client
            try:
                command = json.loads(data)
                print(f"Received command: {command}")
                if "action" in command:
                    if command["action"] == "pause":
                        GAME_STATE["paused"] = True
                        print("Game paused")
                    elif command["action"] == "resume":
                        GAME_STATE["paused"] = False
                        print("Game resumed")
                    elif command["action"] == "set_speed":
                        GAME_STATE["speed"] = command.get("speed", "normal")
                        print(f"Game speed set to: {GAME_STATE['speed']}")
                    
                    # Broadcast updated state after command
                    await manager.broadcast_game_state()
            except json.JSONDecodeError:
                print(f"Failed to parse WebSocket message: {data}")
                pass
    except WebSocketDisconnect:
        print("WebSocket disconnected")
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        manager.disconnect(websocket)

# Playable nations endpoint
@app.get("/playable-nations")
async def get_playable_nations():
    """Get all playable nations with their details and difficulty levels"""
    session = Session(engine)
    try:
        # Get all nations and their leaders
        nations_with_leaders = (
            session.query(Nation, Leader)
            .join(Leader, Nation.leader_id == Leader.id)
            .all()
        )
        
        # Format the response
        result = []
        for nation, leader in nations_with_leaders:
            # Determine difficulty level based on factors like military power, economy, etc.
            difficulty = "medium"  # default
            
            # Simple algorithm: higher military power and GDP = easier
            if nation.military_power >= 90 and nation.gdp >= 20000:
                difficulty = "easy"
            elif nation.military_power < 60 or nation.gdp < 3000:
                difficulty = "hard"
                
            # Format description based on nation's attributes
            description = f"{'Nuclear power with ' if nation.has_nuclear_weapons else ''}"
            
            if nation.military_power > 80:
                description += "powerful military and "
            elif nation.military_power > 60:
                description += "strong military and "
            else:
                description += "developing military and "
                
            if nation.gdp > 15000:
                description += "massive economy."
            elif nation.gdp > 5000:
                description += "substantial economy."
            else:
                description += "growing economy."
            
            result.append({
                "name": nation.name,
                "leader": leader.name,
                "difficulty": difficulty,
                "description": description,
            })
        
        return result
    finally:
        session.close()

# Game state endpoint (HTTP)
@app.get("/game-state")
async def get_game_state():
    return GAME_STATE

# Update game state endpoint (for admin/testing purposes)
@app.post("/game-state/update")
async def update_game_state(data: Dict[str, Any]):
    global GAME_STATE
    
    # Update specific fields of the game state
    for key, value in data.items():
        if key in GAME_STATE:
            GAME_STATE[key] = value
    
    # Broadcast updated state
    await manager.broadcast_game_state()
    return {"message": "Game state updated", "state": GAME_STATE}

# Run the app
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 