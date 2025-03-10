import os
import redis
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Redis URL from environment variable or use default
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

def initialize_redis():
    try:
        # Connect to Redis
        r = redis.from_url(REDIS_URL)
        
        # Test connection with a ping
        response = r.ping()
        print(f"Redis connection test: {'SUCCESS' if response else 'FAILED'}")
        
        # Clear existing data
        r.flushall()
        print("Cleared existing Redis data")
        
        # Initialize game state data
        game_state = {
            "game_started": False,
            "current_date": "2025-01-01",
            "game_speed": "normal",
            "paused": True,
            "active_events": []
        }
        
        # Initialize AI behavior settings
        ai_behavior = {
            "aggression_modifier": 1.0,
            "diplomatic_threshold": 0.6,
            "economic_focus": 0.5,
            "military_focus": 0.5,
            "random_event_frequency": "medium"
        }
        
        # Initialize cached data
        cached_data = {
            "last_update": "2025-01-01T00:00:00Z",
            "global_tension": 50.0,
            "active_conflicts": []
        }
        
        # Store data in Redis
        r.set("game_state", json.dumps(game_state))
        r.set("ai_behavior", json.dumps(ai_behavior))
        r.set("cached_data", json.dumps(cached_data))
        
        # Set some nation-specific data
        nations = ["United States", "China", "Russia", "India", "France", 
                  "Germany", "United Kingdom", "Poland", "Ukraine", "North Korea"]
        
        for nation in nations:
            nation_key = f"nation:{nation.lower().replace(' ', '_')}"
            nation_data = {
                "last_action": "none",
                "ai_state": "neutral",
                "current_focus": "balanced",
                "relations": {}
            }
            
            # Set initial relations between nations
            for other_nation in nations:
                if nation != other_nation:
                    # Default neutral relations (50)
                    relation_value = 50
                    
                    # Set some predefined relations
                    if (nation == "United States" and other_nation == "Russia") or \
                       (nation == "Russia" and other_nation == "United States"):
                        relation_value = 20  # Tense relations
                    
                    elif (nation == "China" and other_nation == "United States") or \
                         (nation == "United States" and other_nation == "China"):
                        relation_value = 30  # Somewhat tense relations
                    
                    elif (nation == "Russia" and other_nation == "Ukraine") or \
                         (nation == "Ukraine" and other_nation == "Russia"):
                        relation_value = 10  # Very tense relations
                    
                    elif (nation == "United States" and other_nation == "United Kingdom") or \
                         (nation == "United Kingdom" and other_nation == "United States"):
                        relation_value = 90  # Strong allies
                    
                    elif (nation == "Russia" and other_nation == "China") or \
                         (nation == "China" and other_nation == "Russia"):
                        relation_value = 75  # Good relations
                    
                    nation_data["relations"][other_nation.lower().replace(' ', '_')] = relation_value
            
            r.set(nation_key, json.dumps(nation_data))
            
        print(f"Initialized Redis with game state and nation data")
        
        # Verify data was stored correctly
        print("\nVerifying stored data:")
        print(f"Game State: {r.get('game_state').decode('utf-8')}")
        print(f"Sample Nation Data (US): {r.get('nation:united_states').decode('utf-8')}")
        
        return True
        
    except Exception as e:
        print(f"Error initializing Redis: {e}")
        return False

if __name__ == "__main__":
    print(f"Initializing Redis at {REDIS_URL}...")
    success = initialize_redis()
    if success:
        print("\nRedis initialization complete!")
    else:
        print("\nRedis initialization failed!") 