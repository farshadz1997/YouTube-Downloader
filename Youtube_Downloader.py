from pytube import YouTube, request
import pyperclip
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import threading
from tkinter import messagebox as msg
import os

#getting title and qualities
def get_url():
    try:
        URL_button ['state'] = 'disabled'
        if qualities_Var != "-":
            qualities_Var.set("-")
            options["menu"].delete(0, 'end')
        counter = 0
        pb.config(mode = "indeterminate")
        pb.start()
        yt = YouTube(URL_entry.get())
        Info_Var.set(f"Title: {yt.title}\n"
                    f"Length: {yt.length // 60:02d}:{yt.length % 60:02d}")
        global res_list
        res_list = {}
        for stream in yt.streams:
            if stream.mime_type != "audio/webm" and stream.resolution != None and stream.video_codec != "vp9":
                text = str(stream.resolution) + " - " + str(stream.fps) + "fps - " + str(stream.video_codec) + " - " + str(f"{stream.filesize/1000000:.2f}") + " MB " 
                res_list[text] = counter
                options["menu"].add_command(label = text, command = tk._setit(qualities_Var, text))
                counter += 1
    except Exception as e:
        msg.showerror("Error", e)
    else:
        dl_button_V ['state'] = 'normal'
        dl_button_A ['state'] = 'normal'
    finally:
        URL_button ['state'] = 'normal'
        pb.stop()
        pb.config(mode = "determinate")
        pb_Var.set(0)

#download function        
def Download(url,audio=False):
    qua = qualities_Var.get()
    path = Path_Ent.get()
    percentage_Var.set("Connecting...")
    URL_button ['state'] = 'disabled'
    Paste_button ['state'] = 'disabled'
    Path_button ['state'] = 'disabled'
    dl_button_V ['state'] = 'disabled'
    dl_button_A ['state'] = 'disabled' 
    try:
        yt = YouTube(url, on_progress_callback=progress_Check)
        title = yt.title
        if (audio):
            stream = yt.streams.filter(subtype='mp4',only_audio=True).first()
        else:
            stream = yt.streams[res_list[qua]]
        global filesize
        filesize = stream.filesize
        stream.download(path)
    except Exception as e:
        if qua == "-" and audio is False:
            msg.showerror("Error", "Choose a quality for download!")
        else:    
            msg.showerror("Error", e)
    else:
        msg.showinfo("Done", "Download complete!")
    finally:
        percentage_Var.set("")
        pb_Var.set(0)
        URL_button ['state'] = 'normal'
        Paste_button ['state'] = 'normal'
        Path_button ['state'] = 'normal'
        dl_button_V ['state'] = 'normal'
        dl_button_A ['state'] = 'normal'
 
#Gets the percentage of the file that has been downloaded.
def progress_Check(chunk = None, file_handler = None, bytes_remaining = None):
        percent = (100*(filesize - bytes_remaining))/filesize
        pb_Var.set(percent)
        percentage_Var.set('{:00.0f}%'.format(percent))
    
#where to save downloaded file                
def Save_to():
    dir = filedialog.askdirectory()
    Path_Var.set(dir)

#default save address
def default_file_path():
    home = os.path.expanduser('~')
    download_path = os.path.join(home, 'Downloads')
    Path_Var.set(download_path)

#paste button function
def Paste():
    URL_entry.delete(0, 'end')
    s = pyperclip.paste()
    URL_VAR.set(s)
    
def url_thread():
    threading.Thread(target = get_url, daemon = True).start()
    
def download_thread_V():
    threading.Thread(target = Download, args = (URL_entry.get(),False), daemon = True).start()
    
def download_thread_A():
    threading.Thread(target = Download, args = (URL_entry.get(),True), daemon = True).start()


if __name__ == "__main__":
    #win UI
    win = Tk()
    win.title("Youtube Downloader")
    win.iconbitmap("icon.ico")
    win.geometry("500x500")
    win.resizable(False, False)
            
    #title
    Label_title = Label(win, text = "Youtube Downloader", fg = "red", font = ("Times",30)).place(x = 90, y = 25)
            
    #URL
    URL_label = Label(win, text = "URL:").place(x = 70, y = 100)
    URL_VAR = StringVar()
    URL_entry = Entry(win, textvariable = URL_VAR, width = 50)
    URL_entry.place(x = 115, y = 100)
    URL_button = ttk.Button(win, text = "Get URL", command = url_thread)
    URL_button.place(x = 220, y = 125)

    #Paste Button
    paste_ico = PhotoImage(file = r"clipboard_paste.png")
    Paste_button = ttk.Button(win, image = paste_ico, width = 3, command = Paste)
    Paste_button.place(x = 420, y = 98)
            
    #save to
    Path_label = Label(win, text = "Save to:").place(x = 60, y = 160)
    Path_Var = StringVar()
    Path_Ent = ttk.Entry(win, textvariable = Path_Var, width = 50, state = DISABLED)
    Path_Ent.place(x = 115, y = 160)
    default_file_path()
    Path_button = ttk.Button(win, text = "Save to", command = Save_to)
    Path_button.place(x = 220, y = 185)
            
    #Option menu
    qualities_Var = StringVar()
    qualities_Var.set("-")
    qualities_label = Label(win, text = "Qualities:").place(x = 60, y = 225)
    options = ttk.OptionMenu(win, variable = qualities_Var)
    options.place(x = 115, y = 225)
        
    #Video infos
    Info_Var = StringVar()
    Info_label = Message(win, textvariable = Info_Var, width = 200)
    Info_label.place(x = 60, y = 260)
            
    #download button
    dl_button_V = ttk.Button(win, text = "Download Video", state = 'disabled', command = download_thread_V)
    dl_button_V.place(x = 160, y = 400)
    dl_button_A = ttk.Button(win, text = "Download Audio", state = 'disabled', command = download_thread_A)
    dl_button_A.place(x = 260, y = 400)
        
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