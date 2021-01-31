import glob
import random
import re
import datetime
import os
import shutil
import requests
import json
import subprocess
from bs4 import BeautifulSoup
from threading import Thread
import time

def addCommaToNumber(num):
    return "{:,}".format(num)


def dd_mm_yyyyToTimestamp(date):
    return time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y").timetuple())

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
    fileName = glob.glob(fileNameWithoutExt + '.png') + glob.glob(fileNameWithoutExt + '.jpg') + glob.glob(fileNameWithoutExt + '.jpeg')
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


def moveFile(src,dst,settings,force=False):
    try:
        if force:
            os.replace(src,dst)
        else:
            os.rename(src,dst)
        return True
    except OSError as e:
        insertError(f"""Error moving file from:\n{src}\nTO\n{dst}\nError: {e}""",settings['errLog'])
        return e


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

def classHaveProperty(c,property):
    return hasattr(c, property)


def isArray(a):
    return hasattr(a, "__len__")


def fetchPic(isbn,settings):
    url = settings['api']['openLibrary']['covers'] + isbn + '-L.jpg?default=false' #default=false so if picture not exists, return 404
    res = requests.get(url = url)
    if res.status_code != 200:
        insertError(f"""Fetch error - bad status code from http request\nurl: {url}\nstatus code: {res.status_code}\nresponse: {res.text}""",settings['errLog'])
        return False

    path = settings['tmp'] + getRandomStr(45) + '.jpg'
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

    return {'rating':res['books'][0]['average_rating'], 'count':res['books'][0]['work_ratings_count']}


def getIsbn(title,author,settings):
    payload = {'key': settings['api']['goodreads']['key'], 'title':title + ' ' + author,'format':'json'}
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

def jsonIsEmpty(json):
    return json == {} or not json


def convertnameToPath(name,removeWhiteSpaces = False):
    path = name.replace(':','.').replace('<','.').replace('>','.').replace('|','.').replace('/','.').replace('"','.').replace('\\','.').replace('*','.').replace('?','.').lower()
    return re.sub('\s+','',path) if removeWhiteSpaces else path

def listDir(dir,mimeArr = None):
    ls = []
    if mimeArr:
        for mime in mimeArr:
            ls += glob.glob(dir + '/*.' + mime)
    else:
        ls += glob.glob(dir + '/*')

    return list(map(lambda it: it.replace('\\','/'), ls))


def getMD5(path,fileName):
    curentWD = os.getcwd()
    os.chdir(path)
    command = f'''certutil -hashfile {fileName} md5'''
    res = subprocess.check_output(command, shell=True)
    os.chdir(curentWD)
    res = str(res).split("\\r\\n")
    return res[1]


def clearFolder(path):
    list = os.listdir(path)
    for file in list:
        if not file.startswith('.'):
            destroyFile(path + "/" + file)


def getVarietyOfCoversFromBookNameAndAuthor(title,author,settings):
    url = settings['api']['googleBooksApi']['search'] + title + ' ' + author
    res = requests.get(url = url)
    if res.status_code != 200:
        insertError(f"""Fetch error - bad status code from http request\nurl: {url}\nstatus code: {res.status_code}\nresponse: {res.text}""",settings['errLog'])
        return False

    res = json.loads(res.content)
    coversArr = []
    tempPathVal = False
    if 'totalItems' in res and res['totalItems'] > 0 and 'items' in res and isArray(res['items']):
        for item in res['items']:
            #iterate the results
            if 'volumeInfo' not in item:
                continue #invalid - go to next iteration

            if 'title' not in item['volumeInfo']:
                continue #invalid - go to next iteration

            if not stringIncludes2WaysInsensitive(title,item['volumeInfo']['title']):
                #no match in title
                continue
            #now check if imageLinks exists - if not continue
            if 'imageLinks' not in item['volumeInfo']:
                continue

            #now check if imagelings has thumbnail property
            if 'thumbnail' not in item['volumeInfo']['imageLinks']:
                continue

            #now try to fetch the thumbnail
            res = requests.get(url = item['volumeInfo']['imageLinks']['thumbnail'])
            #bad response
            if res.status_code != 200:
                insertError(f"""Fetch error - bad status code from http request\nurl: {item['volumeInfo']['imageLinks']['thumbnail']}\nstatus code: {res.status_code}\nresponse: {res.text}""",settings['errLog'])
                continue

            #save the fetched picture
            tempPathVal = settings['tmp'] + getRandomStr(55) + '.jpg'
            try:
                open(tempPathVal, 'wb').write(res.content)
            except OSError as e:
                insertError(f"""OS error - Could not create tmp file\nerror: {e}""",settings['errLog'])
                continue

            #push the pic to array
            coversArr.append(tempPathVal) #save the pic path

            #fetched the max number of allowed covers
            if len(coversArr) >= settings["maxCoverFetch"]:
                break

    return coversArr


