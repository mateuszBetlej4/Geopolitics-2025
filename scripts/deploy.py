#!/usr/bin/env python
"""
Main deployment script for Geopolitics-2025 game.
This script orchestrates the deployment of all components.
"""

import os
import sys
import argparse
import subprocess
import time

# Add parent directory to path so we can import from backend
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_command(command, description=None):
    """Run a shell command and print its output."""
    if description:
        print(f"\n=== {description} ===")
    
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    
    if result.stderr:
        print(f"Error: {result.stderr}")
    
    return result.returncode == 0

def deploy_database():
    """Deploy and initialize the PostgreSQL database."""
    print("\n🗄️  Deploying PostgreSQL database...")
    
    # Start PostgreSQL container
    if not run_command("cd docker && docker-compose up -d postgres", 
                     "Starting PostgreSQL container"):
        return False
    
    # Wait for PostgreSQL to be ready
    print("Waiting for PostgreSQL to be ready...")
    time.sleep(5)
    
    # Initialize database with all nations and alliances
    if not run_command("python -m backend.initialize_all_nations", 
                     "Initializing database with nations and alliances"):
        return False
    
    print("✅ PostgreSQL database deployed and initialized successfully!")
    return True

def deploy_redis():
    """Deploy and initialize Redis."""
    print("\n📊 Deploying Redis...")
    
    # Start Redis container
    if not run_command("cd docker && docker-compose up -d redis", 
                     "Starting Redis container"):
        return False
    
    # Wait for Redis to be ready
    print("Waiting for Redis to be ready...")
    time.sleep(3)
    
    # Initialize Redis with game state
    if not run_command("python -m backend.initialize_redis", 
                     "Initializing Redis with game state"):
        return False
    
    print("✅ Redis deployed and initialized successfully!")
    return True

def deploy_backend():
    """Deploy the backend API server."""
    print("\n🖥️  Deploying backend API server...")
    
    # Build and start backend container
    if not run_command("cd docker && docker-compose up -d backend", 
                     "Starting backend container"):
        return False
    
    print("✅ Backend API server deployed successfully!")
    return True

def deploy_frontend():
    """Deploy the frontend application."""
    print("\n🌐 Deploying frontend application...")
    
    # Build and start frontend container
    if not run_command("cd docker && docker-compose up -d frontend", 
                     "Starting frontend container"):
        return False
    
    print("✅ Frontend application deployed successfully!")
    return True

def deploy_all():
    """Deploy all components."""
    print("\n🚀 Deploying Geopolitics-2025 game...\n")
    
    if not deploy_database():
        print("❌ Failed to deploy database. Aborting deployment.")
        return False
    
    if not deploy_redis():
        print("❌ Failed to deploy Redis. Aborting deployment.")
        return False
    
    if not deploy_backend():
        print("❌ Failed to deploy backend. Aborting deployment.")
        return False
    
    if not deploy_frontend():
        print("❌ Failed to deploy frontend. Aborting deployment.")
        return False
    
    print("\n✨ Geopolitics-2025 game deployed successfully! ✨")
    print("\nAccess the game at: http://localhost:3000")
    print("Backend API available at: http://localhost:8000")
    return True

def stop_all():
    """Stop all containers."""
    print("\n🛑 Stopping all containers...")
    
    if not run_command("cd docker && docker-compose down", 
                     "Stopping all containers"):
        return False
    
    print("✅ All containers stopped successfully!")
    return True

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Deploy Geopolitics-2025 game components")
    
    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Add deploy command
    deploy_parser = subparsers.add_parser("deploy", help="Deploy components")
    deploy_parser.add_argument("component", nargs="?", default="all",
                             choices=["all", "database", "redis", "backend", "frontend"],
                             help="Component to deploy (default: all)")
    
    # Add stop command
    stop_parser = subparsers.add_parser("stop", help="Stop all containers")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute command
    if args.command == "deploy":
        if args.component == "all":
            deploy_all()
        elif args.component == "database":
            deploy_database()
        elif args.component == "redis":
            deploy_redis()
        elif args.component == "backend":
            deploy_backend()
        elif args.component == "frontend":
            deploy_frontend()
    elif args.command == "stop":
        stop_all()
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 