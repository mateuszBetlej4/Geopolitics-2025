from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.database.db_config import engine, Base
from backend.database.models import Nation, Leader, Alliance, Treaty, GameEvent, ResearchProgress

def initialize_all_nations():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    session = Session(engine)
    
    try:
        # Clear existing data - handle junction tables first
        print("Clearing existing data from database...")
        
        # Delete from junction tables first
        session.execute(text("DELETE FROM alliance_members"))
        session.execute(text("DELETE FROM treaty_participants"))
        session.commit()
        
        # Now delete from main tables
        session.query(Alliance).delete()
        session.query(Treaty).delete()
        session.query(GameEvent).delete()
        session.query(ResearchProgress).delete()
        session.query(Nation).delete()
        session.query(Leader).delete()
        session.commit()
        print("Cleared existing data from database")
        
        # Define all nations and their leaders
        all_nations = [
            # Major Powers
            {
                "leader": {
                    "name": "Donald Trump",
                    "personality_type": "aggressive",
                    "aggression_factor": 0.8,
                    "diplomatic_factor": 0.3,
                    "economic_focus": 0.7,
                    "military_focus": 0.8
                },
                "nation": {
                    "name": "United States",
                    "gdp": 25000.0,
                    "military_power": 100.0,
                    "population": 330.0,
                    "has_nuclear_weapons": True,
                    "ground_forces": 90.0,
                    "air_forces": 100.0,
                    "naval_forces": 100.0,
                    "nuclear_arsenal": 5500,
                    "global_reputation": 75.0
                }
            },
            {
                "leader": {
                    "name": "Li Qiang",
                    "personality_type": "diplomatic",
                    "aggression_factor": 0.5,
                    "diplomatic_factor": 0.7,
                    "economic_focus": 0.9,
                    "military_focus": 0.6
                },
                "nation": {
                    "name": "China",
                    "gdp": 18000.0,
                    "military_power": 85.0,
                    "population": 1400.0,
                    "has_nuclear_weapons": True,
                    "ground_forces": 95.0,
                    "air_forces": 80.0,
                    "naval_forces": 70.0,
                    "nuclear_arsenal": 350,
                    "global_reputation": 60.0
                }
            },
            {
                "leader": {
                    "name": "Vladimir Putin",
                    "personality_type": "opportunistic",
                    "aggression_factor": 0.9,
                    "diplomatic_factor": 0.4,
                    "economic_focus": 0.5,
                    "military_focus": 0.9
                },
                "nation": {
                    "name": "Russia",
                    "gdp": 4000.0,
                    "military_power": 70.0,
                    "population": 145.0,
                    "has_nuclear_weapons": True,
                    "ground_forces": 85.0,
                    "air_forces": 75.0,
                    "naval_forces": 65.0,
                    "nuclear_arsenal": 6000,
                    "global_reputation": 40.0
                }
            },
            # Other Major Nations
            {
                "leader": {
                    "name": "Narendra Modi",
                    "personality_type": "diplomatic",
                    "aggression_factor": 0.4,
                    "diplomatic_factor": 0.7,
                    "economic_focus": 0.8,
                    "military_focus": 0.6
                },
                "nation": {
                    "name": "India",
                    "gdp": 3500.0,
                    "military_power": 65.0,
                    "population": 1380.0,
                    "has_nuclear_weapons": True,
                    "ground_forces": 80.0,
                    "air_forces": 60.0,
                    "naval_forces": 55.0,
                    "nuclear_arsenal": 160,
                    "global_reputation": 65.0
                }
            },
            {
                "leader": {
                    "name": "Emmanuel Macron",
                    "personality_type": "diplomatic",
                    "aggression_factor": 0.3,
                    "diplomatic_factor": 0.8,
                    "economic_focus": 0.7,
                    "military_focus": 0.5
                },
                "nation": {
                    "name": "France",
                    "gdp": 2800.0,
                    "military_power": 60.0,
                    "population": 67.0,
                    "has_nuclear_weapons": True,
                    "ground_forces": 65.0,
                    "air_forces": 70.0,
                    "naval_forces": 75.0,
                    "nuclear_arsenal": 290,
                    "global_reputation": 70.0
                }
            },
            {
                "leader": {
                    "name": "Friedrich Merz",
                    "personality_type": "diplomatic",
                    "aggression_factor": 0.2,
                    "diplomatic_factor": 0.9,
                    "economic_focus": 0.9,
                    "military_focus": 0.4
                },
                "nation": {
                    "name": "Germany",
                    "gdp": 4000.0,
                    "military_power": 55.0,
                    "population": 83.0,
                    "has_nuclear_weapons": False,
                    "ground_forces": 60.0,
                    "air_forces": 65.0,
                    "naval_forces": 50.0,
                    "nuclear_arsenal": 0,
                    "global_reputation": 75.0
                }
            },
            {
                "leader": {
                    "name": "Keir Starmer",
                    "personality_type": "diplomatic",
                    "aggression_factor": 0.3,
                    "diplomatic_factor": 0.8,
                    "economic_focus": 0.7,
                    "military_focus": 0.6
                },
                "nation": {
                    "name": "United Kingdom",
                    "gdp": 3200.0,
                    "military_power": 65.0,
                    "population": 67.0,
                    "has_nuclear_weapons": True,
                    "ground_forces": 60.0,
                    "air_forces": 75.0,
                    "naval_forces": 80.0,
                    "nuclear_arsenal": 225,
                    "global_reputation": 70.0
                }
            },
            # Smaller Nations
            {
                "leader": {
                    "name": "Sławomir Mentzen",
                    "personality_type": "opportunistic",
                    "aggression_factor": 0.6,
                    "diplomatic_factor": 0.5,
                    "economic_focus": 0.9,
                    "military_focus": 0.7
                },
                "nation": {
                    "name": "Poland",
                    "gdp": 700.0,
                    "military_power": 30.0,
                    "population": 38.0,
                    "has_nuclear_weapons": False,
                    "ground_forces": 40.0,
                    "air_forces": 30.0,
                    "naval_forces": 20.0,
                    "nuclear_arsenal": 0,
                    "global_reputation": 60.0
                }
            },
            {
                "leader": {
                    "name": "Volodymyr Zelenskyy",
                    "personality_type": "opportunistic",
                    "aggression_factor": 0.6,
                    "diplomatic_factor": 0.7,
                    "economic_focus": 0.5,
                    "military_focus": 0.9
                },
                "nation": {
                    "name": "Ukraine",
                    "gdp": 200.0,
                    "military_power": 25.0,
                    "population": 44.0,
                    "has_nuclear_weapons": False,
                    "ground_forces": 35.0,
                    "air_forces": 20.0,
                    "naval_forces": 10.0,
                    "nuclear_arsenal": 0,
                    "global_reputation": 65.0
                }
            },
            {
                "leader": {
                    "name": "Kim Jong-un",
                    "personality_type": "aggressive",
                    "aggression_factor": 0.9,
                    "diplomatic_factor": 0.2,
                    "economic_focus": 0.3,
                    "military_focus": 0.9
                },
                "nation": {
                    "name": "North Korea",
                    "gdp": 40.0,
                    "military_power": 20.0,
                    "population": 25.0,
                    "has_nuclear_weapons": True,
                    "ground_forces": 30.0,
                    "air_forces": 15.0,
                    "naval_forces": 10.0,
                    "nuclear_arsenal": 30,
                    "global_reputation": 20.0
                }
            }
        ]
        
        # Add all nations
        nations_by_name = {}
        for nation_data in all_nations:
            # Create leader
            leader = Leader(**nation_data["leader"])
            session.add(leader)
            session.flush()  # Flush to get the leader ID
            
            # Create nation with leader
            nation = Nation(**nation_data["nation"], leader=leader)
            session.add(nation)
            session.flush()
            
            # Store nation for alliance creation
            nations_by_name[nation.name] = nation
            
            print(f"Added {nation_data['nation']['name']} with leader {nation_data['leader']['name']}")
        
        # Create alliances
        alliances = [
            {
                "name": "NATO",
                "alliance_type": "military",
                "members": ["United States", "United Kingdom", "France", "Germany", "Poland"]
            },
            {
                "name": "European Union",
                "alliance_type": "economic",
                "members": ["France", "Germany", "Poland"]
            },
            {
                "name": "Shanghai Cooperation Organization",
                "alliance_type": "economic",
                "members": ["China", "Russia"]
            },
            {
                "name": "BRICS",
                "alliance_type": "economic",
                "members": ["Russia", "China", "India"]
            }
        ]
        
        for alliance_data in alliances:
            alliance = Alliance(
                name=alliance_data["name"],
                alliance_type=alliance_data["alliance_type"],
                members=[nations_by_name[name] for name in alliance_data["members"] if name in nations_by_name]
            )
            session.add(alliance)
            print(f"Added alliance: {alliance_data['name']} with members: {', '.join(alliance_data['members'])}")
        
        # Commit all changes
        session.commit()
        print("\nSuccessfully initialized all nations, leaders, and alliances!")
        
    except Exception as e:
        session.rollback()
        print(f"Error initializing database: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    print("Initializing all nations in the database...")
    initialize_all_nations()
    print("Database initialization complete!") 