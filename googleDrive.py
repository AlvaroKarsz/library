from driveFunctions import *
from functions import *
from settings import settings
from tkinter import *
import time



def updateDriveDialog(dialog,text):
    dialog.insert(END,text)
    dialog.see(END)


def backupFilesToDrive(dialog,win, folderToBackUp):
    if folderToBackUp:
        updateDriveDialog(dialog,'Backup ' + folderToBackUp + ' folder\n\n')
    else:
        updateDriveDialog(dialog,'Backup ALL folders\n\n')

    updateDriveDialog(dialog,'Loggin in to Google Drive.\n')
    service = loginDrive()
    updateDriveDialog(dialog,'Logged into Google Drive.\n')
    updateDriveDialog(dialog,'Fetching all relevant folders from Google Drive.\n')

    #get all relevant data from drive
    folders = getFoldersFromDrive(service,settings['api']['googleDrive']['mainFolderId'])
    updateDriveDialog(dialog,'Folders found in Google Drive:\n')
    for fl in folders:
        updateDriveDialog(dialog,fl['name'] + '\n')

    updateDriveDialog(dialog,'Total: ' + str(len(folders)) + ' Folders\n\n')

    if folderToBackUp:
        updateDriveDialog(dialog, 'Keep only relevant folder ' + folderToBackUp + '\n\n')
        folders = keepRelevantFolderFromDrive(folders,folderToBackUp)


    updateDriveDialog(dialog,'Fetching all relevant files from Google Drive.\n')

    files = getFilesFromDrive(service,folders)
    updateDriveDialog(dialog,'Files found in Google Drive:\n')
    for fil in files:
        updateDriveDialog(dialog,fil['name'] + '\n')
    updateDriveDialog(dialog,'Total: ' + str(len(files)) + ' Files\n\n')


    #list of folders to backup
    foldersToBackup = settings['api']['googleDrive']['foldersList']
    updateDriveDialog(dialog,'Local folders to backup:\n')
    for fil in foldersToBackup:
        updateDriveDialog(dialog,fil + '\n')
    updateDriveDialog(dialog,'Total: ' + str(len(foldersToBackup)) + ' Folders\n\n')

    if folderToBackUp:
        updateDriveDialog(dialog, 'Keep only relevant folder ' + folderToBackUp + '\n\n')
        foldersToBackup = [folderToBackUp]


    #create unexisting folders
    updateDriveDialog(dialog,'Creating unexisting remote Folders\n')
    newFolderIdTmp = ''
    numberOfCreatedFolders = 0
    for fldr in foldersToBackup:
        if not checkIfFolderExistsInJson(fldr, folders):
            numberOfCreatedFolders += 1
            #create the folder and save the new id on folders json
            newFolderIdTmp = createFolder(service,fldr,settings['api']['googleDrive']['mainFolderId'])
            folders.append({'id':newFolderIdTmp,'name':fldr})
            updateDriveDialog(dialog,'Remote folder ' + fldr + ' created, id: ' + newFolderIdTmp + '\n')
        else:
            updateDriveDialog(dialog,'Remote folder ' + fldr + ' already exists\n')

    updateDriveDialog(dialog,str(numberOfCreatedFolders) + ' new Remote folders created\n\n')

    #get local data to backup (including MD5 generated by windows 10)
    updateDriveDialog(dialog,'List all local files to backup\n')
    localJsonData = {}
    for folder in foldersToBackup:
        updateDriveDialog(dialog,'Folder ' + folder + ':\n')
        localJsonData[folder] = list(filter(lambda a: not a.startswith('.'),list(map(lambda a: a.split('/')[-1],listDir(settings['appDir'] + folder)))))
        for f in localJsonData[folder]:
            updateDriveDialog(dialog,'File name: ' + f + ':\n')
        updateDriveDialog(dialog,str(len(localJsonData[folder])) + ' Files in folder ' + folder + ':\n\n')


    updateDriveDialog(dialog,'Generating MD5CheckSum to local files\n')
    arrTmp = []
    tmpMd5 = ''
    for val in localJsonData:
        arrTmp = []
        updateDriveDialog(dialog,'Folder ' + val + ':\n')
        for nm in localJsonData[val]:
            tmpMd5 = getMD5(settings['appDir'] + val,nm)
            arrTmp.append([nm,tmpMd5])
            updateDriveDialog(dialog,'File: ' + nm + ', Hash: ' + tmpMd5 + '\n')

        localJsonData[val] = arrTmp
        updateDriveDialog(dialog,str(len(localJsonData[val])) + ' Files in folder ' + val + ':\n\n')


    #upload non existing files or changes files (by md5)
    updateDriveDialog(dialog,'Check which file needs Backup:\n')
    backupFlag = ''
    for val in localJsonData:
        updateDriveDialog(dialog,'Folder ' + val + ':\n')
        for file in localJsonData[val]:
            updateDriveDialog(dialog,'File: ' + file[0] + '\n')
            backupFlag = backupToDriveIsNeeded(file[0],file[1], val, files,folders)
            if backupFlag:
                updateDriveDialog(dialog,'Backup is needed, Uploading file ' + file[0] + '\n')
                if backupFlag == True:
                    uploadFileToDrive(service,file[0],settings['appDir'] + val,getFolderIdByName(val,folders))
                else:
                    updateDriveDialog(dialog,'File ' + file[0] + ' exists, update is needed\n')
                    updateDriveDialog(dialog,'Deleting File ' + file[0] + ' From Remote\n')
                    deleteFileFromRemote(service,backupFlag)
                    updateDriveDialog(dialog,file[0] + ' was deleted From Remote\n')
                    updateDriveDialog(dialog,'Uploading ' + file[0] + ' to Remote\n')
                    uploadFileToDrive(service,file[0],settings['appDir'] + val,getFolderIdByName(val,folders))

                updateDriveDialog(dialog,'File ' + file[0] + ' was uploaded Successfully to Remote\n')


    #now delete files from remote that no logner exists on local
    updateDriveDialog(dialog,'\nChecking for files in remote that no longer exists in local\n')
    parentTmpHolder = ''
    for fe in files:
        parentTmpHolder = getParentNameById(fe['parents'][0],folders)
        updateDriveDialog(dialog,'Remote file ' + fe['name'] + ' in local folder ' + parentTmpHolder + '\n')
        if checkIfFileExistsInLocal(fe['name'],localJsonData[parentTmpHolder]):
            updateDriveDialog(dialog,'Remote file ' + fe['name'] + ' exists in local folder ' + parentTmpHolder + '\n')
        else:
            updateDriveDialog(dialog,'Remote file ' + fe['name'] + ' NOT exists in local folder ' + parentTmpHolder + '\n')
            updateDriveDialog(dialog,'DELETING Remote file ' + fe['name'] + ' from remote folder ' + parentTmpHolder + '\n')
            deleteFileFromRemote(service,fe['id'])
            updateDriveDialog(dialog,' Remote file ' + fe['name'] + ' from remote folder ' + parentTmpHolder + ' was DELETED\n')


    updateDriveDialog(dialog,'\nBACKUP IS DONE!\n\n')
    time.sleep(3)
    win.destroy()
