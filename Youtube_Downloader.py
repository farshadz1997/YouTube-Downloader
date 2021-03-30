from pytube import YouTube
import pyperclip
import tkinter as tk
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
    Label_title = Label(win, text = "Youtube Downloader", fg = "red", font = ("Times",30)).place(x = 90, y = 25)
    
    #URL
    URL_label = Label(win, text = "URL:").place(x = 70, y = 100)
    URL_VAR = StringVar()
    URL_entry = Entry(win, textvariable = URL_VAR, width = 50).place(x = 115, y = 100)
    URL_button = ttk.Button(win, text = "Get URL").place(x = 220, y = 125)
    #Paste Button
    paste_ico = PhotoImage(file = r"clipboard_paste.png")
    Paste_button = ttk.Button(win, image = paste_ico, width = 3).place(x = 420, y = 98)

    #save to
    Path_label = Label(win, text = "Save to:").place(x = 60, y = 160)
    Path_Var = StringVar()
    Path_Ent = ttk.Entry(win, textvariable = Path_Var, width = 50, state = DISABLED).place(x = 115, y = 160)
    Path_button = ttk.Button(win, text = "Save to").place(x = 220, y = 185)
    
    #Option menu
    qualities_Var = StringVar()
    qualities_Var.set("-")
    qualities_label = Label(win, text = "Qualities:").place(x = 60, y = 210)
    options = ttk.OptionMenu(win, variable = qualities_Var).place(x = 115, y = 210)
    
    #download-button
    dl_button = ttk.Button(win, text = "Download").place(x = 220, y = 420)
    #Progressbar
    pb_Var = DoubleVar()
    pb = ttk.Progressbar(win, variable = pb_Var, length = 300).place(x = 115, y = 450)


    win.mainloop()
