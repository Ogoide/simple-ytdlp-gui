import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import functions as func
import os

class Manager:
    def __init__(self):
        self.media_type = ''
        self.format_options = []
        self.folder_path = ''
        self.selected_format = ''
        self.url = ''
        self.confirm = False

    def download(self):
        if self.media_type == '':
            tk.messagebox.showerror(title='ERROR', message='No Media Type Selected!')
        elif self.selected_format == '':
            tk.messagebox.showerror(title='ERROR', message='No Format Selected!')
        elif self.folder_path == '':
            tk.messagebox.showerror(title='ERROR', message='No Folder Selected!')
        elif not self.confirm:
            tk.messagebox.showerror(title='ERROR', message='Please confirm your url!')
        else:
            func.download(url=self.url, media_type=self.media_type, format=self.selected_format, path=self.folder_path)
            self.progress_checker()

    def format_selection(self, event):
        self.selected_format = cbb_format.get()

    def clear(self):
        ent_url.delete(0, tk.END)
        lbl_title_display['text'] = ''
        lbl_channel_display['text'] = ''
        lbl_duration_display['text'] = ''

    def confirm_url(self):
        url = ent_url.get()
        self.url = url
        url_check = func.check_url_video(url)
        if url_check:
            info = func.get_video_info(url)
            lbl_title_display['text'] = info['title']
            lbl_channel_display['text'] = info['channel']
            lbl_duration_display['text'] = info['duration']
            self.confirm = True
        else:
            tk.messagebox.showerror(title='ERROR', message='Invalid URL')

    """def thumbnail_check(self):
        tbcheck = var_thumbnail.get()
        if tbcheck == '1':
            self.original_thumbnail = True
        else:
            self.original_thumbnail = False"""

    def define_type(self):
        if self.media_type == 'Video':
            self.format_options = ['MP4', 'WEBM']
        if self.media_type == 'Audio':
            self.format_options = ['MP3', 'WAV', 'FLAC', 'M4A']
        cbb_format['values'] = tuple(self.format_options)

    def on_type_choice(self, event, mtype_choice):
        self.media_type = mtype_choice
        self.define_type()

    def folder_selection(self):
        if self.folder_path == '':
            folder_path = filedialog.askdirectory()
            self.folder_path = folder_path
        lbl_folder_display['text'] = self.folder_path

m = Manager()

config_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'simple-ytdlp-gui')
os.makedirs(config_folder, exist_ok=True)
config_path = os.path.join(config_folder, 'config.txt')

try:
    with open(config_path, 'r') as config:
        m.folder_path = config.read()
except:
    m.folder_path = ''

main = tk.Tk()
main.title('Simple Yt-Dlp GUI')
main.resizable(False, False)

main.rowconfigure([0,1,2,3,4,5,6,7,8,9], minsize=20)
main.columnconfigure(0, minsize=20)

frm_main = ttk.Frame(master=main)
frm_main.rowconfigure([0], minsize=20)
frm_main.columnconfigure([0,1], minsize=20)

frm_url = ttk.Frame(master=main, borderwidth=2, relief=tk.SUNKEN)
ent_url = ttk.Entry(master=frm_url, width=50)
ent_url.grid(row=0, column=0, padx=10, pady=10)
ent_url.insert(string='Enter your url here!', index=0)
btn_confirm = ttk.Button(master=frm_url, text='Confirm', command=m.confirm_url)
btn_confirm.grid(row=0, column=1, padx=10, pady=10)

frm_options = ttk.Frame(master=main, borderwidth=2, relief=tk.SUNKEN)
frm_options.rowconfigure(0, minsize=20)
frm_options.columnconfigure([0,1,2], minsize=20)

frm_options_media = ttk.Frame(master=frm_options)
frm_options_media.rowconfigure([0,1,2], minsize=10)
frm_options_media.columnconfigure(0, minsize=10)

lbl_options_media = ttk.Label(master=frm_options_media, text='Media Type')
lbl_options_media.grid(row=0, column=0)
media_types = ['Video', 'Audio']
mtype_var = tk.StringVar()
for i, mtype in enumerate(media_types):
    rbt_mtype = ttk.Radiobutton(master=frm_options_media, text=mtype, value=mtype, variable=mtype_var)
    rbt_mtype.grid(column=0, row=i+1, sticky='w')
    rbt_mtype.bind('<Button-1>', lambda event, mtype_choice=mtype: m.on_type_choice(event, mtype_choice))

frm_options_media.grid(row=0, column=0, sticky='w', padx=10, pady=10)

