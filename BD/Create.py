import sqlite3
from sqlite3 import Error


def sql_connection():
    try:
        con = sqlite3.connect('Dance.db')
        return con
    except Error:
        print(Error)


def sql_init(con, table):
    cursorObj = con.cursor()
    cursorObj.execute('create table if not exists ' + table)
    con.commit()


def sql_drop(con, table):
    cursorObj = con.cursor()
    cursorObj.execute('drop table if exists ' + table)
    con.commit()


con = sql_connection()
con.cursor().execute('PRAGMA foreign_keys = ON')
con.commit()

sql_drop(con, 'User')
sql_drop(con, 'Team')
sql_drop(con, 'Championship')
sql_drop(con, 'Style')
sql_drop(con, 'Ratings')
sql_drop(con, 'Jury_Stage')
sql_drop(con, 'Style_Team')
sql_drop(con, 'Champ_Team')
sql_drop(con, 'User_Team')

sql_init(con, 'User(id integer PRIMARY KEY, '
              'login text, '
              'password text, '
              'name text, '
              'email text, '
              'phone text, '
              'country text, '
              'age integer, '
              'description text, '
              'is_admin tinyint(1) DEFAULT 0)')

sql_init(con, 'Team(id integer PRIMARY KEY, '
              'name text, '
              'description text)')

sql_init(con, 'Style(id integer PRIMARY KEY, '
              'name text, '
              'description text)')

sql_init(con, 'Championship(id integer PRIMARY KEY, '
              'year integer, '
              'description text)')

sql_init(con, 'Jury_Stage(id_user integer, '
              'id_champ integer, '
              'id_style integer, '
              'FOREIGN KEY(id_user) REFERENCES User(id), '
              'FOREIGN KEY(id_champ) REFERENCES Championship(id), '
              'FOREIGN KEY(id_style) REFERENCES Style(id))')

sql_init(con, 'Style_Team_Champ(id_style integer, '
              'id_team integer, '
              'id_champ integer, '              
              'FOREIGN KEY(id_style) REFERENCES Style(id), '
              'FOREIGN KEY(id_team) REFERENCES Team(id)'
              'FOREIGN KEY(id_champ) REFERENCES Championship(id) )')

sql_init(con, 'User_Team(id_user integer, '
              'id_team integer, '
              'FOREIGN KEY(id_user) REFERENCES User(id), '
              'FOREIGN KEY(id_team) REFERENCES Team(id) )')


sql_init(con, 'Ratings(id_champ integer, '
              'id_jury integer, '
              'id_style integer, '
              'id_team integer, '
              'mark integer, '
              'stage integer, '
              'FOREIGN KEY(id_champ) REFERENCES Championship(id), '
              'FOREIGN KEY(id_jury) REFERENCES User(id), '
              'FOREIGN KEY(id_style) REFERENCES Style(id), '
              'FOREIGN KEY(id_team) REFERENCES Team(id) )')
