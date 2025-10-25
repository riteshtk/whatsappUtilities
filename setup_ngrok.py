#!/usr/bin/env python3
"""
Simple script to help set up ngrok URL for WhatsApp media files.
This script will help you get your ngrok URL and update your .env file.
"""

import os
import subprocess
import sys
import re
from pathlib import Path

def get_ngrok_url():
    """Get the current ngrok URL."""
    try:
        # Try to get ngrok URL from ngrok API
        import requests
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        if response.status_code == 200:
            data = response.json()
            tunnels = data.get("tunnels", [])
            for tunnel in tunnels:
                if tunnel.get("proto") == "https":
                    return tunnel.get("public_url")
    except:
        pass
    
    # Fallback: try to get from ngrok status
    try:
        result = subprocess.run(["ngrok", "api", "tunnels"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            # Parse the output to find the HTTPS URL
            lines = result.stdout.split('\n')
            for line in lines:
                if 'https://' in line and '.ngrok.io' in line:
                    match = re.search(r'https://[a-zA-Z0-9-]+\.ngrok\.io', line)
                    if match:
                        return match.group(0)
    except:
        pass
    
    return None

def update_env_file(ngrok_url):
    """Update the .env file with the ngrok URL."""
    env_file = Path("backend/.env")
    if not env_file.exists():
        print("❌ .env file not found. Please create it from .env.example first.")
        return False
    
    # Read current .env file
    with open(env_file, 'r') as f:
        lines = f.readlines()
    
    # Update or add MEDIA_BASE_URL
    updated = False
    for i, line in enumerate(lines):
        if line.startswith("MEDIA_BASE_URL="):
            lines[i] = f"MEDIA_BASE_URL={ngrok_url}\n"
            updated = True
            break
    
    if not updated:
        lines.append(f"MEDIA_BASE_URL={ngrok_url}\n")
    
    # Write back to file
    with open(env_file, 'w') as f:
        f.writelines(lines)
    
    return True

def main():
    print("🔧 WhatsApp Media URL Setup")
    print("=" * 40)
    
    # Check if ngrok is running
    ngrok_url = get_ngrok_url()
    
    if not ngrok_url:
        print("❌ ngrok is not running or not accessible.")
        print("\n📋 To fix this:")
        print("1. Start your backend: cd backend && python -m uvicorn app.main:app --reload")
        print("2. In another terminal, start ngrok: ngrok http 8000")
        print("3. Run this script again: python setup_ngrok.py")
        return
    
    print(f"✅ Found ngrok URL: {ngrok_url}")
    
    # Update .env file
    if update_env_file(ngrok_url):
        print(f"✅ Updated .env file with MEDIA_BASE_URL={ngrok_url}")
        print("\n🚀 You can now send media files via WhatsApp!")
        print("   The files will be accessible at: {}/uploads/".format(ngrok_url))
    else:
        print("❌ Failed to update .env file")
    
    print("\n📝 Manual setup:")
    print("   If this script didn't work, manually add this to your backend/.env file:")
    print(f"   MEDIA_BASE_URL={ngrok_url}")

if __name__ == "__main__":
    main()