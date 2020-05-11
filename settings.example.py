from functions import *

settings = {}
settings['db'] = {}
settings['db']['port'] = 1111
settings['db']['db'] = 'name'
settings['db']['host'] = 'localhost'
settings['db']['user'] = 'username'
settings['db']['passSeparator'] = '*'
settings['db']['password'] = decodePass('65*65*65*65*65*65',settings['db']['passSeparator'])
settings['db']['books_table'] = 't1'
settings['db']['series_table'] = 't2'
settings['db']['stories_table'] = 't3'

settings['maxBooksFetch'] = 20

settings['gui'] = {}
settings['gui']['width'] = 1000
settings['gui']['height'] = 900
settings['gui']['popup_pad_x'] = 100
settings['gui']['popup_pad_y'] = 10
settings['gui']['popup_font_size'] = 13

settings['booksDisplayPreRow'] = 4

settings['appDir'] = 'C:/path'
settings['pics'] = {}
settings['pics']['picFolderPath'] = settings['appDir'] + 'pictures/'
settings['pics']['storiesFolderPath'] = settings['appDir'] + 'stories/'
settings['pics']['width'] = 180
settings['pics']['height'] = 200
settings['pics']['width_big'] =  220
settings['pics']['height_big'] =  250



settings['insertBook'] = {}
settings['insertBook']['padx_popup'] = 100
settings['insertBook']['pady_popup'] = 50


settings['icons'] = {}
settings['icons']['width'] = 40
settings['icons']['height'] = 40
settings['icons']['folder'] = 'icons/'
settings['icons']['has_been_read'] = settings['appDir'] + settings['icons']['folder'] + 'hasbeenread.jpg'
settings['icons']['has_not_been_read'] = settings['appDir'] + settings['icons']['folder'] + 'hasnotbeenread.jpg'
settings['icons']['paperback'] = settings['appDir'] + settings['icons']['folder'] + 'paperback.png'
settings['icons']['hardcover'] = settings['appDir'] + settings['icons']['folder'] + 'hardcoverdj.png'
settings['icons']['hardcover_no_dj'] = settings['appDir'] + settings['icons']['folder'] + 'hardcovernodj.png'
