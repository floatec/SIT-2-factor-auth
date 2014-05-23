
from Tkinter import *
from ampel import Ampel
ampel = Ampel('rot')
import thread
__author__ = 'floatec'


def login():
    Label(fenster, text="Code").grid(row=0)

    code=Label(fenster, text="...wait for second password...").grid(row=0,column=1)
    Label(fenster, text="2. Password").grid(row=1)
    anzeigeAktualisieren(False, True, False)
    
def anzeigeAktualisieren(lampeRot, lampeGelb, lampeGruen):
    if lampeRot:
        labelRot.config(background='red')
    else:
        labelRot.config(background='gray')
    if lampeGelb:
        labelGelb.config(background='yellow')
    else:
        labelGelb.config(background='gray')
    if lampeGruen:
        labelGruen.config(background='green')
    else:
        labelGruen.config(background='gray')


fenster = Tk()
fenster.geometry("600x200")
#master.configure(background='red')
userlabel=Label(fenster, text="User").grid(row=0)
user = Entry(fenster, width=70).grid(row=0, column=1)



pwdlabel = Label(fenster, text="Password").grid(row=1)
pwd = Entry(fenster, width=70).grid(row=1, column=1)
# Rahmen
frameAmpel = Frame(master=fenster, background='darkgray')
frameAmpel.place(x=500, y=20, width=40, height=100)
# Label Rot-Licht
labelRot = Label(master=frameAmpel, background='gray')
labelRot.place(x=10, y=10, width=20, height=20)
# Gelb-Licht
labelGelb = Label(master=frameAmpel, background='gray')
labelGelb.place(x=10, y=40, width=20, height=20)
# Gruen-Licht
labelGruen = Label(master=frameAmpel, background='gray')
labelGruen.place(x=10, y=70, width=20, height=20)
# Aktualisierung der Anzeige
(lampeRot, lampeGelb, lampeGruen) = ampel.getLampen()
anzeigeAktualisieren(lampeRot, lampeGelb, lampeGruen)

Button(fenster, text='Quit', command=fenster.quit).grid(row=2, column=0, sticky=W, pady=1)
Button(fenster, text='Next', command=login).grid(row=2, column=1, sticky=W, pady=1)
fenster.mainloop( )