def getBookDescription(isbn,settings):
    url = settings['api']['googleBooksApi']['description'] + isbn
    res = requests.get(url = url)
    if res.status_code != 200:
        insertError(f"""Fetch error - bad status code from http request\nurl: {url}\nstatus code: {res.status_code}\nresponse: {res.text}""",settings['errLog'])
        return False
    res = json.loads(res.content)
    if 'items' in res:
        for i in res['items']:
            if 'volumeInfo' in i and 'description' in i['volumeInfo']:
                return i['volumeInfo']['description']
    return False

def getISBNfromGoogleApiTitle(title,author,settings):
    url = settings['api']['googleBooksApi']['search'] + title + ' ' + author
    res = requests.get(url = url)
    if res.status_code != 200:
        insertError(f"""Fetch error - bad status code from http request\nurl: {url}\nstatus code: {res.status_code}\nresponse: {res.text}""",settings['errLog'])
        return False
    res = json.loads(res.content)
    isbn = None
    if 'items' in res:
        for v in res['items']:
            if 'volumeInfo' in v:
                if 'industryIdentifiers' in v['volumeInfo']:
                    for a in v['volumeInfo']['industryIdentifiers']:
                        if 'type' in a:
                            if a['type'].lower() == 'isbn_13':
                                return a['identifier']
                            elif a['type'].lower() == 'isbn_10':
                                isbn = a['identifier']
    return isbn


def fetchCoverFromWiki(title,settings):
    url = settings['api']['wiki']['summary'] + title
    res = requests.get(url = url)
    if res.status_code != 200:
        insertError(f"""Fetch error - bad status code from http request\nurl: {url}\nstatus code: {res.status_code}\nresponse: {res.text}""",settings['errLog'])
        return False
    res = json.loads(res.content)
    picBin = None
    if 'originalimage' in res:
        if 'source' in res['originalimage']:
            url = res['originalimage']['source']
            resT = requests.get(url =  url)
            if resT.status_code != 200:
                insertError(f"""Fetch error - bad status code from http request\nurl: {url}\nstatus code: {resT.status_code}\nresponse: {resT.text}""",settings['errLog'])
            else:
                picBin = resT.content
    if not picBin:
        if 'thumbnail' in res:
            if 'source' in res['thumbnail']:
                url = res['thumbnail']['source']
                resT = requests.get(url =  url)
                if resT.status_code != 200:
                    insertError(f"""Fetch error - bad status code from http request\nurl: {url}\nstatus code: {resT.status_code}\nresponse: {resT.text}""",settings['errLog'])
                else:
                    picBin = resT.content
    if not picBin:
        return False

    path = settings['tmp'] + getRandomStr(45) + '.jpg'
    try:
        open(path, 'wb').write(picBin)
    except OSError as e:
        insertError(f"""OS error - Could not create tmp file\nerror: {e}""",settings['errLog'])
        return False
    return path


