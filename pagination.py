# Scripts to paginate through Google Drive API results
import os 

import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build 

# Path to service account key 
SERVICE_ACCOUNT_FILE = "your-service-account-key"

# Google Drive Folder ID
# https://drive.google.com/drive/folders/[FOLDER_ID]
FOLDER_ID = "your-folder-id"

# Initialize Google Drive API client 
def init_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, 
        scopes=["https://www.googleapis.com/auth/drive.readonly"]
    )
    return build('drive', 'v3', credentials=creds)

# Retrieve file metadata from a google drive folder
def list_files_in_folder(service, folder_id):
    files = []
    page_token = None
    while True:
        response = service.files().list(
            q=f"'{folder_id}' in parents and mimeType = 'video/mp4'",
            spaces='drive',
            fields='nextPageToken, files(id, name)',
            pageToken=page_token
        ).execute()

        print(response)

        files.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return files 

# Generate a shareable link for a file
def generate_drive_url(file_id):
    return f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"

# Save the file data to an Excel file 
def save_to_excel(file_data, filename="file_links.xlsx"):
    df = pd.DataFrame(file_data)
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")

def main():
    service = init_drive_service()
    files = list_files_in_folder(service, FOLDER_ID)

    if not files:
        print("No files found in the specified folder")
        return 
    
    file_data = []
    for file in files:
        file_info = {
            'file_name': file['name'],
            'file_id': file['id'],
            'file_link': generate_drive_url(file['id'])
        }
        file_data.append(file_info)

    save_to_excel(file_data)

if __name__ == "__main__":
    main()