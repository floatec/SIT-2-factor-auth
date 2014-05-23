
from Tkinter import *
import thread
__author__ = 'floatec'


def login():
    Label(master, text="Code").grid(row=0)

    code=Label(master, text="...wait for second password...").grid(row=0,column=1)
    Label(master, text="2. Password").grid(row=1)
    master.configure(background='yellow')

master = Tk()
master.configure(background='red')
userlabel=Label(master, text="User").grid(row=0)
user = Entry(master, width=70).grid(row=0, column=1)
code=Label(master, text="Code").grid(row=0)


pwdlabel = Label(master, text="Password").grid(row=1)
pwd = Entry(master, width=70).grid(row=1, column=1)



Button(master, text='Quit', command=master.quit).grid(row=2, column=0, sticky=W, pady=1)
Button(master, text='Login', command=login).grid(row=2, column=1, sticky=W, pady=1)
mainloop( )