#!/usr/bin/env python3
"""
Use the provided oauth token to get master token
"""

import gpsoauth

def get_master_token_from_oauth():
    email = "emanuvaderland@gmail.com"
    android_id = "0123456789abcdef"
    oauth_token = "oauth2_4/0AVMBsJgdz1nbK-Un7-00IfYPQB5pEe5XTVfDBZILEdSQYyutLmtttATXA5Cj05CATTdQMQ"
    
    print("🔄 Converting OAuth token to Master token...")
    print(f"Email: {email}")
    print(f"OAuth token: {oauth_token[:50]}...")
    print()
    
    try:
        # Exchange oauth_token for master_token
        print("Step 1: Exchanging oauth_token for master_token...")
        master_response = gpsoauth.exchange_token(email, oauth_token, android_id)
        
        print(f"Response: {master_response}")
        
        if 'Token' not in master_response:
            print(f"❌ Failed to get master token: {master_response}")
            return False
        
        master_token = master_response['Token']
        print(f"✅ Got master token: {master_token}")
        
        # Save to .env file
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
        print("=" * 60)
        print(f"✅ Master token: {master_token}")
        print("✅ Saved to .env file")
        print("=" * 60)
        print()
        print("🚀 Ready to start the server:")
        print("./start_http.sh")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Exception type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    get_master_token_from_oauth()