#!/usr/bin/env python
"""
Status checking script for Geopolitics-2025 game.
This script checks the status of all components.
"""

import os
import sys
import subprocess
import json
import requests
from tabulate import tabulate

# Add parent directory to path so we can import from backend
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_command(command):
    """Run a shell command and return its output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr

def check_docker_status():
    """Check the status of Docker containers."""
    print("\n🐳 Checking Docker containers status...")
    
    # Get container status
    success, stdout, stderr = run_command("cd docker && docker-compose ps")
    
    if not success:
        print(f"Error: {stderr}")
        return False
    
    print(stdout)
    return True

def check_database_status():
    """Check the status of the PostgreSQL database."""
    print("\n🗄️  Checking PostgreSQL database status...")
    
    # Check if PostgreSQL container is running
    success, stdout, stderr = run_command("docker ps | findstr postgres")
    
    if not success or not stdout:
        print("❌ PostgreSQL container is not running.")
        return False
    
    # Check if we can connect to the database
    try:
        from backend.database.db_config import engine
        from sqlalchemy import text
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            if result.scalar() == 1:
                print("✅ PostgreSQL database is running and accessible.")
                
                # Count nations in the database
                result = connection.execute(text("SELECT COUNT(*) FROM nations"))
                nation_count = result.scalar()
                print(f"   - Nations in database: {nation_count}")
                
                # Count alliances in the database
                result = connection.execute(text("SELECT COUNT(*) FROM alliances"))
                alliance_count = result.scalar()
                print(f"   - Alliances in database: {alliance_count}")
                
                return True
            else:
                print("❌ PostgreSQL database connection test failed.")
                return False
    except Exception as e:
        print(f"❌ Error connecting to PostgreSQL database: {e}")
        return False

def check_redis_status():
    """Check the status of Redis."""
    print("\n📊 Checking Redis status...")
    
    # Check if Redis container is running
    success, stdout, stderr = run_command("docker ps | findstr redis")
    
    if not success or not stdout:
        print("❌ Redis container is not running.")
        return False
    
    # Check if we can connect to Redis
    try:
        import redis
        from backend.initialize_redis import REDIS_URL
        
        r = redis.from_url(REDIS_URL)
        if r.ping():
            print("✅ Redis is running and accessible.")
            
            # Check if game state is initialized
            game_state = r.get("game_state")
            if game_state:
                game_state = json.loads(game_state)
                print(f"   - Game state: {game_state['current_date']}, Speed: {game_state['game_speed']}")
                
                # Count nation keys
                nation_keys = r.keys("nation:*")
                print(f"   - Nations in Redis: {len(nation_keys)}")
                
                return True
            else:
                print("❌ Redis is running but game state is not initialized.")
                return False
        else:
            print("❌ Redis connection test failed.")
            return False
    except Exception as e:
        print(f"❌ Error connecting to Redis: {e}")
        return False

def check_backend_status():
    """Check the status of the backend API server."""
    print("\n🖥️  Checking backend API server status...")
    
    # Check if backend container is running
    success, stdout, stderr = run_command("docker ps | findstr backend")
    
    if not success or not stdout:
        print("❌ Backend container is not running.")
        return False
    
    # Check if backend API is accessible
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Backend API server is running and accessible.")
            print(f"   - API version: {response.json().get('version', 'unknown')}")
            print(f"   - Status: {response.json().get('status', 'unknown')}")
            return True
        else:
            print(f"❌ Backend API server returned status code {response.status_code}.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to backend API server: {e}")
        return False

def check_frontend_status():
    """Check the status of the frontend application."""
    print("\n🌐 Checking frontend application status...")
    
    # Check if frontend container is running
    success, stdout, stderr = run_command("docker ps | findstr frontend")
    
    if not success or not stdout:
        print("❌ Frontend container is not running.")
        return False
    
    # Check if frontend is accessible
    try:
        response = requests.get("http://localhost:3000")
        if response.status_code == 200:
            print("✅ Frontend application is running and accessible.")
            return True
        else:
            print(f"❌ Frontend application returned status code {response.status_code}.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to frontend application: {e}")
        return False

def main():
    """Main entry point."""
    print("\n🔍 Checking status of Geopolitics-2025 game components...\n")
    
    # Check Docker status
    docker_status = check_docker_status()
    
    # Check component status
    db_status = check_database_status()
    redis_status = check_redis_status()
    backend_status = check_backend_status()
    frontend_status = check_frontend_status()
    
    # Print summary
    print("\n📋 Status Summary:")
    
    status_table = [
        ["PostgreSQL Database", "✅ Running" if db_status else "❌ Not Running"],
        ["Redis", "✅ Running" if redis_status else "❌ Not Running"],
        ["Backend API", "✅ Running" if backend_status else "❌ Not Running"],
        ["Frontend", "✅ Running" if frontend_status else "❌ Not Running"]
    ]
    
    print(tabulate(status_table, headers=["Component", "Status"], tablefmt="grid"))
    
    # Print access URLs if components are running
    if backend_status or frontend_status:
        print("\n🔗 Access URLs:")
        if frontend_status:
            print("   - Frontend: http://localhost:3000")
        if backend_status:
            print("   - Backend API: http://localhost:8000")
    
    # Overall status
    all_running = db_status and redis_status and backend_status and frontend_status
    if all_running:
        print("\n✨ All components are running! The game is ready to play.")
    else:
        print("\n⚠️  Some components are not running. Use 'python scripts/deploy.py deploy all' to deploy all components.")

if __name__ == "__main__":
    main() 