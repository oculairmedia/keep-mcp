#!/usr/bin/env python3
"""
Alternative Google Authentication Flow using oauth_token cookie
Based on: https://github.com/simon-weber/gpsoauth#alternative-flow
"""

import gpsoauth
import webbrowser
import sys

def get_oauth_token_instructions():
    """Provide step-by-step instructions to get oauth_token"""
    print("🔐 Alternative Google Authentication Flow")
    print("=" * 45)
    print()
    print("This method works when app passwords fail!")
    print()
    print("📋 STEP-BY-STEP INSTRUCTIONS:")
    print()
    print("1. Open this URL in your browser:")
    print("   https://accounts.google.com/EmbeddedSetup")
    print()
    print("2. Log into your Google Account (emanuvaderland@gmail.com)")
    print()
    print("3. Click 'I agree' when prompted")
    print("   (Ignore any persistent loading screen)")
    print()
    print("4. Open Browser Developer Tools:")
    print("   - Press F12 (or Ctrl+Shift+I)")
    print("   - Go to 'Application' or 'Storage' tab")
    print("   - Look under 'Cookies' for 'accounts.google.com'")
    print("   - Find the 'oauth_token' cookie")
    print("   - Copy its VALUE (long string)")
    print()
    print("5. Paste the oauth_token value below")
    print()
    
    choice = input("Open the URL now? (y/n): ").lower()
    if choice == 'y':
        webbrowser.open('https://accounts.google.com/EmbeddedSetup')
        print("✅ Opened in browser - follow the steps above!")
        print()

def alternative_auth():
    """Perform alternative authentication using oauth_token"""
    email = "emanuvaderland@gmail.com"
    android_id = "0123456789abcdef"  # Standard android_id
    
    get_oauth_token_instructions()
    
    print("📝 Enter the oauth_token cookie value:")
    oauth_token = input("oauth_token: ").strip()
    
    if not oauth_token:
        print("❌ No token provided")
        return False
    
    print(f"\n🔄 Processing oauth_token for {email}...")
    
    try:
        # Step 1: Exchange oauth_token for master_token
        print("Step 1: Exchanging oauth_token for master_token...")
        master_response = gpsoauth.exchange_token(email, oauth_token, android_id)
        
        if 'Token' not in master_response:
            print(f"❌ Failed to get master token: {master_response}")
            return False
        
        master_token = master_response['Token']
        print(f"✅ Got master token: {master_token[:20]}...")
        
        # Save the master token - this is what we need for Google Keep
        env_content = f"""# Google Keep MCP Configuration
MCP_HOST=127.0.0.1
MCP_PORT=8000
GOOGLE_EMAIL={email}
GOOGLE_MASTER_TOKEN={master_token}
UNSAFE_MODE=false
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("\n🎉 SUCCESS!")
        print("=" * 50)
        print(f"✅ Master token obtained and saved to .env")
        print(f"✅ Email: {email}")
        print(f"✅ Master token: {master_token}")
        print("=" * 50)
        print()
        print("🚀 You can now start the Google Keep MCP server:")
        print("./start_http.sh")
        print()
        print("Or manually:")
        print("python3 -m src.server.cli --transport sse --host 127.0.0.1 --port 8000")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during authentication: {e}")
        print(f"Exception type: {type(e).__name__}")
        
        if "BadAuthentication" in str(e):
            print("\n💡 Troubleshooting:")
            print("- Make sure you copied the oauth_token correctly")
            print("- Try refreshing the page and getting a new oauth_token")
            print("- Ensure you're logged into the correct Google account")
        
        return False

def test_saved_credentials():
    """Test if saved credentials work"""
    try:
        from src.server.keep_api import get_client
        print("🧪 Testing saved credentials...")
        
        keep = get_client()
        notes = keep.find(query="", archived=False, trashed=False)
        print(f"✅ Successfully connected! Found {len(list(notes))} notes.")
        return True
        
    except Exception as e:
        print(f"❌ Credential test failed: {e}")
        return False

if __name__ == "__main__":
    print("Google Keep MCP - Alternative Authentication")
    print("=" * 45)
    print()
    
    # Check if we already have credentials
    try:
        with open('.env', 'r') as f:
            env_content = f.read()
            if 'GOOGLE_MASTER_TOKEN' in env_content:
                print("🔍 Found existing credentials in .env file")
                test_choice = input("Test existing credentials? (y/n): ").lower()
                if test_choice == 'y':
                    if test_saved_credentials():
                        print("\n✅ Existing credentials work! Server is ready.")
                        sys.exit(0)
                    else:
                        print("\n❌ Existing credentials failed. Getting new ones...")
    except FileNotFoundError:
        pass
    
    success = alternative_auth()
    
    if success:
        # Test the new credentials
        print("\n🧪 Testing new credentials...")
        if test_saved_credentials():
            print("✅ All set! Google Keep MCP is ready to use.")
        else:
            print("⚠️  Credentials saved but test failed. Try starting the server anyway.")
    else:
        print("\n❌ Authentication failed. Please try again or use a different method.")