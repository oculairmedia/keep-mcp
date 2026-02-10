#!/usr/bin/env python3
"""
Comprehensive authentication troubleshooting
"""

import gpsoauth
import sys

def test_auth_methods():
    email = "emanuvaderland@gmail.com"
    
    print("Google Keep Authentication - Comprehensive Test")
    print("=" * 50)
    print(f"Email: {email}")
    print()
    
    # Test different approaches
    passwords_to_try = [
        "znmvltnelmdqmhmo",  # Without spaces
        "znmv ltne lmdq mhmo",  # With spaces
        "znmv-ltne-lmdq-mhmo",  # With dashes
    ]
    
    for i, password in enumerate(passwords_to_try, 1):
        print(f"Test {i}: Trying password format: '{password}'")
        
        try:
            result = gpsoauth.perform_master_login(email, password, "android_id")
            
            if "Token" in result:
                print(f"✅ SUCCESS with format {i}!")
                print(f"Master Token: {result['Token']}")
                
                # Save to .env
                with open('.env', 'w') as f:
                    f.write(f"GOOGLE_EMAIL={email}\n")
                    f.write(f"GOOGLE_MASTER_TOKEN={result['Token']}\n")
                    f.write("MCP_HOST=127.0.0.1\n")
                    f.write("MCP_PORT=8000\n")
                    f.write("UNSAFE_MODE=false\n")
                
                print("✅ Saved to .env file!")
                return True
            else:
                print(f"❌ Failed: {result.get('Error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        print()
    
    print("All authentication attempts failed.")
    print("\n📋 TROUBLESHOOTING CHECKLIST:")
    print()
    print("1. ✅ App Password Generated:")
    print("   - Go to https://myaccount.google.com/apppasswords")
    print("   - Generate a NEW app password")
    print("   - Copy it EXACTLY as shown (with or without spaces)")
    print()
    print("2. ✅ Account Type Check:")
    print("   - Personal Gmail: Should work")
    print("   - Google Workspace: May need admin approval")
    print("   - Check if 2FA is enabled")
    print()
    print("3. ✅ Alternative Solutions:")
    print("   - Try a different MCP server (like Notion, Slack, etc.)")
    print("   - Use Google Keep web interface directly")
    print("   - Contact Google Support for account issues")
    print()
    print("4. ✅ Manual .env Setup:")
    print("   If you get a token from elsewhere, create .env file:")
    print(f"   GOOGLE_EMAIL={email}")
    print("   GOOGLE_MASTER_TOKEN=your_token_here")
    print()
    
    return False

if __name__ == "__main__":
    success = test_auth_methods()
    if not success:
        print("\n💡 RECOMMENDATION:")
        print("The Google Keep API authentication is notoriously difficult.")
        print("Consider using alternative note-taking MCP servers like:")
        print("- Notion MCP")
        print("- Obsidian MCP") 
        print("- Plain text file MCP")
        print("\nOr use Google Keep through the web interface.")