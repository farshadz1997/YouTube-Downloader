from pytube import YouTube
import pyperclip
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import threading
from tkinter import messagebox as msg

def get_url():
    yt = YouTube(URL_entry.get())
    Info_Var.set(f"Title: {yt.title}\n"
                f"Length: {yt.length // 60}:{yt.length % 60}" )
        

def Save_to():
    global dir
    dir = filedialog.askdirectory()
    Path_Var.set(dir)

def Paste():
    URL_entry.delete(0, 'end')
    s = pyperclip.paste()
    URL_VAR.set(s)
    
def url_thread():
    threading.Thread(target = get_url, daemon = True).start()


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
    URL_entry = Entry(win, textvariable = URL_VAR, width = 50)
    URL_entry.place(x = 115, y = 100)
    URL_button = ttk.Button(win, text = "Get URL", command = url_thread).place(x = 220, y = 125)

    #Paste Button
    paste_ico = PhotoImage(file = r"clipboard_paste.png")
    Paste_button = ttk.Button(win, image = paste_ico, width = 3, command = Paste).place(x = 420, y = 98)
        
    #save to
    Path_label = Label(win, text = "Save to:").place(x = 60, y = 160)
    Path_Var = StringVar()
    Path_Ent = ttk.Entry(win, textvariable = Path_Var, width = 50, state = DISABLED).place(x = 115, y = 160)
    Path_button = ttk.Button(win, text = "Save to", command = Save_to).place(x = 220, y = 185)
        
    #Option menu
    qualities_Var = StringVar()
    qualities_Var.set("-")
    qualities_label = Label(win, text = "Qualities:").place(x = 60, y = 210)
    options = ttk.OptionMenu(win, variable = qualities_Var)
    options.place(x = 115, y = 210)
    
    #Video infos
    Info_Var = StringVar()
    Info_label = Message(win, textvariable = Info_Var, width = 200)
    Info_label.place(x = 60, y = 260)
        
    #download-button
    dl_button = ttk.Button(win, text = "Download").place(x = 220, y = 420)
        
    #Progressbar
    pb_Var = DoubleVar()
    pb = ttk.Progressbar(win, variable = pb_Var, length = 300).place(x = 115, y = 450)

    win.mainloop()
