import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:3000/api/ws"
    print(f"Connecting to {uri}...")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected!")
            
            # Receive initial state
            data = await websocket.recv()
            parsed = json.loads(data)
            print(f"Received game state:")
            print(f"- Date: {parsed.get('date', 'Not found')}")
            print(f"- Nations: {len(parsed.get('nations', []))}")
            print(f"- Paused: {parsed.get('paused', 'Unknown')}")
            
            # Test pause command
            print("\nSending pause command...")
            await websocket.send(json.dumps({"action": "pause"}))
            await asyncio.sleep(1)
            
            # Receive updated state
            data = await websocket.recv()
            parsed = json.loads(data)
            print("\nReceived updated game state:")
            print(f"- Date: {parsed.get('date', 'Not found')}")
            print(f"- Paused: {parsed.get('paused', 'Unknown')}")
            
            # Test resume command
            print("\nSending resume command...")
            await websocket.send(json.dumps({"action": "resume"}))
            await asyncio.sleep(1)
            
            # Receive updated state
            data = await websocket.recv()
            parsed = json.loads(data)
            print("\nReceived updated game state:")
            print(f"- Date: {parsed.get('date', 'Not found')}")
            print(f"- Paused: {parsed.get('paused', 'Unknown')}")
            
            print("\nWebSocket test completed successfully!")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket()) 