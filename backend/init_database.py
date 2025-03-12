from database.db_config import init_db, populate_initial_data

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database schema created successfully!")
    
    print("Populating database with initial data...")
    populate_initial_data()
    print("Initial data populated successfully!")
    
    print("Database setup complete!") 