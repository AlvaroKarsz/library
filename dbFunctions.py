import json
from functions import *


def fetchAllBooks(db,settings):
    db.execute("SELECT * FROM " + settings['db']['books_table'] + ";")
    return [item for item, in db]

def fetchAllSeries(db,settings):
    db.execute("SELECT * FROM " + settings['db']['series_table'] + ";")
    return  db.fetchall()

def insertNewBook(db,settings,json):
    values = "(name,year,author,original_language,language,isbn,type,pages"
    arguments = [json['name'],json['year'],json['author'],json['oriLan'],json['lang'],json['isbn'],json['type'],json['pages']]
    if 'serie' in json:
        values += ",serie,serie_num"
        arguments += [json['serie']['id'],json['serie']['number']]
    if 'collection' in json:
        values += ",collection"
        arguments.append(True)
    if 'next' in json:
        values += ",next"
        arguments.append(json['next'])

    values += ")"

    sql = '''
    INSERT INTO ''' + settings['db']['books_table'] + values +  '''
    VALUES(''' + addMultipleS(len(arguments)) + ''')
    RETURNING id;
    '''

    db.execute(sql,arguments)
    id = db.fetchone()[0]

    if 'collection' in json:
        sql = '''
            INSERT INTO ''' + settings['db']['stories_table'] + '''
            (name,pages,parent) VALUES  ''' + jsonToValues(len(json['collection']),3) + ''';'''
        json['collection'] = addValueToEachJson(json['collection'],'id',id)
        args = convertJsonToFlatArray(json['collection'])
        db.execute(sql,args)

    if 'prev' in json:
        sql = '''
        UPDATE ''' + settings['db']['books_table'] + '''
        SET next = %s
        WHERE id = %s
        '''
        args = [id,json['prev']]
        db.execute(sql,args)

def jsonToValues(totalArguments,numOfArgumentsEach):
    return (("(" + addMultipleS(numOfArgumentsEach) + "),") * totalArguments)[:-1]


def addMultipleS(num):
    return ("%s," * num)[:-1]

def convertJsonToFlatArray(arr):
    return [item for items in map(lambda a: a.values(),arr) for item in items]

def addValueToEachJson(arr,key,val):
    for miniJson in arr:
        miniJson[key] = val
    return arr

def getBookNames(db,settings):
    sql = '''
        SELECT
        t1.id,
        REGEXP_REPLACE(
        CONCAT_WS(
        ' - ',
        CONCAT_WS(' ',t2.name,t1.serie_num),
        t1.name || ' - ' || t1.author || '(' || t1.year || ')'
        ),
        '^\s-\s',
        ''
        )

         FROM ''' +  settings['db']['books_table'] + '''  t1
         LEFT JOIN ''' + settings['db']['series_table'] + ''' t2
         ON t2.id =t1.serie
         ORDER BY t1.id;'''
    db.execute(sql);
    return db.fetchall()

def previousBookAlreadyHaveFollow(db,settings,previuos):
    sql = '''
    SELECT EXISTS(
        SELECT 1 FROM ''' + settings['db']['books_table'] + '''
        WHERE id = %s AND next IS NOT NULL
    );
    '''
    db.execute(sql,[previuos]);
    return db.fetchone()[0]

def buildJsonFromSingleRow(columns,row):
    i = 0
    size = len(columns)
    rowTemp = {}
    while i < size:
        rowTemp[columns[i]] = row[i]
        i += 1
    return rowTemp

def postgresResultToColumnRowJson(columns,rows):
    columns = list( map( lambda a: a[0], [ list(x) for x in columns ] ))
    return list (map( lambda row : buildJsonFromSingleRow(columns,row) , rows)  )

def fetchMyLibrary(db,settings):
    sql = '''
    SELECT
        id,
        name,
        author,
        pages,
        year
        FROM ''' + settings['db']['books_table'] + '''
        ORDER BY
        id;
        '''
    db.execute(sql)
    rows = db.fetchall()
    columns = db.description
    return postgresResultToColumnRowJson(columns,rows)


