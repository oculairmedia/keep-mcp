# Google Keep Authentication Troubleshooting

## Common Issues and Solutions

### 1. **"BadAuthentication" Error**
- **Cause**: Wrong email/password or 2FA is enabled
- **Solution**: 
  - Generate an App Password at https://myaccount.google.com/apppasswords
  - Use the 16-character app password instead of your regular password

### 2. **"DeviceManagementRequiredOrSyncDisabled" Error**
- **Cause**: Google Workspace security settings
- **Solution**:
  - Go to https://admin.google.com/ac/devices/settings/general
  - Enable "Turn off mobile management (Unmanaged)"
  - Or contact your Google Workspace admin

### 3. **"CaptchaRequired" Error**
- **Cause**: Google suspects automated access
- **Solution**:
  - Sign into Gmail in a web browser first
  - Complete any captcha challenges
  - Wait 10-15 minutes then try again

### 4. **"AccountDisabled" Error**
- **Cause**: Account suspended or disabled
- **Solution**: Check your Google account status and contact Google support

## Step-by-Step Setup for 2FA Users

1. **Enable 2-Factor Authentication** (if not already enabled)
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Other (Custom name)"
   - Enter "Google Keep MCP"
   - Copy the 16-character password

3. **Use App Password**
   - When prompted for password, use the app password
   - NOT your regular Google password

## Alternative: Manual Token Setup

If automated token generation fails, you can try:

1. **Use Google Takeout API** (more complex but reliable)
2. **Use unofficial Keep web scraping** (less reliable)
3. **Use Google Apps Script** with Keep API access

## Testing Your Setup

Run this to test your credentials:
```bash
python3 debug_auth.py
```

This will show the exact error message and suggested solutions.