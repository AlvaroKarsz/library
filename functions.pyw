import glob
import random
import re
import datetime
import os
import shutil
import requests
import json

def decodePass(passw,separator):
    passw = passw.split(separator)
    return "".join(map(lambda a: chr(int(a)),passw))


def centerWindow(window,width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))


def getExtensionIfExist(fileNameWithoutExt):
    fileName = glob.glob(fileNameWithoutExt + '.*')
    return fileName[0].replace('\\','/') if len(fileName) > 0 else None


def findJsonByElemenyKey(object,key,value):
    size = len(object)
    counter = 0
    while counter <= size:
        if object[counter][key] and object[counter][key] == value:
            return object[counter]
        counter += 1
    return None


def findIndexByElemenyKey(object,key,value):
    size = len(object)
    counter = 0
    while counter <= size:
        if object[counter][key] and object[counter][key] == value:
            return counter
        counter += 1
    return None


def getNextValueInJsonByElementKey(object,key,value):
    size = len(object)
    counter = 0
    myIndex = None
    while counter <= size:
        if object[counter][key] and object[counter][key] == value:
            myIndex = counter
            break
        counter += 1
    if not myIndex and myIndex != 0:
        return None

    if myIndex == size - 1 :
        counter = 0
        while True:
            if object[counter]['relevant']:
                return object[counter]['id']
            counter += 1

    counter = myIndex + 1
    while True:
        if counter == size:
            counter = 0
        if object[counter]['relevant']:
            return object[counter]['id']
        counter += 1


def getPrevValueInJsonByElementKey(object,key,value):
    size = len(object)
    counter = size - 1
    myIndex = None
    while counter >= 0:
        if object[counter][key] and object[counter][key] == value:
            myIndex = counter
            break
        counter -= 1

    if not myIndex and myIndex != 0 :
        return None

    if myIndex == 0:
        counter = size - 1
        while True:
            if object[counter]['relevant']:
                return object[counter]['id']
            counter -= 1

    counter = myIndex - 1
    while True:
        if counter < 0:
            counter = size - 1
        if object[counter]['relevant']:
            return object[counter]['id']
        counter -= 1


def includeInsensitive(whole,part):
    if part.isspace() or not part:
        return True
    return True if part.lower() in whole.lower() else False


def getRandomNumber():
    return random.randrange(-50000000, 50000000)


def getRandomStr(len):
    return ''.join([random.choice('qazxswedcvfrQAZXSWEDCV9876FRTGBNHYUJMKIO0L1P2t3g4b5nhyujmkiolp') for _ in range(len)])




