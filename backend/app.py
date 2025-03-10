from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import asyncio
from typing import List, Dict, Any

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

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to Geopolitics 2025 API"}

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Process the received data
            await manager.broadcast(f"Message received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("Client disconnected")

# Game state endpoint
@app.get("/game-state")
async def get_game_state():
    # This would normally fetch from a database
    return {
        "date": "January 1, 2025",
        "nations": [
            {"name": "United States", "leader": "Donald Trump", "gdp": 25000, "military_power": 100},
            {"name": "China", "leader": "Li Qiang", "gdp": 18000, "military_power": 85},
            {"name": "Russia", "leader": "Vladimir Putin", "gdp": 4000, "military_power": 70},
        ]
    }

# Run the app
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 