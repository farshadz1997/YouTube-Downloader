from pytube import YouTube
import tkinter
from tkinter import *
from tkinter import ttk
import threading
from tkinter import messagebox as msg


if __name__ == "__main__":
    #win UI
    win = Tk()
    win.title("Youtube Downloader")
    win.geometry("500x500")
    win.resizable(False, False)
    
    #title
    
    
    #URL
    label_link = Label(win, text = "Link").place(x = 45, y = 50)
    URL_VAR = StringVar()
    URL_entry = Entry(win, textvariable = URL_VAR)
    URL_entry.place(x = 115, y = 50)

    label2 = Label(win, text = "delay time:").place(x = 45, y = 90)
    delayvar = IntVar()
    delayent = Entry(win, textvariable = delayvar)
    delayent.place(x = 115, y = 90)

    command_button = ttk.Button(win, text = "Run").place(x = 100, y = 110)

    win.mainloop()
