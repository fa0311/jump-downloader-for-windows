import asyncio
import tkinter
import tkinter.filedialog
import tkinter.scrolledtext
import os
from turtle import right
import jumpplus_downloader
import webbrowser

APP_NAME = "jump-downloader-for-windows"
VERSION = "0.1"


class input_window:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("jump-downloader-for-windows")
        self.window.geometry("400x325")

    def run(self):
        tkinter.Label(self.window, text="マンガのURL").grid(
            column=0,
            row=0,
            columnspan=1,
            pady=10,
            padx=0,
        )
        self.url_box = tkinter.Entry(width=20)
        self.url_box.grid(
            column=1,
            row=0,
            columnspan=1,
            pady=10,
            padx=0,
        )

        tkinter.Label(self.window, text="ダウンロード先").grid(
            column=0,
            row=1,
            columnspan=1,
            pady=0,
            padx=0,
        )
        folder_dialog_button = tkinter.Button(self.window, text="選択", width=20)
        folder_dialog_button.bind("<ButtonPress>", self.folder_dialog)
        folder_dialog_button.grid(
            column=1,
            row=1,
            columnspan=1,
            pady=0,
            padx=0,
        )

        self.folder_name = tkinter.StringVar(self.window)
        self.folder_name.set(
            "{USERPROFILE}\Downloads".format(USERPROFILE=os.environ["USERPROFILE"])
        )
        tkinter.Label(self.window, textvariable=self.folder_name).grid(
            column=0,
            row=2,
            columnspan=2,
            pady=0,
            padx=0,
        )

        self.pdf_flag = tkinter.BooleanVar()
        self.pdf_checkbox = tkinter.Checkbutton(text="PDF出力", variable=self.pdf_flag)
        self.pdf_checkbox.grid(
            column=1,
            row=3,
            columnspan=1,
            pady=0,
            padx=0,
        )

        tkinter.Label(
            self.window,
            wraplength=380,
            text="このツールは不正ダウンロードを助長するものではありません。このツールはダウンロードした著作物を情報処理の過程において円滑又は効率的に当該電子計算機の記録媒体に記録することを目的として制作されました。利用が終わった際は速やかに当該著作物を記録媒体から削除して下さい。マンガをアーカイブしたり第三者に公開、アップロードする行為は著作権法違反です。",
        ).grid(
            column=0,
            row=4,
            columnspan=2,
            pady=10,
            padx=0,
        )

        enter_button = tkinter.Button(self.window, text="ダウンロード", width=50)
        enter_button.bind("<ButtonPress>", self.click)
        enter_button.grid(
            column=0,
            row=5,
            columnspan=2,
            pady=0,
            padx=20,
        )

        enter_update = tkinter.Button(self.window, text="アップデートの確認", width=50)
        enter_update.bind("<ButtonPress>", self.update_dialog)
        enter_update.grid(
            column=0,
            row=6,
            columnspan=2,
            pady=10,
            padx=20,
        )

        tkinter.Label(
            self.window,
            text="{app_name} v{version}".format(app_name=APP_NAME, version=VERSION),
        ).grid(
            column=0,
            row=7,
            columnspan=2,
        )
        return self

    def folder_dialog(self, event):
        folder_name = tkinter.filedialog.askdirectory(initialdir=self.folder_name.get())
        if len(folder_name) > 0:
            self.folder_name.set(folder_name)

    def update_dialog(self, event):
        webbrowser.open(
            "https://github.com/fa0311/jump-downloader-for-windows/releases"
        )

    def click(self, event):
        asyncio.new_event_loop().run_in_executor(None, self.download)

    def download(self):
        url = self.url_box.get()
        dir = self.folder_name.get().replace("\\", "/") + "/"
        print(dir)
        progress_window().run().download(
            url, sleeptime=0, pdfConversion=self.pdf_flag.get(), dir=dir
        )


class progress_window:
    def __init__(self):
        self.window = tkinter.Toplevel()
        self.window.geometry("600x325")
        self.exit = False

    def run(self):
        force_exit_button = tkinter.Button(self.window, text="強制終了", width=50)
        force_exit_button.bind("<ButtonPress>", self.force_exit)
        force_exit_button.pack(
            pady=20,
        )
        self.progress = tkinter.scrolledtext.ScrolledText(self.window)
        self.progress.pack()
        return self

    def force_exit(self, event):
        if self.exit:
            self.add_log("既に終了しています")
        else:
            self.add_log("終了しています")
            self.exit = True

    def download(self, url, **arg):
        self.add_log("開始します")
        try:
            while url and not self.exit:
                self.add_log(f"ダウンロードしています: {url}")
                jpd = jumpplus_downloader.jumpplus_downloader()
                jpd.auto_list_download(url=url, **arg)
                url = jpd.list["readableProduct"]["nextReadableProductUri"]
                self.add_log(
                    "ダウンロードが完了しました: {title}".format(
                        title=jpd.list["readableProduct"]["title"]
                    )
                )
        except:
            self.add_log("エラーが発生しました")
        self.add_log("終了しました")

    def add_log(self, log):
        self.progress.insert("end", f"{log}\n")
        self.progress.see("end")
        print(log)


if __name__ == "__main__":
    input_window().run().window.mainloop()
