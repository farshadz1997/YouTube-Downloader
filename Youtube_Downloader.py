from pytube import YouTube, request
import pyperclip
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import threading
from tkinter import messagebox as msg
import os

def get_url():
    try:
        if qualities_Var != "-":
            qualities_Var.set("-")
            options["menu"].delete(0, 'end')
        counter = 0
        pb.config(mode = "indeterminate")
        pb.start()
        yt = YouTube(URL_entry.get())
        Info_Var.set(f"Title: {yt.title}\n"
                    f"Length: {yt.length // 60}:{yt.length % 60}")
        global res_list
        res_list = {}
        for stream in yt.streams:
            if stream.mime_type != "audio/webm" and stream.resolution != None and stream.video_codec != "vp9":
                text = str(stream.resolution) + " - " + str(stream.fps) + "fps - " + str(stream.video_codec)
                res_list[text] = counter
                options["menu"].add_command(label = text, command = tk._setit(qualities_Var, text))
                counter += 1
        pb.stop()
        pb.config(mode = "determinate")
        pb_Var.set(0)
    except Exception as e:
        pb.stop()
        pb.config(mode = "determinate")
        pb_Var.set(0)
        msg.showerror("Error", e)
        
def Download(url,directory,audio=False):
    qua = qualities_Var.get()
    percentage_Var.set("Connecting...")
    try:
        yt = YouTube(url)
        if (audio):
            stream = yt.streams.filter(subtype='mp4',only_audio=True).first()
            directory = directory + '/' + yt.title + '.mp3'
        else:
            stream = yt.streams[res_list[qua]]
            directory = directory + '/' + yt.title + '.mp4'
        filesize = stream.filesize
        with open(directory, 'wb') as f:
            stream = request.stream(stream.url)
            downloaded = 0
            while True:
                chunk = next(stream, None)
                if chunk:
                    f.write(chunk)
                    remaining = filesize - downloaded
                    percent = 100*(filesize - remaining)/filesize
                    pb_Var.set(percent)
                    percentage_Var.set('{:00.0f}%'.format(percent))
                    downloaded += len(chunk)
                else:
                    percentage_Var.set("")
                    pb_Var.set(0)
                    msg.showinfo("Done", "Download complete.")
                    break
    except Exception as e:
        percentage_Var.set("")
        pb_Var.set(0)
        msg.showerror("Error", e)
                
def Save_to():
    global dir
    dir = filedialog.askdirectory()
    Path_Var.set(dir)
    return dir

def Paste():
    URL_entry.delete(0, 'end')
    s = pyperclip.paste()
    URL_VAR.set(s)
    
def url_thread():
    threading.Thread(target = get_url, daemon = True).start()
    
def download_thread_V():
    threading.Thread(target = Download, args = (URL_entry.get(),dir,False), daemon = True).start()
    
def download_thread_A():
    threading.Thread(target = Download, args = (URL_entry.get(),dir,True), daemon = True).start()


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
            
    #download button
    dl_button_V = ttk.Button(win, text = "Download Video", command = download_thread_V).place(x = 160, y = 400)
    dl_button_A = ttk.Button(win, text = "Download Audio", command = download_thread_A).place(x = 260, y = 400)
        
    #percentage label
    percentage_Var = StringVar()
    percentage_label = Label(win, textvariable = percentage_Var)
    percentage_label.place(x = 222, y = 430)
                
    #Progressbar
    pb_Var = DoubleVar()
    pb = ttk.Progressbar(win, variable = pb_Var, length = 375)
    pb.place(x = 70, y = 450)
    pb['maximum'] = 100

    win.mainloop()
    
