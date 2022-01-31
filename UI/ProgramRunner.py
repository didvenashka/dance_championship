#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os, sys
from tkinter import *
import sqlite3
from sqlite3 import Error
from StartClass import start_page


def sql_connection():
    try:
        con = sqlite3.connect('Dance.db')
        return con
    except Error:
        print(Error)


con = sql_connection()

window = Tk()
window["bg"] = "white"
window.title("Чемпионат мира по танцам")
window.iconphoto(False, PhotoImage(file="../IMAGES/icon.png"))
window.geometry('1260x800')
window.resizable(width=False, height=False)

window.update_idletasks()
print(window.geometry())
start_page(con, window)

print(con.cursor().execute('select * from User').fetchall())
window.mainloop()  # бесконечный цикл вызова окна
con.close()
