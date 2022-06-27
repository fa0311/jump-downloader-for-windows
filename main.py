import tkinter
import tkinter.filedialog
import os
import sys
import jumpplus_downloader

class jumpplus_downloader_for_win:
    def __init__(self):
        window = tkinter.Tk()
        window.title(u"jump-downloader-for-windows")
        window.geometry("400x300")
        self.input_window(window)
        window.mainloop()

    def input_window(self, window):
        self.url_box_title = tkinter.StringVar(window)
        self.url_box_title.set('URLを入力してください')
        tkinter.Label(window,textvariable=self.url_box_title).grid(
            column=0,
            row=0,
            padx=30,
        )

        self.url_box = tkinter.Entry(width=20)
        self.url_box.grid(
            column=1,
            row=0,
            padx=30,
        )

        self.folder_dialog_button_title = tkinter.StringVar(window)
        self.folder_dialog_button_title.set('ダウンロード先を選択してください')
        tkinter.Label(window,textvariable=self.folder_dialog_button_title).grid(
            column=0,
            row=1,
        )
        folder_dialog_button = tkinter.Button(window, text='開く', width=20)
        folder_dialog_button.bind('<ButtonPress>', self.folder_dialog)
        folder_dialog_button.grid(
            column=1,
            row=1,
        )
        self.folder_name = tkinter.StringVar(window)
        self.folder_name.set('')
        tkinter.Label(window,textvariable=self.folder_name).grid(
            column=0,
            row=2,
            columnspan=2,
        )


        self.pdf_flag = tkinter.BooleanVar()
        self.pdf_checkbox = tkinter.Checkbutton(text=u"PDF出力",variable=self.pdf_flag)
        self.pdf_checkbox.grid(
            column=1,
            row=3,
        )

        enter_button = tkinter.Button(window,text=u'決定', width=50)
        enter_button.bind("<Button-1>",self.click)
        enter_button.grid(
            column=0,
            row=4,
            columnspan=2,
            padx=30,
        )


    def folder_dialog(self, event):
        iDir = os.path.abspath(os.path.dirname(__file__))
        folder_name = tkinter.filedialog.askdirectory(initialdir=iDir)
        if len(folder_name) == 0:
            self.folder_name.set('未選択です')
        else:
            self.folder_name.set(folder_name)

    def click(self,event):
        url = self.url_box.get()
        while url:
            print(url)
            jpd = jumpplus_downloader.jumpplus_downloader()
            jpd.auto_list_download(url=url, sleeptime=0, pdfConversion=self.pdf_flag.get())
            url = jpd.list["readableProduct"]["nextReadableProductUri"]
            del jpd

if __name__ == '__main__':
    jumpplus_downloader_for_win()