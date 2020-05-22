settings = {}
settings['db'] = {}
settings['db']['dir'] = "path"
settings['db']['port'] = 1111
settings['db']['db'] = 'name'
settings['db']['host'] = 'host'
settings['db']['user'] = 'username'
settings['db']['password'] = 'pass'
settings['db']['books_table'] = 't1'
settings['db']['series_table'] = 't2'
settings['db']['stories_table'] = 't3'
settings['db']['wish_table'] = 't4'


settings['maxBooksFetch'] = 1

settings['gui'] = {}
settings['gui']['width'] = 1
settings['gui']['height'] = 1
settings['gui']['popup_pad_x'] = 1
settings['gui']['popup_pad_y'] = 1
settings['gui']['popup_font_size'] = 1

settings['booksDisplayPreRow'] = 1

settings['appDir'] = 'C:/path'
settings['pics'] = {}
settings['pics']['picFolderPath'] = settings['appDir'] + 'f1/'
settings['pics']['wishFolderPath'] = settings['appDir'] + 'f2/'
settings['pics']['storiesFolderPath'] = settings['appDir'] + 'f3/'
settings['pics']['seriesFolderPath'] = settings['appDir'] + 'f4/'
settings['pics']['width'] = 1
settings['pics']['height'] = 1
settings['pics']['width_big'] =  1
settings['pics']['height_big'] =  1



settings['insertBook'] = {}
settings['insertBook']['padx_popup'] = 1
settings['insertBook']['pady_popup'] = 1


settings['insertSerie'] = {}
settings['insertSerie']['padx_popup'] = 1
settings['insertSerie']['pady_popup'] = 1


settings['insertWish'] = {}
settings['insertWish']['padx_popup'] = 1
settings['insertWish']['pady_popup'] = 1

settings['icons'] = {}
settings['icons']['width'] = 1
settings['icons']['height'] = 1
settings['icons']['folder'] = 'f/'
settings['icons']['has_been_read'] = settings['appDir'] + settings['icons']['folder'] + 'p.jpg'
settings['icons']['has_not_been_read'] = settings['appDir'] + settings['icons']['folder'] + 'p.jpg'
settings['icons']['paperback'] = settings['appDir'] + settings['icons']['folder'] + 'p.png'
settings['icons']['hardcover'] = settings['appDir'] + settings['icons']['folder'] + 'p.png'
settings['icons']['hardcover_no_dj'] = settings['appDir'] + settings['icons']['folder'] + 'p.png'
settings['icons']['has_been_ordered'] = settings['appDir'] + settings['icons']['folder'] + 'p.png'
settings['icons']['has_not_been_ordered'] = settings['appDir'] + settings['icons']['folder'] + 'p.png'

settings['errLog'] = settings['appDir'] + 'p.log'


settings['confirm'] = {}
settings['confirm']['picWidth'] = 1
settings['confirm']['picHeight'] = 1
settings['confirm']['padx_popup'] = 1
settings['confirm']['pady_popup'] = 1


settings['backups'] = {}
settings['backups']['dir'] = settings['appDir'] + 'f55/'
settings['backups']['db_structure'] = settings['backups']['dir'] + 'n.txt'
settings['backups']['db_data'] = settings['backups']['dir'] + 'n2.txt'
