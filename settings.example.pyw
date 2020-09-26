settings = {}
settings['db'] = {}
settings['db']['dir'] = "C:\/path"
settings['db']['port'] = 1111
settings['db']['db'] = 'books_db_name'
settings['db']['host'] = '127.0.0.1'
settings['db']['user'] = 'postgres'
settings['db']['password'] = 'pass'
settings['db']['books_table'] = 'my_books_table_name'
settings['db']['series_table'] = 'series_table_name'
settings['db']['stories_table'] = 'stories_table_name'
settings['db']['wish_table'] = 'wish_list_table_name'

settings['maxBooksFetch'] = 20
settings["maxCoverFetch"] = 9

settings['dialog'] = {}
settings['dialog']['width'] = 500
settings['dialog']['height'] = 300

settings['storiesDialog'] = {}
settings['storiesDialog']['width'] = 800
settings['storiesDialog']['height'] = 600

settings['statistics'] = {}
settings['statistics']['width'] = 900
settings['statistics']['height'] = 700

settings['gui'] = {}
settings['gui']['width'] = 1000
settings['gui']['height'] = 900
settings['gui']['popup_pad_x'] = 100
settings['gui']['popup_pad_y'] = 2
settings['gui']['popup_font_size'] = 13

settings['booksDisplayPreRow'] = 4

settings['appDir'] = 'C:/Users/app'
settings['tmp'] = settings['appDir'] + 'tmp/'
settings['pics'] = {}
settings['pics']['picFolderPath'] = settings['appDir'] + 'pictures/'
settings['pics']['wishFolderPath'] = settings['appDir'] + 'wishlist/'
settings['pics']['storiesFolderPath'] = settings['appDir'] + 'stories/'
settings['pics']['seriesFolderPath'] = settings['appDir'] + 'series/'
settings['pics']['width'] = 180
settings['pics']['height'] = 200
settings['pics']['width_big'] =  220
settings['pics']['height_big'] =  250
settings['pics']['covers_width'] = 160
settings['pics']['covers_height'] = 180
settings['pics']['blank_pic'] =  settings['appDir'] + 'generalPics/blank.jpg'

settings['insertBook'] = {}
settings['insertBook']['padx_popup'] = 100
settings['insertBook']['pady_popup'] = 50


settings['insertWish'] = {}
settings['insertWish']['padx_popup'] = 200
settings['insertWish']['pady_popup'] = 180

settings['covers'] = {}
settings['covers']['width'] = 800
settings['covers']['height'] = 900

settings['settings_popup'] = {}
settings['insertBook']['padx'] = 100
settings['insertBook']['pady'] = 50


settings['insertSerie'] = {}
settings['insertSerie']['padx_popup'] = 200
settings['insertSerie']['pady_popup'] = 270

settings['descriptions'] = {}
settings['descriptions']['width'] = 800
settings['descriptions']['height'] = 900


