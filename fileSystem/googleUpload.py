from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/drive.metadata']


def getUploadFolderId(service):
    response = service.files().list(
        q="name = 'uploadFolder' and mimeType = 'application/vnd.google-apps.folder'").execute()
    files = response.get('files', [])
    if len(files) > 0:
        return files[0].get('id')
    # create folder if not exist
    file_metadata = {
        'name': 'uploadFolder',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body=file_metadata,
                                  fields='id').execute()
    return file.get('id')


def upload2drive(name, src):
    creds = loadCredencials()
    if creds is None:
        print("Not found credentialsGoogleApi.json. Sorry I cannot send it to Google Drive")
        return None
    service = build('drive', 'v3', credentials=creds)

    folderId = getUploadFolderId(service)
    # Call the Drive v3 API
    file_metadata = {'name': name, 'parents': [folderId]}
    media = MediaFileUpload(src)
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()

    file = service.files().get(fileId=file.get('id'), fields="webContentLink").execute()

    return file['webContentLink']


def loadCredencials():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentialsGoogleApi.json', SCOPES)
                creds = flow.run_local_server(port=0)
            except FileNotFoundError:
                return None
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds
