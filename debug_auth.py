#!/usr/bin/env python3
"""
Debug Google authentication issues
"""

import gpsoauth
import getpass
import sys

def debug_auth():
    email = "emanuvaderland@gmail.com"
    
    print("Google Keep Authentication Debugger")
    print("=" * 40)
    print(f"Email: {email}")
    print()
    
    password = input("Enter password: ")
    
    print("\nTrying authentication...")
    print("This will show the exact error message...")
    
    try:
        result = gpsoauth.perform_master_login(email, password, "android_id")
        print(f"\nFull result: {result}")
        
        if "Token" in result:
            print(f"\n✅ SUCCESS! Token: {result['Token']}")
        else:
            print(f"\n❌ FAILED!")
            print("Full error details:")
            for key, value in result.items():
                print(f"  {key}: {value}")
            
            # Common error solutions
            if "Error" in result:
                error = result.get("Error", "")
                print(f"\nError Analysis:")
                
                if "BadAuthentication" in error:
                    print("- Wrong email or password")
                    print("- Try using an app password if you have 2FA")
                    
                elif "DeviceManagementRequiredOrSyncDisabled" in error:
                    print("- Device management issue")
                    print("- Go to https://admin.google.com/ac/devices/settings/general")
                    print("- Turn on 'Turn off mobile management (Unmanaged)'")
                    
                elif "AccountDisabled" in error:
                    print("- Account might be disabled or suspended")
                    
                elif "CaptchaRequired" in error:
                    print("- Google requires captcha verification")
                    print("- Try logging into Gmail in a browser first")
                    
                else:
                    print(f"- Unknown error: {error}")
                    print("- Try enabling 'Less secure app access' (if available)")
                    print("- Generate an app password at https://myaccount.google.com/apppasswords")
            
    except Exception as e:
        print(f"\n❌ Exception occurred: {e}")
        print(f"Exception type: {type(e).__name__}")

if __name__ == "__main__":
    debug_auth()