import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
# Using drive scope to access/create folders in Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate():
    """Shows basic usage of the Drive v3 API.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def get_or_create_folder(service, folder_name='WS'):
    """Get the folder ID for the specified folder, or create it if it doesn't exist."""
    # Search for the folder
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    
    if items:
        # Folder exists, return its ID
        print(f"[+] Found existing folder '{folder_name}'")
        return items[0]['id']
    else:
        # Create the folder
        print(f"[+] Creating folder '{folder_name}'...")
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        print(f"[+] Folder created with ID: {folder.get('id')}")
        return folder.get('id')

def upload_file(file_path, folder_name='WS'):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_name = os.path.basename(file_path)
    
    # Get or create the folder
    folder_id = get_or_create_folder(service, folder_name)

    file_metadata = {
        'name': file_name,
        'parents': [folder_id]  # Upload to the specified folder
    }
    
    # You can specify mimetype if you know it, e.g., 'image/jpeg' or 'application/pdf'
    media = MediaFileUpload(file_path, resumable=True)

    print(f"Uploading {file_name} to folder '{folder_name}'...")
    
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    print(f"File ID: {file.get('id')} uploaded successfully to '{folder_name}' folder.")

if __name__ == '__main__':
    # REPLACE THIS with the path to the file you want to upload
    my_file = "./exports/rep.html" 
    
    # Create a dummy file to test if you don't have one
    if not os.path.exists(my_file):
        with open(my_file, "w") as f:
            f.write("This is a test upload to Google Drive!")

    upload_file(my_file, folder_name='WS')