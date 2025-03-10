#!/usr/bin/env python
"""
Reset script for Geopolitics-2025 game.
This script resets the game data to its initial state.
"""

import os
import sys
import argparse

# Add parent directory to path so we can import from backend
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Get the project root directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def reset_database():
    """Reset the PostgreSQL database to its initial state."""
    print("\n🗄️  Resetting PostgreSQL database...")
    
    try:
        # Change to project root directory
        os.chdir(PROJECT_ROOT)
        
        # Import and run the database initialization script
        from backend.initialize_all_nations import initialize_all_nations
        
        # Initialize database with all nations and alliances
        initialize_all_nations()
        
        print("✅ PostgreSQL database reset successfully!")
        return True
    except Exception as e:
        print(f"❌ Error resetting PostgreSQL database: {e}")
        return False

def reset_redis():
    """Reset Redis to its initial state."""
    print("\n📊 Resetting Redis...")
    
    try:
        # Change to project root directory
        os.chdir(PROJECT_ROOT)
        
        # Import and run the Redis initialization script
        from backend.initialize_redis import initialize_redis
        
        # Initialize Redis with game state
        initialize_redis()
        
        print("✅ Redis reset successfully!")
        return True
    except Exception as e:
        print(f"❌ Error resetting Redis: {e}")
        return False

def reset_all():
    """Reset all game data."""
    print("\n🔄 Resetting all Geopolitics-2025 game data...\n")
    
    db_success = reset_database()
    redis_success = reset_redis()
    
    if db_success and redis_success:
        print("\n✨ All game data reset successfully! ✨")
        return True
    else:
        print("\n⚠️  Some components could not be reset.")
        return False

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Reset Geopolitics-2025 game data")
    
    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest="component", help="Component to reset")
    
    # Add reset commands
    subparsers.add_parser("all", help="Reset all game data")
    subparsers.add_parser("database", help="Reset only the database")
    subparsers.add_parser("redis", help="Reset only Redis")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute command
    if args.component == "all" or args.component is None:
        reset_all()
    elif args.component == "database":
        reset_database()
    elif args.component == "redis":
        reset_redis()
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 