frm_options_format = ttk.Frame(master=frm_options)
frm_options_format.rowconfigure([0,1,2], minsize=10)
frm_options_format.columnconfigure([0], minsize=10)

lbl_options_format = ttk.Label(master=frm_options_format, text='Format')
lbl_options_format.grid(row=0, column=0, padx=10)

cbb_format = ttk.Combobox(master=frm_options_format, state='readonly', width=15)
cbb_format.grid(row=1, column=0, padx=10)
cbb_format.set('Choose a format')
cbb_format.bind('<<ComboboxSelected>>', m.format_selection)

frm_additional_options = ttk.Frame(master=frm_options)
frm_additional_options.rowconfigure([0,1,2], minsize=10)
frm_additional_options.columnconfigure(0, minsize=15)

"""var_thumbnail = tk.StringVar()
chb_thumbnail = ttk.Checkbutton(master=frm_additional_options, text='Original thumbnail', variable=var_thumbnail, command=m.thumbnail_check)
chb_thumbnail.grid(row=0, column=0)"""

frm_additional_options.grid(row=0, column=2, ipadx=5)

btn_folder_selection = ttk.Button(master=frm_options, text='Select a\nfolder', command=m.folder_selection)
btn_folder_selection.grid(row=0, column=3, padx=10)
frm_options_format.grid(row=0, column=1)

frm_folder_display = ttk.Frame(master=main)
frm_folder_display.rowconfigure([0,1], minsize=1)
frm_folder_display.columnconfigure(0, minsize=1)
lbl_folder_display = ttk.Label(master=frm_folder_display, width=70, borderwidth=1, relief=tk.SUNKEN)
lbl_folder_display.grid(row=1, column=0)

frm_video_info = ttk.Frame(master=main, borderwidth=2, relief=tk.SUNKEN)
frm_video_info.rowconfigure([0,1,2], minsize=20)
frm_video_info.columnconfigure([0,1], minsize=1)

lbl_video_title = ttk.Label(master=frm_video_info, text='Title:')
lbl_video_title.grid(row=0, column=0, sticky='e')
lbl_title_display = ttk.Label(master=frm_video_info, width=70, borderwidth=1, relief=tk.SUNKEN)
lbl_title_display.grid(row=0, column=1, sticky='w', pady=5, ipadx=10)

lbl_video_channel = ttk.Label(master=frm_video_info, text='Channel:')
lbl_video_channel.grid(row=1, column=0, sticky='e')
lbl_channel_display = ttk.Label(master=frm_video_info, width=70, borderwidth=1, relief=tk.SUNKEN)
lbl_channel_display.grid(row=1, column=1, sticky='w', pady=5, ipadx=10)

lbl_video_duration = ttk.Label(master=frm_video_info, text='Duration:')
lbl_video_duration.grid(row=2, column=0, sticky='e')
lbl_duration_display = ttk.Label(master=frm_video_info, width=70, borderwidth=1, relief=tk.SUNKEN)
lbl_duration_display.grid(row=2, column=1, sticky='w', pady=5, ipadx=10)

frm_download = ttk.Frame(master=main)
frm_download.rowconfigure(0, minsize=10)
frm_download.columnconfigure([0,1], minsize=10)

btn_download = ttk.Button(master=frm_download, text='Download', command=m.download)
btn_download.grid(row=0, column=0, sticky='e')

btn_clear = ttk.Button(master=frm_download, text='Clear Video', command=m.clear)
btn_clear.grid(row=0, column=1, sticky='e')

# Placing all the widgets

lbl_title = ttk.Label(master=main, text='A Simple Yt-Dlp GUI', font='Helvetica 18 bold')
lbl_title.grid(row=0, column=0, rowspan=True)

lbl_url = ttk.Label(master=main, text='URL')
lbl_url.grid(row=1, column=0, sticky='w')
frm_url.grid(row=2, column=0, rowspan=True)

lbl_options = ttk.Label(master=main, text='Options')
lbl_options.grid(row=3, column=0, sticky='w')
frm_options.grid(row=4, column=0, rowspan=True)

lbl_folder = ttk.Label(master=main, text='Currently selected folder')
lbl_folder.grid(row=5, column=0, sticky='w')
frm_folder_display.grid(row=6, column=0, rowspan=True)

lbl_video_info = ttk.Label(master=main, text='Video Information')
lbl_video_info.grid(row=7, column=0, sticky='w')
frm_video_info.grid(row=8, column=0, rowspan=True)

frm_download.grid(row=9, column=0, sticky='e', rowspan=True)

m.folder_selection()
main.mainloop()

with open(config_path, 'w') as config:
    config.write(m.folder_path)