def fetchBookById(db,settings,id):
    sql = '''
    SELECT
        my_books_main.id AS id,
        my_books_main.name AS name,
        my_books_main.year AS year,
        my_books_main.author AS author,
        my_books_main.language AS language,
        my_books_main.original_language AS o_language,
        my_books_main.isbn AS isbn,
        my_books_main.type AS type,
        my_books_main.pages AS pages,
        my_books_main.read_order AS read,
        my_books_main.listed_date AS listed_date,
        my_books_main.serie_num AS serie_num,
        series_table.name AS serie,
        my_books_entry1.id AS next_id,
        my_books_entry1.name AS next_name,
        my_books_entry1.author AS next_author,
        my_books_entry2.id AS prev_id,
        my_books_entry2.name AS prev_name,
        my_books_entry2.author AS prev_author,
        JSON_STRIP_NULLS(
            JSON_AGG(
                JSONB_BUILD_OBJECT(
                    'name',
                    stories_table.name,
                    'pages',
                    stories_table.pages
                )
            )
        ) AS stories

        FROM ''' + settings['db']['books_table'] + ''' my_books_main

        LEFT JOIN ''' +  settings['db']['books_table'] + ''' my_books_entry1
        ON my_books_main.next = my_books_entry1.id

        LEFT JOIN ''' + settings['db']['series_table']  + ''' series_table
        ON my_books_main.serie = series_table.id

        LEFT JOIN ''' + settings['db']['stories_table']  + ''' stories_table
        ON my_books_main.id = stories_table.parent

        LEFT JOIN ''' +  settings['db']['books_table'] + ''' my_books_entry2
        ON my_books_main.id = my_books_entry2.next
        WHERE my_books_main.id = %s
        GROUP BY
        my_books_main.id,
        my_books_main.name,
        my_books_main.year,
        my_books_main.author,
        my_books_main.language,
        my_books_main.original_language,
        my_books_main.isbn,
        my_books_main.type,
        my_books_main.pages,
        my_books_main.read_order,
        my_books_main.serie_num,
        series_table.name,
        my_books_main.listed_date,
        my_books_entry1.id,
        my_books_entry1.name,
        my_books_entry1.author,
        my_books_entry2.id,
        my_books_entry2.name,
        my_books_entry2.author
        '''
    db.execute(sql,[id])
    rows = [db.fetchone()]
    columns = db.description
    return postgresResultToColumnRowJson(columns,rows)[0]


def markBookAsReaded(db,settings,bookID,date):
    sql = '''
    UPDATE ''' + settings['db']['books_table'] + '''
        SET read_order =
            (
                (
                SELECT read_order FROM ''' + settings['db']['books_table'] + '''
                WHERE read_order IS NOT NULL
                ORDER BY read_order DESC
                LIMIT 1
                ) + 1
            ),
        read_date = %s
    WHERE id = %s
    RETURNING read_order;
    '''
    db.execute(sql,[date,bookID])
    return db.fetchone()[0]


def markWishAsOrdered(db,settings,bookID):
    date = makeReadableTime()
    sql = '''
    UPDATE ''' + settings['db']['wish_table'] + '''
        SET ordered = 't',
        order_date = %s
    WHERE id = %s;
    '''
    try:
        db.execute(sql,[date,bookID])
        return True
    except Exception as err:
        return err


def markThisBookSecondOrder(db,settings,bookID):
    date = makeReadableTime()
    sql = '''
    UPDATE ''' + settings['db']['wish_table'] + '''
        SET order_date_2 = %s
    WHERE id = %s;
    '''
    try:
        db.execute(sql,[date,bookID])
        return True
    except Exception as err:
        return err


def fetchAllMySeries(db,settings):
    sql = '''
    SELECT
        ser.id,
        ser.name,
        ser.author,
        (
            SELECT COUNT(1)
            FROM ''' + settings['db']['books_table'] + '''
            WHERE serie = ser.id
        ) AS books,
        (
            SELECT COUNT(1)
            FROM ''' + settings['db']['books_table'] + '''
            WHERE serie = ser.id AND read_order IS NOT NULL
        ) AS books_read,
        (
            SELECT COUNT(1)
            FROM ''' + settings['db']['wish_table'] + '''
            WHERE serie = ser.id
        ) AS wish_books
        FROM ''' + settings['db']['series_table'] + ''' ser
        ORDER BY ser.id;
    '''
    db.execute(sql)
    rows = db.fetchall()
    columns = db.description
    return postgresResultToColumnRowJson(columns,rows)


