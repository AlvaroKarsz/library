from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from apiclient.http import MediaFileUpload

def loginDrive() :
    #SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
    SCOPES = ['https://www.googleapis.com/auth/drive']
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
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)


def getFoldersFromDrive(service,mainParentId):
    results = service.files().list(
        pageSize=1000,
        fields="nextPageToken, files(id, name)",
        q = "mimeType = 'application/vnd.google-apps.folder' and trashed = false and '" + mainParentId + "' in parents"
        ).execute()
    items = results.get('files', [])
    return items if items else []


def getFilesFromDrive(service, folders):
    if not folders:
        return []
    qString = "trashed = false and ("
    for folder in folders:
        qString +=  " '" + folder['id'] + "' in parents or"

    qString = qString[:-2]
    qString += ")"

    results = service.files().list(
        pageSize=1000,
        fields="nextPageToken, files(id, name,parents,md5Checksum)",
        q = qString
        ).execute()
    items = results.get('files', [])
    return items if items else []


def createFolder(service,name,parentId):
    file = service.files().create(
    body = {
        'name' : name,
        'parents' : [parentId],
        'mimeType' : 'application/vnd.google-apps.folder'
    },
    fields='id'
    ).execute()
    return file.get('id')


def checkIfFolderExistsInJson(folderName,json):
    for val in json:
        if val['name'] == folderName:
            return True
    return False

def getParentNameById(id,remoteFoldersObj):
    for folder in remoteFoldersObj:
        if folder['id'] == id:
            return folder['name']
    return ''


def backupToDriveIsNeeded(localFileName,localFileMD5, localFolder, remoteFilesObj,remoteFoldersObj):
    for val in remoteFilesObj:
        if val['name'] == localFileName:#good name
            if getParentNameById(val['parents'][0],remoteFoldersObj) == localFolder:#good parent
                if val['md5Checksum'] and localFileMD5 == val['md5Checksum']:#good MD5
                    return False
                else:#file changed - need to be updated
                    return val['id']

    return True


def getMimeFromExtension(extension):
    return {
        'png': 'image/png',
        'jpeg': 'image/jpeg',
        'jpg': 'image/jpeg',
        'txt':'text/plain',
        'ico': 'image/vnd.microsoft.icon'
    }.get(extension, '')


def uploadFileToDrive(service,name,path,folderId):
    if not folderId:
        return False

    mime = getMimeFromExtension(name.split('.')[-1])
    if not mime:
        return False
    media = MediaFileUpload(path + '/' + name, mimetype = mime)
    newFileId = service.files().create(
    body={
    'name': name,
    'parents':[folderId]
    },
    media_body=media,
    fields='id'
    ).execute()


def getFolderIdByName(name,folders):
    for folder in folders:
        if folder['name'] == name:
            return folder['id']
    return ''


def deleteFileFromRemote(service,fileId):
    service.files().delete(fileId=fileId).execute()


def updateFileinDrive(service,name,path,folderId,fileId):
    service.files().delete(fileId=fileId).execute()
    return uploadFileToDrive(service,name,path,folderId)
    if not folderId:
        return False

    mime = getMimeFromExtension(name.split('.')[-1])
    if not mime:
        return False

    file = service.files().get(fileId=fileId).execute()
    file['mimeType'] = mime


    media_body = MediaFileUpload(
        path + '/' + name, mimetype=mime)

    updated_file = service.files().update(
        fileId=fileId,
        body=file,
        media_body=media_body).execute()
