from tkinter import *
import os
import os.path
from tkinter import filedialog,ttk,messagebox
from PIL import Image, ImageTk
import dudak
import bigsamol
import gozluk

IMAGEPAGE2 = ""
IMAGEDIR = ""
OLDIMAGE = ""
SAVELOC = ""
CURRENTFRAME = 2
ENTRYSTATE = 1


def dudakcagir():

    if listBox.curselection() != ():
        n = listBox.curselection()
        imgname = listBox.get(n)
        dudak.dudakboya(current_var.get(), os.path.join(IMAGEDIR, imgname))
        # dudak.dudakboya(current_var.get(),OLDIMAGE)
        # image = Image.open(os.path.join(IMAGEDIR, imgname)).resize((400, 250))


def gozlukcagir():
    if listBox.curselection() != ():
        n = listBox.curselection()
        imgname = listBox.get(n)
        gozluk.gozlukekle(os.path.join(IMAGEDIR, imgname))


def bigsamolcagir():
    if listBox.curselection() != ():
        n = listBox.curselection()
        imgname = listBox.get(n)
        bigsamol.buyultkucult(os.path.join(IMAGEDIR, imgname))


def show(event):
    global OLDIMAGE
    if listBox.curselection() != ():
        n = listBox.curselection()
        imgname = listBox.get(n)
        image = Image.open(os.path.join(IMAGEDIR, imgname)).resize((400,250))
        img = ImageTk.PhotoImage(image)
        OLDIMAGE=img
        orimgLabel.config(image=img)
        orimgLabel.image = img


def raise_frame(frame):
    global CURRENTFRAME
    if frame == 1 and CURRENTFRAME == 2:
        CURRENTFRAME = 1
        frame1.tkraise()
    elif frame == 2 and CURRENTFRAME ==1:
        CURRENTFRAME = 2
        frame2.tkraise()


# GUI
mainWindow = Tk()

frame1 = Frame(mainWindow,width=500,height=500,bg="pink")
frame1.place(x=0,y=0)
frame2 = Frame(mainWindow,width=500,height=500,bg="gray55")
frame2.place(x=0,y=0)


mainWindow.geometry('500x500+150+100')
mainWindow.title('img')
mainWindow.configure(bg="gray55")


# Original image Frame
orimgFrame = Frame(frame1,width=400,height=250)
orimgFrame.configure(bg="gray55")
orimgFrame.place(x=50,y=50)
orimgLabel = Label(orimgFrame,width=400,height=250,bg="gray55",image=OLDIMAGE)
orimgLabel.place(x=0,y=0)


# Setting Frame
settingFrame = Frame(frame1,width=200,height=100)
settingFrame.configure(bg="pink")
settingFrame.place(x=250,y=350)


# Format setting
FormatLabel = Label(settingFrame,text='Renk:',font=('arial',8,'bold'),fg='red',bg ='pink')
FormatLabel.place(x=0,y=0)
current_var = StringVar()
combobox = ttk.Combobox(settingFrame, textvariable=current_var,width=9)
combobox['state'] = 'readonly'
combobox['values'] = ('red','green','purple','yellow')
combobox.current(0)
combobox.place(x=50, y=0)


# List Box
listBox = Listbox(frame1)
listBox.bind("<<ListboxSelect>>",show)
listBox.place(x=50 ,y=350, height=100,width=150)



IMAGEDIR = ''
directory = "images"
IMAGEDIR = directory
for filename in os.listdir(directory):
    listBox.insert(END, filename)
    image = Image.open(os.path.join(IMAGEDIR, filename)).resize((400, 250))
    img = ImageTk.PhotoImage(image)
    orimgLabel.config(image=img)
    orimgLabel.image = img
    OLDIMAGE = img
    listBox.select_set(0)

# Select File Button


saveAllButton = Button(settingFrame,text="Dudak",command=dudakcagir,bg="gray50",fg="white")
saveAllButton.place(x=150,y=75)

uploadAllButton = Button(settingFrame,text="Gözlük",command=gozlukcagir,bg="gray50",fg="white")
uploadAllButton.place(x=90,y=75)

boyutButton = Button(settingFrame,text="eyesize",command=bigsamolcagir,bg="gray50",fg="white")
boyutButton.place(x=30,y=75)


raise_frame(1)
mainWindow.mainloop()