def fetchSerieById(db,settings,id):
    sql = '''
    SELECT
        ser.id,
        ser.name,
        ser.author,
        (
            SELECT COUNT(1)
            FROM ''' + settings['db']['books_table'] + '''
            WHERE serie = ser.id
        ) AS books,
        (
            SELECT COUNT(1)
            FROM ''' + settings['db']['books_table'] + '''
            WHERE serie = ser.id AND read_order IS NOT NULL
        ) AS books_read,
        (
            SELECT COUNT(1)
            FROM ''' + settings['db']['wish_table'] + '''
            WHERE serie = ser.id
        ) AS wish_books
        FROM ''' + settings['db']['series_table'] + ''' ser
        WHERE id = %s
    '''
    db.execute(sql,[id])
    rows = [db.fetchone()]
    columns = db.description
    return postgresResultToColumnRowJson(columns,rows)[0]


def fetchAllMyStories(db,settings):
    sql = '''
    SELECT
        self.id,
        self.name,
        self.pages,
        parent.author,
        parent.name AS parent_name,
        parent.year
        FROM ''' + settings['db']['stories_table'] + ''' self
        LEFT JOIN ''' + settings['db']['books_table'] + ''' parent
        ON self.parent = parent.id
        ORDER BY
        self.id;
        '''
    db.execute(sql)
    rows = db.fetchall()
    columns = db.description
    return postgresResultToColumnRowJson(columns,rows)


def fetchMyReadList(db,settings):
    sql = '''
    SELECT
        id,
        name,
        author,
        pages,
        year,
        read_order AS read
        FROM ''' + settings['db']['books_table'] + '''
        WHERE read_order IS NOT NULL
        ORDER BY
        read_order;
        '''
    db.execute(sql)
    rows = db.fetchall()
    columns = db.description
    return postgresResultToColumnRowJson(columns,rows)


def fetchStoryById(db,settings,id):
    sql = '''
    SELECT
        my_stories_main.id AS id,
        my_stories_main.name AS name,
        my_stories_main.pages AS pages,
        my_books_main.year AS year,
        my_books_main.name AS parent_name,
        my_books_main.author AS author,
        my_books_main.language AS language,
        my_books_main.listed_date AS listed_date,
        my_books_main.original_language AS o_language,
        my_books_main.read_order AS read,
        my_stories_entry1.id AS next_id,
        my_stories_entry1.name AS next_name,
        my_stories_entry2.id AS prev_id,
        my_stories_entry2.name AS prev_name

        FROM ''' + settings['db']['stories_table'] + ''' my_stories_main

        LEFT JOIN  ''' + settings['db']['books_table'] + ''' my_books_main
        ON my_stories_main.parent = my_books_main.id

        LEFT JOIN ''' +  settings['db']['stories_table'] + ''' my_stories_entry1
        ON my_stories_entry1.id = (
            SELECT id FROM ''' + settings['db']['stories_table'] + ''' aa
            WHERE aa.parent = my_stories_main.parent
            AND
            aa.id > my_stories_main.id
            ORDER BY aa.id ASC
            LIMIT 1
        )

        LEFT JOIN ''' +  settings['db']['stories_table'] + ''' my_stories_entry2
        ON my_stories_entry2.id = (
            SELECT id FROM ''' + settings['db']['stories_table'] + ''' aaa
                WHERE aaa.parent = my_stories_main.parent
                AND
                aaa.id < my_stories_main.id
                ORDER BY aaa.id DESC
                LIMIT 1
            )
        WHERE my_stories_main.id = %s
        GROUP BY
        my_stories_main.id,
        my_stories_main.name,
        my_stories_main.pages,
        my_books_main.name,
        my_books_main.year,
        my_books_main.author,
        my_books_main.language,
        my_books_main.listed_date,
        my_books_main.original_language,
        my_books_main.read_order,
        my_stories_entry1.id,
        my_stories_entry1.name,
        my_stories_entry2.id,
        my_stories_entry2.name;
        '''
    db.execute(sql,[id])
    rows = [db.fetchone()]
    columns = db.description
    return postgresResultToColumnRowJson(columns,rows)[0]


def fetchReadById(db,settings,id):
    sql = '''
    SELECT
        main.id,
        main.name,
        main.year,
        main.author,
        main.language,
        main.original_language AS o_language,
        main.isbn,
        main.type,
        main.listed_date,
        main.pages,
        main.read_order AS read,
        main.read_date,
        JSON_STRIP_NULLS(
            JSON_AGG(
                JSONB_BUILD_OBJECT(
                    'name',
                    stories_table.name,
                    'pages',
                    stories_table.pages
                )
            )
        ) AS stories
        FROM ''' + settings['db']['books_table'] + ''' main

        LEFT JOIN ''' + settings['db']['stories_table']  + ''' stories_table
        ON main.id = stories_table.parent

        WHERE main.id = %s
        GROUP BY
        main.id,
        main.name,
        main.year,
        main.author,
        main.listed_date,
        main.language,
        main.original_language,
        main.isbn,
        main.type,
        main.pages,
        main.read_order,
        main.read_date
        '''
    db.execute(sql,[id])
    rows = [db.fetchone()]
    columns = db.description
    return postgresResultToColumnRowJson(columns,rows)[0]


