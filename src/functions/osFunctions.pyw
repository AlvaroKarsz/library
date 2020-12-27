from settings import *
from functions import *
import os
import re

usefullCommands = {
'dumpDB':f'''pg_dump --dbname=postgresql://{settings['db']['user']}:{settings['db']['password']}@{settings['db']['host']}:{settings['db']['port']}/{settings['db']['db']}''',
'gitAdd':f'''git add .''',
'gitPush':f'''git push''',
'gitCommit':f'''git commit -m '''
}


def checkSuccess(res):
    return True if res == 0 else False

def escapeGitMessage(message):
    return re.sub(r'\"','\\"',message) if message else ''

def backupWholeDB():
    curentWD = os.getcwd()
    os.chdir(settings['db']['dir'])
    command = f'''{usefullCommands['dumpDB']} > {settings['backups']['db']}'''
    res = os.system(command)
    os.chdir(curentWD)
    return checkSuccess(res)

def commitPushOS(commitMessage):
    if not commitMessage or emptyStr(commitMessage):
        return False
    command = f'''cd {settings['appDir']} && {usefullCommands['gitAdd']} && {usefullCommands['gitCommit']} "{escapeGitMessage(commitMessage)}" && {usefullCommands['gitPush']}'''
    res = os.system(command)
    return checkSuccess(res)
