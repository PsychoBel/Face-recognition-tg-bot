# -*- coding: utf-8 -*-
import os
import io
import pickle
from os.path import join, dirname
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload


SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


class GoogleDriveClient	:
    def __init__(self):
        token = os.environ['GOOGLE_TOKEN']
#         creds = None
#         directory = join(dirname(__file__), "credentials") 
#         token_f = join(directory, 'token.pickle')
#         if os.path.exists(token_f):
#             with open(token_f, 'rb') as token:
#                 creds = pickle.load(token)
#         if not creds or not creds.valid:
#             if creds and creds.expired and creds.refresh_token:
#                 creds.refresh(Request())
#             else:
#                 flow = InstalledAppFlow.from_client_secrets_file(
#                     join(directory, "credentials.json"), SCOPES)
#                 creds = flow.run_local_server(port=0)
#             with open(token_f, 'wb') as token:
#                 pickle.dump(creds, token)
        self.service = build('drive', 'v3', credentials=creds)
        self.files = self.files_ids

    @property
    def files_ids(self):
        page_token = None
        response = self.service.files().list(
            spaces='drive',
            fields='nextPageToken, files(id, name)',
            pageToken=page_token).execute()

        return {file.get('name'): file.get('id') for file in response.get('files', [])}

    def download_file(self, save_dir, file_name):
        f = join(save_dir, file_name)

        try:
            os.makedirs(save_dir)
        except:
            pass

        if not os.path.exists(f):
            fh = io.FileIO(join(save_dir, file_name), 'wb')
            request = self.service.files().get_media(fileId=self.files_ids[file_name])
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
