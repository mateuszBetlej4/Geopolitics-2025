from sqlalchemy import inspect
from backend.database.db_config import engine

def check_database():
    inspector = inspect(engine)
    
    # Get all table names
    tables = inspector.get_table_names()
    print(f"Tables in database: {tables}")
    
    # Check if specific tables exist
    required_tables = ['nations', 'leaders', 'alliances', 'treaties', 'game_events', 'research_progress']
    for table in required_tables:
        if table in tables:
            print(f"✅ Table '{table}' exists")
        else:
            print(f"❌ Table '{table}' does not exist")
    
    # Get sample data from nations table
    if 'nations' in tables:
        from sqlalchemy.orm import Session
        from backend.database.models import Nation
        
        with Session(engine) as session:
            nations = session.query(Nation).all()
            print(f"\nNations in database ({len(nations)}):")
            for nation in nations:
                print(f"  - {nation.name} (GDP: {nation.gdp}, Military Power: {nation.military_power})")

if __name__ == "__main__":
    print("Checking database connection and tables...")
    check_database()
    print("\nDatabase check complete!") 