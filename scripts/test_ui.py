#!/usr/bin/env python3
"""
UI Test script for the Geopolitics 2025 system.
This script opens a browser and navigates to the frontend.
"""

import os
import sys
import time
import webbrowser
import argparse

# Configuration
FRONTEND_URL = "http://localhost:3000"

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Test the Geopolitics 2025 UI")
    parser.add_argument("--browser", help="Browser to use (chrome, firefox, edge, safari)", default=None)
    args = parser.parse_args()
    
    print(f"Opening {FRONTEND_URL} in the default browser...")
    
    if args.browser:
        # Use the specified browser
        if args.browser.lower() == "chrome":
            browser = webbrowser.get("chrome")
        elif args.browser.lower() == "firefox":
            browser = webbrowser.get("firefox")
        elif args.browser.lower() == "edge":
            browser = webbrowser.get("edge")
        elif args.browser.lower() == "safari":
            browser = webbrowser.get("safari")
        else:
            print(f"Unknown browser: {args.browser}")
            return 1
        
        browser.open(FRONTEND_URL)
    else:
        # Use the default browser
        webbrowser.open(FRONTEND_URL)
    
    print("Browser opened. Please check if the UI is working correctly.")
    print("The UI should show the Geopolitics 2025 home page.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 