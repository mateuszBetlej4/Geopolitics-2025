#!/usr/bin/env python3
"""
Test script for the Geopolitics 2025 system.
This script checks if all components are running and accessible.
"""

import os
import sys
import json
import time
import requests
import subprocess
from tabulate import tabulate

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5433
POSTGRES_USER = "admin"
POSTGRES_PASSWORD = "admin"
POSTGRES_DB = "geopolitics_2025"
REDIS_HOST = "localhost"
REDIS_PORT = 6379

def print_header(message):
    """Print a header message."""
    print("\n" + "=" * 80)
    print(f" {message}")
    print("=" * 80)

def check_docker_containers():
    """Check if all Docker containers are running."""
    print_header("Checking Docker Containers")
    
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}\t{{.Status}}"],
            capture_output=True,
            text=True,
            check=True
        )
        
        containers = []
        for line in result.stdout.strip().split('\n'):
            if line:
                name, status = line.split('\t', 1)
                if any(x in name for x in ['geopolitics_postgres', 'geopolitics_redis', 'geopolitics_backend', 'geopolitics_frontend']):
                    containers.append([name, status, "✅" if "Up" in status else "❌"])
        
        print(tabulate(containers, headers=["Container", "Status", "Running"]))
        
        all_running = all("Up" in row[1] for row in containers)
        if all_running:
            print("\n✅ All containers are running.")
        else:
            print("\n❌ Some containers are not running.")
            
        return all_running
    
    except subprocess.CalledProcessError as e:
        print(f"Error checking Docker containers: {e}")
        return False

def test_backend_api():
    """Test the backend API."""
    print_header("Testing Backend API")
    
    endpoints = [
        {"url": "/", "name": "Root Endpoint"},
        {"url": "/game-state", "name": "Game State Endpoint"}
    ]
    
    results = []
    all_successful = True
    
    for endpoint in endpoints:
        url = BACKEND_URL + endpoint["url"]
        try:
            response = requests.get(url, timeout=5)
            status = response.status_code
            data = response.json()
            success = status == 200
            
            if not success:
                all_successful = False
                
            results.append([
                endpoint["name"],
                url,
                status,
                "✅" if success else "❌",
                json.dumps(data, indent=2)[:50] + "..." if len(json.dumps(data, indent=2)) > 50 else json.dumps(data, indent=2)
            ])
            
        except requests.RequestException as e:
            all_successful = False
            results.append([endpoint["name"], url, "Error", "❌", str(e)])
    
    print(tabulate(results, headers=["Endpoint", "URL", "Status", "Success", "Response"]))
    
    if all_successful:
        print("\n✅ All backend API endpoints are working.")
    else:
        print("\n❌ Some backend API endpoints are not working.")
        
    return all_successful

def test_frontend():
    """Test the frontend."""
    print_header("Testing Frontend")
    
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        status = response.status_code
        success = status == 200
        
        print(f"Frontend URL: {FRONTEND_URL}")
        print(f"Status Code: {status}")
        print(f"Success: {'✅' if success else '❌'}")
        
        return success
    
    except requests.RequestException as e:
        print(f"Error accessing frontend: {e}")
        return False

def test_database():
    """Test the database connection."""
    print_header("Testing Database Connection")
    
    try:
        # Try to import psycopg2
        import psycopg2
        
        # Connect to the database
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            dbname=POSTGRES_DB
        )
        
        # Create a cursor
        cur = conn.cursor()
        
        # Execute a simple query
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        
        # Close the cursor and connection
        cur.close()
        conn.close()
        
        print(f"Database Connection: ✅")
        print(f"PostgreSQL Version: {version}")
        
        return True
    
    except ImportError:
        print("Error: psycopg2 module not found. Install it with: pip install psycopg2-binary")
        return False
    
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return False

def test_redis():
    """Test the Redis connection."""
    print_header("Testing Redis Connection")
    
    try:
        # Try to import redis
        import redis
        
        # Connect to Redis
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        
        # Ping Redis
        response = r.ping()
        
        print(f"Redis Connection: {'✅' if response else '❌'}")
        print(f"Redis Response: {response}")
        
        return response
    
    except ImportError:
        print("Error: redis module not found. Install it with: pip install redis")
        return False
    
    except Exception as e:
        print(f"Error connecting to Redis: {e}")
        return False

def main():
    """Main function."""
    print_header("Geopolitics 2025 System Test")
    
    # Check Docker containers
    containers_ok = check_docker_containers()
    
    # Test backend API
    backend_ok = test_backend_api()
    
    # Test frontend
    frontend_ok = test_frontend()
    
    # Test database
    database_ok = test_database()
    
    # Test Redis
    redis_ok = test_redis()
    
    # Print summary
    print_header("Test Summary")
    
    results = [
        ["Docker Containers", "✅" if containers_ok else "❌"],
        ["Backend API", "✅" if backend_ok else "❌"],
        ["Frontend", "✅" if frontend_ok else "❌"],
        ["Database", "✅" if database_ok else "❌"],
        ["Redis", "✅" if redis_ok else "❌"]
    ]
    
    print(tabulate(results, headers=["Component", "Status"]))
    
    # Overall result
    all_ok = containers_ok and backend_ok and frontend_ok and database_ok and redis_ok
    
    print("\n" + "=" * 80)
    if all_ok:
        print("✅ All components are working correctly!")
    else:
        print("❌ Some components are not working correctly.")
    print("=" * 80)
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main()) 