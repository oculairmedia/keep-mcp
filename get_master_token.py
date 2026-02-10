#!/usr/bin/env python3
"""
Helper script to obtain Google Master Token for Google Keep MCP.

This script uses gpsoauth to authenticate with Google and obtain a master token
that can be used with the Google Keep API.
"""

import getpass
import sys

try:
    import gpsoauth
except ImportError:
    print("Error: gpsoauth not installed. Install it with: pip install gpsoauth")
    sys.exit(1)

def get_master_token():
    """Get Google Master Token interactively."""
    print("Google Keep MCP - Master Token Generator")
    print("=" * 45)
    print()
    print("This script will help you obtain a master token for Google Keep access.")
    print("You'll need to provide your Google account credentials.")
    print()
    print("IMPORTANT: Use an app-specific password if you have 2FA enabled!")
    print("Generate one at: https://myaccount.google.com/apppasswords")
    print()
    
    # Get credentials
    email = input("Google Email: ").strip()
    if not email:
        print("Error: Email is required")
        return False
    
    password = getpass.getpass("Password (or App Password): ")
    if not password:
        print("Error: Password is required")
        return False
    
    print("\nAuthenticating...")
    
    try:
        # Perform master login
        result = gpsoauth.perform_master_login(email, password, "android_id")
        
        if "Token" in result:
            master_token = result["Token"]
            print("\n✅ SUCCESS!")
            print("=" * 45)
            print(f"Master Token: {master_token}")
            print("=" * 45)
            print()
            print("Save this token securely. Add it to your environment:")
            print(f"export GOOGLE_EMAIL='{email}'")
            print(f"export GOOGLE_MASTER_TOKEN='{master_token}'")
            print()
            print("Or add to your .env file:")
            print(f"GOOGLE_EMAIL={email}")
            print(f"GOOGLE_MASTER_TOKEN={master_token}")
            return True
        else:
            print(f"\n❌ Authentication failed: {result}")
            print("\nTroubleshooting:")
            print("1. Check your email and password")
            print("2. If you have 2FA, use an app-specific password")
            print("3. Enable 'Less secure app access' if needed")
            print("4. Check for 'DeviceManagementRequiredOrSyncDisabled' error")
            return False
            
    except Exception as e:
        print(f"\n❌ Error during authentication: {e}")
        return False

if __name__ == "__main__":
    success = get_master_token()
    sys.exit(0 if success else 1)