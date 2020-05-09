import psycopg2
from settings import settings

db = psycopg2.connect(database = settings['db']['db'], user = settings['db']['user'], password = settings['db']['password'], host = settings['db']['host'], port = settings['db']['port'])
db.autocommit = True
db = db.cursor()