def getSeriesBook(settings,author,series):
    def fetchCoverThread(isbn,title,resultKeeper,doneArr):
        picPath = fetchPic(isbn,settings) if isbn else fetchCoverFromWiki(title,settings)
        if picPath:
            resultKeeper[title] = picPath
        doneArr.append(1)

    def getIsbnThread(title,resultKeeper,doneArr):
        isbn = getISBNfromGoogleApiTitle(title,author,settings)
        if isbn:
            resultKeeper[title] = isbn
        doneArr.append(1)


    def makeAuthorThread(authorId,page,resultKeeper,doneKeeper):
        payload = {'key': settings['api']['goodreads']['key'], 'id':authorId,'page':page}
        url = settings['api']['goodreads']['booksByAuthor']
        req = requests.get(url = url, params = payload)
        if req.status_code == 200:
            req = BeautifulSoup(req.content,"html.parser")
            req = req.find_all('book')
            req = list(map(lambda x:{'isbn10':x.find('isbn').get_text(),'isbn13':x.find('isbn13').get_text(),'title':x.find('title_without_series').get_text(),'format':x.find('format').get_text(),'publication':x.find('publication_year').get_text(),'titleWithSerie':x.find('title').get_text()} ,req))
            resultKeeper += req
        else:
            insertError(f"""Fetch error - bad status code from http request\nurl: {url}\nstatus code: {req.status_code}\nresponse: {req.text}""",settings['errLog'])

        doneKeeper.append(1)

    def isEnglish(s):
        try:
            s.encode(encoding='utf-8').decode('ascii')
            return True
        except UnicodeDecodeError:
            return False

    def numberExists(dictArr,num):
        for v in dictArr:
            if str(dictArr[v]['number']) == str(num):
                return True
        return False

    def getBookByNumber(dict,num):
        for v in dict:
            if str(dict[v]['number']) == str(num):
                return dict[v]

    def thisIsGoodFormat(f):
        f = f.lower()
        return 'hardcover' in f or 'softcover' in f or 'paperback' in f

    def saveThisBook(dict,book):
        tmp = None
        if not isEnglish(book['title']):
            return False

        if re.search('part\s?[0-9]+\s?of\s?[0-9]+',book['title'].lower()):
            return False

        if book['title'] not in dict:
            return True


        if numberExists(dict,book['number']):
            tmp = getBookByNumber(dict,book['number'])
            if not thisIsGoodFormat(tmp['format']):
                if thisIsGoodFormat(book['format']):
                    return True
            if tmp['isbn'] == '' and (book['isbn10'] or book['isbn13']):
                return True
            if tmp['format'].lower() != 'hardcover' and book['format'] == 'hardcover':
                    if tmp['isbn'] == '':
                        return True
                    else:
                        if book['isbn10'] or book['isbn13']:
                            return True
        else:
            return True

        return False

    def getBasicSerieName(serie):
        t = serie.lower().replace('trilogy','').replace('series','').replace('serie','').strip()
        t = re.sub('^a','',t).strip()
        t = re.sub('^the','',t).strip()
        return t

    def getKeyByNumber(dict,number):
        for v in dict:
            if str(dict[v]['number']) == str(number):
                return v

    def deleteBookByNumberIfExists(dict,number):
        if numberExists(dict,number):
            k = getKeyByNumber(dict,number)
            del dict[k]

    def thisIsList(t):
        if len(t.split(',')) > 0:
            if re.search("\((.*?)#(.*?)[0-9]+\s?-\s?[0-9]+\)",t):
                return True
        return False

    def getBookByName(name,arr):
        for v in arr:
            if v['title'].lower().strip() == name.lower().strip():
                return v
        return None


    def handleList(t,all):
        serieName = re.search("\((.*?)\)",t).group(1)
        serieName = re.sub('\s?,?\s?#(.*?)[0-9]+\s?-\s?[0-9]+','',serieName)
        tmp = re.sub("\((.*?)\)", "", t)
        tmp = tmp.split(',')
        t = None
        res = []
        for i,book in enumerate(tmp):
            t = getBookByName(book,all)
            if t:
                t['serie'] = serieName
                t['number'] = str(i + 1)
                res.append(t)
            else:
                res.append({'isbn10':'','isbn13':'','title':book,'format':'','publication':'','titleWithSerie':book + '(' + serieName + ' #' + str(i + 1) + ')'})
        return res


    authorId = findGoodReadsAuthorID(author,settings)
    if not authorId:
        return None
    requestsA = []
    waiter = []
    t = False
    times = 2
    for i in range(times):
        t = Thread(target = lambda:makeAuthorThread(authorId,i,requestsA,waiter))
        t.deamon = True
        t.start()

    while len(waiter) != times:
        time.sleep(0.2)
    res = list(filter(lambda a : a['title'] != a['titleWithSerie'],requestsA))

    tmp = []
    for book in res:
        if thisIsList(book['titleWithSerie']):
            tmp += handleList(book['titleWithSerie'],requestsA)
    res += tmp

    tmp = None
    for book in res:
        tmp = re.search('\((.*)\)', book['titleWithSerie'])
        if tmp:
            tmp = tmp.group(1)
            book['serie'] = re.sub("(,)?(\s)?#[0-9]+", "", tmp).strip()
            tmp = re.search('\#(.*)', tmp)
            if tmp:
                book['number'] = tmp.group(1).strip()

    series = getBasicSerieName(series)
    res = list(filter(lambda a : 'number' in a and 'serie' in a and getBasicSerieName(a['serie']) == series,res))
    match = {}

    for book in res:
        if saveThisBook(match,book):
            deleteBookByNumberIfExists(match,book['number'])
            match[book['title']] = {
            'title':book['title'],
            'number':book['number'],
            'year':book['publication'],
            'cover':'',
            'isbn':book['isbn13'] if book['isbn13'] else book['isbn10'] if book['isbn10'] else '',
            'format':book['format']
            }

    match = sorted(match.values(), key = lambda a: int(a['number']))
    isbnsToFetch = []
    for v in match:
        if v['isbn'] == '' or not thisIsGoodFormat(v['format']):
            isbnsToFetch.append(v['title'])


    requestsA = {}
    waiter = []
    times = len(isbnsToFetch)
    t = False
    for book in isbnsToFetch:
        t = Thread(target = lambda:getIsbnThread(book,requestsA,waiter))
        t.deamon = True
        t.start()

    while len(waiter) != times:
        time.sleep(0.2)

    for name in requestsA:
        for g in match:
            if g['title'] == name:
                g['isbn'] = requestsA[name]


    requestsA = {}
    waiter = []
    times = len(match)
    t = False
    for book in match:
        t = Thread(target = lambda:fetchCoverThread(book['isbn'],book['title'],requestsA,waiter))
        t.deamon = True
        t.start()

    while len(waiter) != times:
        time.sleep(0.2)

    for title in requestsA:
        for g in match:
            if g['title'] == title:
                g['cover'] = requestsA[title]
    return match

