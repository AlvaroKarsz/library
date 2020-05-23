from settings import *
from functions import *
import os
usefullCommands = {
'dumpStructure':f'''pg_dump --dbname=postgresql://{settings['db']['user']}:{settings['db']['password']}@{settings['db']['host']}:{settings['db']['port']}/{settings['db']['db']} -s''',
'dumpData':f'''pg_dump --dbname=postgresql://{settings['db']['user']}:{settings['db']['password']}@{settings['db']['host']}:{settings['db']['port']}/{settings['db']['db']} --column-inserts --data-only''',
'gitAdd':f'''git add .''',
'gitPush':f'''git push''',
'gitCommit':f'''git commit -m '''
}


def checkSuccess(res):
    return True if res == 0 else False


def backupDBstructure():
    curentWD = os.getcwd()
    os.chdir(settings['db']['dir'])
    command = f'''{usefullCommands['dumpStructure']} > {settings['backups']['db_structure']}'''
    res = os.system(command)
    os.chdir(curentWD)
    return checkSuccess(res)


def backupDBdata():
    curentWD = os.getcwd()
    os.chdir(settings['db']['dir'])
    command = f'''{usefullCommands['dumpData']} > {settings['backups']['db_data']}'''
    res = os.system(command)
    os.chdir(curentWD)
    return checkSuccess(res)


def commitPushOS(commitMessage):
    if emptyStr(commitMessage):
        return False
    command = f'''{usefullCommands['gitAdd']} && {usefullCommands['gitCommit']} "{commitMessage}" && {usefullCommands['gitPush']}'''
    print(command)
    res = os.system(command)
    return checkSuccess(res)