def fetchMyWishlist(db,settings):
    sql = '''
    SELECT
        id,
        name,
        author,
        year
        FROM ''' + settings['db']['wish_table'] + '''
        WHERE ordered='f'
        ORDER BY
        id;
        '''
    db.execute(sql)
    rows = db.fetchall()
    columns = db.description
    return postgresResultToColumnRowJson(columns,rows)

def fetchMyOrderedlist(db,settings):
    sql = '''
    SELECT
        id,
        name,
        author,
        year,
        order_date,
        order_date_2
        FROM ''' + settings['db']['wish_table'] + '''
        WHERE ordered='t'
        ORDER BY
        id;
        '''
    db.execute(sql)
    rows = db.fetchall()
    columns = db.description
    return postgresResultToColumnRowJson(columns,rows)


def fetchWishById(db,settings,id):
    sql = '''
    SELECT
        main.id AS id,
        main.name AS name,
        main.year AS year,
        main.author AS author,
        main.ordered AS ordered,
        main.serie_num AS serie_num,
        series.name AS serie

        FROM ''' + settings['db']['wish_table'] + ''' main

        LEFT JOIN  ''' + settings['db']['series_table'] + ''' series
        ON main.serie = series.id

        WHERE main.id = %s
        GROUP BY

        main.id,
        main.name,
        main.year,
        main.author,
        main.ordered,
        main.serie_num,
        series.name;
        '''
    db.execute(sql,[id])
    rows = [db.fetchone()]
    columns = db.description
    return postgresResultToColumnRowJson(columns,rows)[0]

def fetchOrderedById(db,settings,id):
    sql = '''
    SELECT
        main.id AS id,
        main.name AS name,
        main.year AS year,
        main.author AS author,
        main.order_date AS order_date,
        main.ordered AS ordered,
        main.order_date_2 AS order_date_2,
        main.serie_num AS serie_num,
        series.name AS serie

        FROM ''' + settings['db']['wish_table'] + ''' main

        LEFT JOIN  ''' + settings['db']['series_table'] + ''' series
        ON main.serie = series.id

        WHERE main.id = %s
        GROUP BY

        main.id,
        main.name,
        main.year,
        main.ordered,
        main.author,
        main.order_date,
        main.order_date_2,
        main.serie_num,
        series.name;
        '''
    db.execute(sql,[id])
    rows = [db.fetchone()]
    columns = db.description
    return postgresResultToColumnRowJson(columns,rows)[0]


def removeBookFromWishList(db,settings,id):
    sql = '''
    DELETE FROM ''' + settings['db']['wish_table'] + '''
    WHERE id = %s;
    '''
    try:
        db.execute(sql,[id])
        return True
    except Exception as err:
        return err

def insertNewWish(db,settings,objs):
    values = "(name,year,author"
    arguments = [objs['name'],objs['year'],objs['author']]
    if 'serie' in objs:
        values += ",serie,serie_num"
        arguments += [objs['serie']['id'],objs['serie']['number']]

    values += ")"

    sql = '''
    INSERT INTO ''' + settings['db']['wish_table'] + values +  '''
    VALUES(''' + addMultipleS(len(arguments)) + ''');
    '''
    try:
        db.execute(sql,arguments)
        return True
    except Exception as err:
        return err

def insertNewSerie(db,settings,json):
        sql = '''
        INSERT INTO ''' + settings['db']['series_table'] +  '''(name,author)
        VALUES(%s,%s);
        '''
        try:
            db.execute(sql,[json['name'],json['author']])
            return True
        except Exception as err:
            return err


def deleteFromWishList(db,settings,id):
    if not id:
        return 'Error, wish list id is not a number'
    sql = '''
    DELETE FROM ''' + settings['db']['wish_table'] + '''
    WHERE id=%s;
    '''
    try:
        db.execute(sql,[id])
        return True
    except Exception as err:
        return err
