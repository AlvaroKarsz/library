from settings import *
import os
usefullCommands = {
'dumpStructure':f'''pg_dump --dbname=postgresql://{settings['db']['user']}:{settings['db']['password']}@{settings['db']['host']}:{settings['db']['port']}/{settings['db']['db']} -s''',
'dumpData':f'''pg_dump --dbname=postgresql://{settings['db']['user']}:{settings['db']['password']}@{settings['db']['host']}:{settings['db']['port']}/{settings['db']['db']} --column-inserts --data-only'''
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
