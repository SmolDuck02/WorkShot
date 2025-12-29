# Google Drive Upload Setup

## Overview
WorkShot will now automatically upload your HTML reports to Google Drive when you stop the app (Ctrl+C) after running for more than 5 hours.

## Setup Steps

### 1. Install Dependencies
Run this command to install the Google Drive API libraries:
```bash
pip install -r requirements.txt
```

### 2. Get Google Drive API Credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select an existing one)
3. Enable the **Google Drive API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Drive API"
   - Click "Enable"
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app" as the application type
   - Name it (e.g., "WorkShot")
   - Click "Create"
5. Download the credentials:
   - Click the download button (⬇️) next to your newly created OAuth client
   - Save the file as `credentials.json` in the **WorkShot** folder (same folder as `main.py`)

### 3. First Run Authentication
The first time WorkShot tries to upload to Google Drive:
1. A browser window will open asking you to sign in to your Google account
2. Grant permission for WorkShot to access your Google Drive
3. A `token.json` file will be created automatically (stores your credentials)
4. Future uploads will happen automatically without requiring login

### 4. Security Notes
- ⚠️ **Never commit** `credentials.json` or `token.json` to git (they're already in .gitignore)
- These files contain sensitive authentication information
- Keep them secure and private

## File Locations
```
WorkShot/
├── main.py
├── upload.py
├── credentials.json     ← You need to add this
└── token.json          ← Auto-generated after first auth
```

## Testing
To test the upload without waiting 5 hours:
1. Temporarily change line 94 in `main.py` from `18000` to `10` (10 seconds instead of 5 hours)
2. Run WorkShot
3. Wait 10+ seconds, then press Ctrl+C
4. You should see the export and upload happen automatically
5. Change the value back to `18000` when done testing

## Troubleshooting

### "File not found: credentials.json"
- Make sure `credentials.json` is in the WorkShot folder
- Double-check the file name (it's case-sensitive)

### "Access denied" or authentication errors
- Delete `token.json` and try again
- Make sure you granted all permissions during the OAuth flow

### Upload takes a long time
- Normal for large HTML reports
- The upload uses resumable uploads for reliability
- Don't interrupt the process

## How It Works
When you press Ctrl+C after running WorkShot for 5+ hours:
1. ✅ WorkShot exports today's data as an HTML report
2. ✅ The report is saved to the `exports/` folder
3. ✅ The report is automatically uploaded to your Google Drive
4. ✅ The uploaded file is placed in a folder called **"WS"** in your Drive
5. ✅ If the "WS" folder doesn't exist, it will be created automatically

The local file is always saved first, so even if the upload fails, you won't lose your data!

## Important Note About Permissions
If you've already authenticated before (have a `token.json` file), you'll need to:
1. **Delete the `token.json` file** 
2. Re-authenticate the next time you run WorkShot
3. This is needed because we updated the permissions to access Drive folders

