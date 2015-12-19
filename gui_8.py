import sys
from Tkinter import *
import tkMessageBox
import tkFileDialog

def hello():
    mtext = ment.get()
    mLabel2 = Label(mGui, text=mtext, fg='red').pack()
    return 
def New():
    mLabel3 = Label(mGui, text='You clicked New').pack()
    return
def About():
    tkMessageBox.showinfo(title='About',message='This is my about msg!')
    return
def Quit():
    mExit = tkMessageBox.askyesno(title='Quit', message='Are you sure?')
    if mExit > 0:
        mGui.destroy()
        return
def Open():
    mOpen = tkFileDialog.askopenfile()
    mLabel4 = Label(mGui, text=mOpen).pack()
    return
    
mGui = Tk()
ment = StringVar()

mGui.geometry('450x450')

mLabel = Label(mGui,text='Iam a label').pack()
mButton = Button(mGui,text='OK',command=hello,fg='red').pack()
mEntry = Entry(mGui,textvariable=ment).pack()

#########menu############

menubar=Menu(mGui)

filemenu=Menu(menubar,tearoff=0)
filemenu.add_command(label='New',command=New)
filemenu.add_command(label='Open',command=Open)
filemenu.add_command(label='Load')
filemenu.add_command(label='Save')
filemenu.add_command(label='Close',command=Quit)
menubar.add_cascade(label='File',menu=filemenu)

helpmenu=Menu(menubar, tearoff=0)
helpmenu.add_command(label='About', command=About)
helpmenu.add_command(label='Contact')
helpmenu.add_command(label='More')
menubar.add_cascade(label='Help',menu=helpmenu)