def findGoodReadsAuthorID(name,settings):
    payload = {'key': settings['api']['goodreads']['key']}
    url = settings['api']['goodreads']['authorIdByName'] + name
    req = requests.get(url = url, params = payload)
    if req.status_code == 200:
        req = BeautifulSoup(req.content,"html.parser")
        req = req.find('author')
        return req['id'] if req['id'] else None
    else:
        insertError(f"""Fetch error - bad status code from http request\nurl: {url}\nstatus code: {req.status_code}\nresponse: {req.text}""",settings['errLog'])
    return None


def getMoreBooksFromThisAuthor(author,settings):
    authorId = findGoodReadsAuthorID(author,settings)
    if not authorId:
        return None

    return fetchAuthorBooksFromGoodReads(authorId,settings)


def fetchAuthorBooksFromGoodReads(authorId,settings):
    payload = {'key': settings['api']['goodreads']['key'], 'id':authorId,'page':'1'}
    url = settings['api']['goodreads']['booksByAuthor']
    req = requests.get(url = url, params = payload)
    output = None
    if req.status_code == 200:
        req = BeautifulSoup(req.content,"html.parser")
        req = req.find_all('book')
        output = list(map(lambda x:{'ratingCount':x.find('ratings_count').get_text(),'rating':x.find('average_rating').get_text(),'description':x.find('description').get_text(),'cover':x.find('image_url').get_text(),'isbn10':x.find('isbn').get_text(),'isbn13':x.find('isbn13').get_text(),'publication':x.find('publication_year').get_text(),'title':x.find('title').get_text()} ,req))
        for book in output:
            if book['cover']:
                pic = requests.get(url =  book['cover'])
                del book['cover']
                if pic.status_code != 200:
                    insertError(f"""Fetch error - bad status code from http request\nurl: {book['cover']}\nstatus code: {pic.status_code}\nresponse: {pic.text}""",settings['errLog'])
                else:
                    id = settings['tmp'] + getRandomStr(45) + '.jpg'
                    try:
                        open(id, 'wb').write(pic.content)
                        book['cover'] = id
                    except OSError as e:
                        insertError(f"""OS error - Could not create tmp file\nerror: {e}""",settings['errLog'])
            else:
                del book['cover']

    else:
        insertError(f"""Fetch error - bad status code from http request\nurl: {url}\nstatus code: {req.status_code}\nresponse: {req.text}""",settings['errLog'])
    return output


def getPicturesFolderNameFromPath(path):
    return path.split('/')[-2]

def getnameFromfileString(str):
    return str.split('.')[0]

def cutArrToSmallerArrs(mainArr, elementsInMiniArrays):
    output = []
    for i in range(0,len(mainArr),elementsInMiniArrays):
        output.append(mainArr[i:elementsInMiniArrays + i])
    return output

def fetchRatingsByIsbnArr(isbnArr, settings):
    MAX_ISBNS_IN_HTTP_PAYLOAD = 500
    apiUrl = settings['api']['goodreads']['ratingByIsbnsArray']
    apiFormat = 'json'
    fetchedRatingsFromAPI = []
    fetchAction = ""
    isbnArr = cutArrToSmallerArrs(isbnArr, MAX_ISBNS_IN_HTTP_PAYLOAD)
    for miniArr in isbnArr: #iterate mini arrays
        apiPayload = {'key': settings['api']['goodreads']['key'], 'isbns': ','.join(miniArr), 'format': apiFormat}
        fetchAction = requests.get(url = apiUrl ,params=apiPayload)
        if fetchAction.status_code != 200 and fetchAction.status_code != 404:
            insertError(f"""Fetch error - bad status code from http request\nurl: {apiUrl}\npayload:{apiPayload}\nstatus code: {fetchAction.status_code}\nresponse: {fetchAction.text}""",settings['errLog'])
            return False
        else:
            if fetchAction.status_code == 200:
                fetchedRatingsFromAPI += json.loads(fetchAction.content)['books']
    return fetchedRatingsFromAPI
