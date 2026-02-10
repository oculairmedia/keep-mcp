#!/usr/bin/env python3
"""
Get Google Master Token for emanuvaderland@gmail.com
"""

import gpsoauth
import getpass
import sys

def get_master_token_for_user():
    email = "emanuvaderland@gmail.com"
    
    print("Google Keep MCP - Master Token Generator")
    print("=" * 45)
    print(f"Email: {email}")
    print()
    print("IMPORTANT: If you have 2FA enabled, use an app-specific password!")
    print("Generate one at: https://myaccount.google.com/apppasswords")
    print()
    
    # This will need to be run interactively where you can enter the password
    password = input("Enter your Google password (or app password if 2FA enabled): ")
    
    if not password:
        print("Error: Password is required")
        return False
    
    print("\nAuthenticating...")
    
    try:
        result = gpsoauth.perform_master_login(email, password, "android_id")
        
        if "Token" in result:
            master_token = result["Token"]
            print("\n✅ SUCCESS!")
            print("=" * 60)
            print(f"Master Token: {master_token}")
            print("=" * 60)
            print()
            print("Add these to your .env file:")
            print(f"GOOGLE_EMAIL={email}")
            print(f"GOOGLE_MASTER_TOKEN={master_token}")
            print()
            
            # Write to .env file
            with open('.env', 'w') as f:
                f.write(f"# Google Keep MCP Configuration\n")
                f.write(f"MCP_HOST=127.0.0.1\n")
                f.write(f"MCP_PORT=8000\n")
                f.write(f"GOOGLE_EMAIL={email}\n")
                f.write(f"GOOGLE_MASTER_TOKEN={master_token}\n")
                f.write(f"UNSAFE_MODE=false\n")
            
            print("✅ Credentials saved to .env file!")
            return True
        else:
            print(f"\n❌ Authentication failed: {result}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error during authentication: {e}")
        return False

if __name__ == "__main__":
    print("Note: This script needs to be run in an interactive terminal.")
    print("The password input requires direct terminal access.")
    print()
    print("To run this interactively, use:")
    print("python3 get_token_for_user.py")
    print()
    print("Alternatively, use the Docker method:")
    print('docker run --rm -it --entrypoint /bin/sh python:3 -c \'pip install gpsoauth; python -c "')
    print('import getpass, gpsoauth')
    print('email = \"emanuvaderland@gmail.com\"')
    print('password = getpass.getpass(\"Password: \")')
    print('result = gpsoauth.perform_master_login(email, password, \"android_id\")')
    print('print(f\"Master token: {result[\"Token\"]}\") if \"Token\" in result else print(f\"Error: {result}\")')
    print('"\'')