#!/usr/bin/env python3
"""
Alternative authentication method using browser-based OAuth
"""

import sys
import webbrowser
from urllib.parse import parse_qs, urlparse

def browser_auth_guide():
    print("Alternative Authentication Method")
    print("=" * 35)
    print()
    print("Since the standard token method isn't working, try this:")
    print()
    print("1. **Manual App Password Method:**")
    print("   - Go to: https://myaccount.google.com/apppasswords")
    print("   - Sign in to your Google account")
    print("   - Click 'Generate app password'")
    print("   - Select 'Other (Custom name)'")
    print("   - Enter: 'Google Keep MCP'")
    print("   - Copy the 16-character password")
    print("   - Use this password in the token generator")
    print()
    print("2. **Check Account Type:**")
    print("   - Personal Gmail: Should work with app passwords")
    print("   - Google Workspace: May need admin approval")
    print("   - School/Work account: May be restricted")
    print()
    print("3. **Try Browser Login First:**")
    print("   - Visit: https://keep.google.com")
    print("   - Sign in and verify access works")
    print("   - Then try token generation again")
    print()
    
    choice = input("Open Google App Passwords page? (y/n): ").lower()
    if choice == 'y':
        webbrowser.open('https://myaccount.google.com/apppasswords')
        print("✅ Opened in browser. Generate an app password and try again.")

if __name__ == "__main__":
    browser_auth_guide()