def roundUpDividation(a,b):
    return -(-a // b)


def clearEntry(entry):
    currentTextLength = len(entry.get())
    entry.delete(0,currentTextLength)
    entry.insert(0,'')


def notEmptyEls(arr):
    for val in arr:
        if val :
            return True
    return False


def dateForDB(date):
    if not date:
        return False

    now = datetime.datetime.now()
    date = date.lower()
    validMonths = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
    date = date.split()
    date = filter(lambda char: char != ' ' and char != '\n' and char != '\t' and char != '\r' ,date)
    date = ''.join(date)
    if re.match('^[a-z]{3}[0-9]{4}\-[a-z]{3}[0-9]{4}$',date):
        mon1 = date[0:3]
        year1 = date[3:7]
        mon2 = date[8:11]
        year2 = date[11:15]
        if mon1 not in validMonths or mon2 not in validMonths:
            return False

        if int(year1) > int(year2):
            return False

        if int(year2) > int(now.year):
            return False

        if int(year2) == int(now.year) and int(now.month - 1) < validMonths.index(mon2):
            return False

        if mon1 == mon2 and year1 == year2:
            return f'''{mon1.capitalize()} {year1}'''

        if int(year1) == int(year2) and validMonths.index(mon1) > validMonths.index(mon2):
            return False

        return f'''{mon1.capitalize()} {year1} - {mon2.capitalize()} {year1}'''

    if re.match('^[a-z]{3}[0-9]{4}$',date):
        mon = date[0:3]
        year = date[3:7]
        if mon not in validMonths:
            return False

        if int(year) > int(now.year):
            return False

        if int(year) == int(now.year) and int(now.month - 1) < validMonths.index(mon):
            return False

        return f'''{mon.capitalize()} {year}'''

    return False


def insertError(errStr,mainFolder):
    y = str(datetime.date.today().year)
    m = str(datetime.date.today().month)
    d = str(datetime.date.today().day)
    path = mainFolder

    if not os.path.exists(path + y):
        os.makedirs(path + y)
    path += y

    if not os.path.exists(path + '/' + m):
        os.makedirs(path + '/' + m)
    path += '/' + m

    path += '/' + d + '.log'

    errStr = f'''{'*' * 180}
{datetime.datetime.now()}

{errStr}
{'*' * 180}\n'''
    log = open(path, 'a')
    log.write(errStr)
    log.close()



def destroyFile(path):
    try:
        os.remove(path)
        return True
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        return e


def getExtensionFromPath(path):
    exploded = path.split('.')
    return '.' + exploded[len(exploded) - 1]


def moveFile(src,dst):
    try:
        os.rename(src,dst)
        return True
    except OSError as e:
        return e


def convertnameToPath(name):
    path = name.replace(':','.').replace('<','.').replace('>','.').replace('|','.').replace('/','.').replace('"','.').replace('\\','.').replace('*','.').replace('?','.').lower()
    return re.sub('\s+','',path)


def copyFile(src,dst):
    try:
        shutil.copyfile(src, dst)
        return True
    except shutil.Error as err:
        return err


def emptyStr(str):
    return str.isspace() or not str


def makeReadableTime():
    today = datetime.date.today()
    return str(today.day) + '/' + str(today.month) + '/' + str(today.year)


def postgresDateToHumanDate(date):
    if not date:
        return 'Unknown'

    date = str(date)
    date = date.split("-")
    date.reverse()
    return '/'.join(date)


def classHasMethod(classObject,methodName):
    attr = getattr(classObject, methodName, None)
    return callable(attr)


def isArray(a):
    return hasattr(a, "__len__")


def fetchPic(isbn,settings):
    url = settings['api']['openLibrary']['covers'] + isbn + '-L.jpg?default=false' #default=false so if picture not exists, return 404
    res = requests.get(url = url)
    if res.status_code != 200:
        insertError(f"""Fetch error - bad status code from http request\nurl: {url}\nstatus code: {res.status_code}\nresponse: {res.text}""",settings['errLog'])
        return False

    path = settings['tmp'] + getRandomStr(35) + '.jpg'
    try:
        open(path, 'wb').write(res.content)
    except OSError as e:
        insertError(f"""OS error - Could not create tmp file\nerror: {e}""",settings['errLog'])
        return False
    return path


def fetchRating(isbn,settings):
    payload = {'key': settings['api']['goodreads']['key'], 'isbns':isbn, 'format':'json'}
    url = settings['api']['goodreads']['ratingByIsbnsArray']
    res = requests.get(url = url ,params=payload)
    if res.status_code != 200:
        insertError(f"""Fetch error - bad status code from http request\nurl: {url}\npayload:{payload}\nstatus code: {res.status_code}\nresponse: {res.text}""",settings['errLog'])
        return False

    res = json.loads(res.content)

    if 'books' not in res or len(res['books']) != 1 or 'average_rating' not in res['books'][0] or 'work_reviews_count' not in res['books'][0]:
        insertError(f"""bad response from goodreads api rating - bad status code from http request\nurl: {url}\npayload:{payload}\nstatus code: {res.status_code}\nresponse: {res}""",settings['errLog'])
        return False

    return {'rating':res['books'][0]['average_rating'], 'count':'{:,}'.format(res['books'][0]['work_reviews_count'])}


def getIsbn(title,settings):
    payload = {'key': settings['api']['goodreads']['key'], 'title':title,'format':'json'}
    url = settings['api']['goodreads']['isbnByTitle']
    res = requests.get(url = url,params=payload)
    if res.status_code != 200:
        insertError(f"""Fetch error - bad status code from http request\nurl: {url}\npayload:{payload}\nstatus code: {res.status_code}\nresponse: {res.text}""",settings['errLog'])
        return False
    res = str(res.content)
    res = re.search('isbn\=[0-9]+',res)
    if not res:
        return False

    res = res.group(0)

    if not res:
        return False

    return res.replace('isbn=','')


def stringIncludes2WaysInsensitive(s1,s2):
    return s1.lower() in s2.lower() or s2.lower() in s1.lower()


def arrayIncludesPartInsensitive(needle,arr):
    #convert to array(if its not one)
    arr = arr if isArray(arr) else [arr]

    for val in arr:
        if stringIncludes2WaysInsensitive(val,needle):
            return True
    return False


def getIsbn13FromResponse(arr):
    #convert to array(if its not one)
    arr = arr if isArray(arr) else [arr]
    isbn10 = False
    isbn13 = False

    for isbnDict in arr:
        if 'type' not in isbnDict or 'identifier' not in isbnDict:
            continue #invalid

        if stringIncludes2WaysInsensitive('13',isbnDict['type']):
            isbn13 = isbnDict['identifier']
            break #isbn13 was found - now break

        elif stringIncludes2WaysInsensitive('10',isbnDict['type']):
            isbn10 = isbnDict['identifier']

    return isbn13 if isbn13 else isbn10


def improvedGetIsbn(title,author,settings):
    url = settings['api']['googleBooksApi']['search'] + title + ' ' + author
    res = requests.get(url = url)
    if res.status_code != 200:
        insertError(f"""Fetch error - bad status code from http request\nurl: {url}\nstatus code: {res.status_code}\nresponse: {res.text}""",settings['errLog'])
        return False
    res = json.loads(res.content)
    resultVal = False
    tempHolderVal = False
    if 'totalItems' in res and res['totalItems'] > 0 and 'items' in res and isArray(res['items']):
        for item in res['items']:
            #iterate the results
            if 'volumeInfo' not in item:
                continue #invalid - go to next iteration

            if 'title' not in item['volumeInfo'] or 'authors' not in item['volumeInfo'] or 'industryIdentifiers' not in item['volumeInfo']:
                continue #invalid - go to next iteration

            if stringIncludes2WaysInsensitive(title,item['volumeInfo']['title']):
                #title match - get the isbn from dict
                tempHolderVal = getIsbn13FromResponse(item['volumeInfo']['industryIdentifiers'])
                if not tempHolderVal:
                    continue #isbn not found in dict
                #isbn found - keep it in returned value
                resultVal = tempHolderVal
                if not author or arrayIncludesPartInsensitive(author,item['volumeInfo']['authors']):
                    break #best match - title and author, exit loop and return value

    #return response if found - if not try goodreads api
    return resultVal if resultVal else  getIsbn(title, settings)


def getPublicationYearFromApiResponse(str):
    str = re.search('[0-9]{4}',str)
    if str:
        str = str.group(0)

    return str

def thisCollectionNameIsStringDict(v):
    v = v.strip()
    return v.startswith('{') and v.endswith('}')


def invalidCollectionJsonToValidCollectionJson(str):
    return str.replace("\'", "\"")


def getCollectionFromApiResponse(res):
    collectionVals = None
    if 'table_of_contents' in res:
        if len(res['table_of_contents']) == 1:
            #different format - example => Contents: Rita Hayworth and Shawshank redemption - Apt pupil - The body - The breathing method - Afterword.
            collectionVals = res['table_of_contents'][0]['title'].replace('Contents:','').replace(' - Afterword','').split(' - ')
        else: #normal case
            collectionVals = []
            for collection in res['table_of_contents']:
                collectionVals += [collection['title']]


        collectionVals = map(lambda val: re.sub(r'\.$','',re.sub(r'\-\-$','',val.strip()).strip()),collectionVals)
        collectionVals = map(lambda val: json.loads(invalidCollectionJsonToValidCollectionJson(val))['title'] if thisCollectionNameIsStringDict(val) else val,collectionVals)

    return collectionVals


def getDataFromIsbn(isbn,settings):
    url = settings['api']['openLibrary']['data'] + isbn
    res = requests.get(url = url)

    if res.status_code != 200:
        insertError(f"""Fetch error - bad status code from http request\nurl: {url}\nstatus code: {res.status_code}\nresponse: {res.text}""",settings['errLog'])
        return False

    res = json.loads(res.content)
    jsonKey = f'''ISBN:{isbn}'''

    if jsonKey not in res: #empty
        return False

    bookName = res[jsonKey]['title'] if 'title' in res[jsonKey] else ''
    authors = ''

    if 'authors' in res[jsonKey]:
        for author in res[jsonKey]['authors']:
            authors += author['name'] + ' and '

    authors = authors[:-5] if authors else authors #remove last ' and '

    bookYear = getPublicationYearFromApiResponse(res[jsonKey]['publish_date']) if 'publish_date' in res[jsonKey] else ''
    bookPages = res[jsonKey]['number_of_pages'] if 'number_of_pages' in res[jsonKey] else ''
    collectionVals = getCollectionFromApiResponse(res[jsonKey])

    return {'name': bookName , 'author':authors, 'year':bookYear,'pages':bookPages,'collection':collectionVals}