settings['icons'] = {}
settings['icons']['width'] = 40
settings['icons']['height'] = 40
settings['icons']['height_cover'] = 30
settings['icons']['width_cover'] = 30
settings['icons']['mini_width'] = 20
settings['icons']['mini_height'] = 20
settings['icons']['purchase_width'] = 70
settings['icons']['purchase_height'] = 40
settings['icons']['folder'] = 'icons/'
settings['icons']['has_been_read'] = settings['appDir'] + settings['icons']['folder'] + 'hasbeenread.jpg'
settings['icons']['has_not_been_read'] = settings['appDir'] + settings['icons']['folder'] + 'hasnotbeenread.jpg'
settings['icons']['paperback'] = settings['appDir'] + settings['icons']['folder'] + 'paperback.png'
settings['icons']['hardcover'] = settings['appDir'] + settings['icons']['folder'] + 'hardcoverdj.png'
settings['icons']['hardcover_no_dj'] = settings['appDir'] + settings['icons']['folder'] + 'hardcovernodj.png'
settings['icons']['has_been_ordered'] = settings['appDir'] + settings['icons']['folder'] + 'order.jpg'
settings['icons']['has_not_been_ordered'] = settings['appDir'] + settings['icons']['folder'] + 'not_order.png'
settings['icons']['delete'] = settings['appDir'] + settings['icons']['folder'] + 'delete.png'
settings['icons']['description'] = settings['appDir'] + settings['icons']['folder'] + 'description.png'
settings['icons']['alter'] = settings['appDir'] + settings['icons']['folder'] + 'edit.png'
settings['icons']['change_cover'] = settings['appDir'] + settings['icons']['folder'] + 'changecover.png'
settings['icons']['logo'] = settings['appDir'] + settings['icons']['folder'] + 'logo.ico'
settings['icons']['amazon'] = settings['appDir'] + settings['icons']['folder'] + 'amazon.png'
settings['icons']['ebay'] = settings['appDir'] + settings['icons']['folder'] + 'ebay.png'
settings['icons']['better_world_books'] = settings['appDir'] + settings['icons']['folder'] + 'better_world_books.png'
settings['icons']['book_depository'] = settings['appDir'] + settings['icons']['folder'] + 'book_depository.jpg'
settings['icons']['abebooks'] = settings['appDir'] + settings['icons']['folder'] + 'abebooks.png'

settings['errLog'] = settings['appDir'] + 'logs/'


settings['confirm'] = {}
settings['confirm']['picWidth'] = 350
settings['confirm']['picHeight'] = 450
settings['confirm']['padx_popup'] = 100
settings['confirm']['pady_popup'] = 50


settings['backups'] = {}
settings['backups']['dir'] = settings['appDir'] + 'backups/'
settings['backups']['db_structure'] = settings['backups']['dir'] + 'db_structure.txt'
settings['backups']['db_data'] = settings['backups']['dir'] + 'db_data.txt'


settings['api'] = {}
settings['api']['openLibrary'] = {}
settings['api']['openLibrary']['covers'] = 'http://covers.openlibrary.org/b/isbn/'
settings['api']['openLibrary']['data'] = 'https://openlibrary.org/api/books?jscmd=data&format=json&bibkeys=ISBN:'


settings['api']['goodreads'] = {}
settings['api']['goodreads']['key'] = 'key'
settings['api']['goodreads']['secret'] = 'secret'
settings['api']['goodreads']['ratingByIsbnsArray'] = 'https://www.goodreads.com/book/review_counts.json'
settings['api']['goodreads']['isbnByTitle'] = 'https://www.goodreads.com/book/title.json'
settings['api']['goodreads']['authorIdByName'] = 'https://www.goodreads.com/api/author_url/'
settings['api']['goodreads']['booksByAuthor'] = 'https://www.goodreads.com/author/list.xml'

settings['api']['googleBooksApi'] = {}
settings['api']['googleBooksApi']['search'] = 'https://www.googleapis.com/books/v1/volumes?maxResults=30&orderBy=relevance&printType=BOOKS&q='
settings['api']['googleBooksApi']['description'] = 'https://www.googleapis.com/books/v1/volumes?q=isbn:'

settings['stores'] = {}
settings['stores']['betterworldbooks'] = 'https://www.betterworldbooks.com/search/results?Format=Hardcover&p=1&hpp=96&q='
settings['stores']['ebay'] = 'https://www.ebay.com/sch/i.html?_from=R40&_ipg=200&_nkw='
settings['stores']['amazon'] = 'https://www.amazon.com/s?k='
settings['stores']['bookdepository'] = 'https://www.bookdepository.com/search?searchTerm='
settings['stores']['abebooks'] = 'https://www.abebooks.com/servlet/SearchResults?bi=h&kn='


settings['api']['googleDrive'] = {}
settings['api']['googleDrive']['mainFolderId'] = 'id'
settings['api']['googleDrive']['foldersList'] = ['series','pictures','stories','wishlist','icons','generalPics','backups']
