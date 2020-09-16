import os
import os.path
import pickle
import threading

from django.conf import settings
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from .models import file

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
                    settings.GOOGLE_API_CREDENTIALS, SCOPES)
                creds = flow.run_local_server(port=0)
            except FileNotFoundError:
                return None
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def saveFile(name, src):
    with open(name, 'wb+') as destination:
        i = 0
        for chunk in src.chunks():
            destination.write(chunk)
            print("Saving... [" + str(i) + " chunk]")
            i += 1
        print("File saved! [DONE]")


def upload2drive(name, src, obj):
    creds = loadCredencials()
    if creds is None:
        print("Not found credentialsGoogleApi.json. Sorry I cannot send it to Google Drive")
        return None
    service = build('drive', 'v3', credentials=creds)

    folderId = getUploadFolderId(service)
    # Call the Drive v3 API
    file_metadata = {'name': name, 'parents': [folderId]}
    media = MediaFileUpload(src)
    files = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()

    files = service.files().get(fileId=files.get('id'), fields="webContentLink").execute()
    print(files)
    if files['webContentLink']:
        obj.upload = files['webContentLink']
        obj.save()


def uploadFile(name,src,obj,uploaded_file):
    saveFile(src, uploaded_file)
    upload2drive(name, src, obj)

def uploadFileThread(name,src,obj,uploaded_file):
    thread = UploadThread(1, "Uploding file", namef=name,  src=src, obj = obj, uploaded_file = uploaded_file)
    thread.start()


class UploadThread (threading.Thread):
   def __init__(self, threadID, name, namef, src, obj, uploaded_file):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.namef=namef
      self.src=src
      self.obj=obj
      self.uploaded_file=uploaded_file
   def run(self):
      print ("Starting " + self.name)
      uploadFile(name=self.namef,  src=self.src, obj=self.obj, uploaded_file=self.uploaded_file)
      print ("Exiting " + self.name)
