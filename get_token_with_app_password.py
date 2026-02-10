#!/usr/bin/env python3
"""
Get master token using app password
"""

import gpsoauth

def get_token():
    email = "emanuvaderland@gmail.com"
    app_password = "znmvltnelmdqmhmo"  # Remove spaces
    
    print("Getting master token with app password...")
    print(f"Email: {email}")
    print(f"App Password: {app_password}")
    print()
    
    try:
        result = gpsoauth.perform_master_login(email, app_password, "android_id")
        
        if "Token" in result:
            master_token = result["Token"]
            print("✅ SUCCESS!")
            print("=" * 60)
            print(f"Master Token: {master_token}")
            print("=" * 60)
            
            # Create .env file
            env_content = f"""# Google Keep MCP Configuration
MCP_HOST=127.0.0.1
MCP_PORT=8000
GOOGLE_EMAIL={email}
GOOGLE_MASTER_TOKEN={master_token}
UNSAFE_MODE=false
"""
            
            with open('.env', 'w') as f:
                f.write(env_content)
            
            print("\n✅ Created .env file with your credentials!")
            print("\nYou can now start the server with:")
            print("./start_http.sh")
            print("\nOr manually:")
            print("python3 -m src.server.cli --transport sse --host 127.0.0.1 --port 8000")
            
            return True
            
        else:
            print("❌ Authentication failed:")
            for key, value in result.items():
                print(f"  {key}: {value}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    get_token()