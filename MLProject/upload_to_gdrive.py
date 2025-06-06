import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Ambil credentials dari secret
credentials_json = os.environ["GDRIVE_CREDENTIALS"]
credentials_info = json.loads(credentials_json)

# Inisialisasi service Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']
credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

# Upload folder atau file
def upload_file(file_path, folder_id):
    file_name = os.path.basename(file_path)
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"✅ Uploaded {file_name} to Google Drive (ID: {file.get('id')})")

if __name__ == "__main__":
    folder_id = os.environ["GDRIVE_FOLDER_ID"]
    upload_file("mlruns/0/meta.yaml", folder_id)  
