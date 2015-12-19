
from Tkinter import *
import tkFileDialog

class Textfield(object):
  def __init__(self, window):
    self.window = window
    window.title("text editor")
    self.scrollbar = Scrollbar(window)
    self.scrollbar.pack(side="right",fill="y")
    self.text = Text(window,yscrollcommand=self.scrollbar.set)
    self.scrollbar.config(command=self.text.yview)
    self.text.pack()
    


class Menubar(object):   
  def __init__(self, window, text):
    self.window = window
    self.text = text
    menubar = Menu(window)
    filemenu = Menu(menubar)
    filemenu.add_command(label="load",command=self.load)
    filemenu.add_command(label="save as",command=self.saveas)
    menubar.add_cascade(label="file",menu=filemenu)
    window.config(menu=menubar)

  def load(self):
    self.file = tkFileDialog.askopenfile()
    self.text.delete(1.0, END)
    if self.file:
      self.text.insert(1.0, self.file.read())

  def saveas(self):
    self.file = tkFileDialog.asksaveasfile()
    if self.file:
      self.file.write(self.text.get(1.0, END))


window =  Tk()            
textfield = Textfield(window)
menu = Menubar(window, textfield.text)
window.mainloop()
