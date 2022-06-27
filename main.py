import asyncio
import tkinter
import tkinter.filedialog
import tkinter.scrolledtext
import os
from turtle import right
import jumpplus_downloader
import webbrowser

APP_NAME = "jump-downloader-for-windows"
VERSION = "1.0.1"


class input_window:
    def __init__(self, debug=False):
        self.debug = debug
        self.window = tkinter.Tk()
        self.window.title("jump-downloader-for-windows")
        self.window.geometry("400x450")

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
        tkinter.Label(self.window).grid(
            column=0,
            row=3,
            columnspan=1,
            pady=0,
            padx=0,
        )

        tkinter.Label(self.window, text="ログイン情報(任意) メールアドレス").grid(
            column=0,
            row=100,
            columnspan=1,
            pady=0,
            padx=0,
        )
        self.email_address = tkinter.StringVar(self.window)
        tkinter.Entry(self.window, textvariable=self.email_address).grid(
            column=1,
            row=100,
            columnspan=2,
            pady=0,
            padx=0,
        )

        tkinter.Label(self.window, text="ログイン情報(任意) パスワード").grid(
            column=0,
            row=101,
            columnspan=1,
            pady=0,
            padx=0,
        )

        self.password = tkinter.StringVar(self.window)
        tkinter.Entry(self.window, textvariable=self.password).grid(
            column=1,
            row=101,
            columnspan=2,
            pady=0,
            padx=0,
        )

        tkinter.Label(self.window).grid(
            column=0,
            row=102,
            columnspan=1,
            pady=0,
            padx=0,
        )

        tkinter.Label(text="PDF出力").grid(
            column=0,
            row=200,
            columnspan=1,
            pady=0,
            padx=0,
        )

        self.pdf_flag = tkinter.BooleanVar()
        self.pdf_checkbox = tkinter.Checkbutton(variable=self.pdf_flag)
        self.pdf_checkbox.grid(
            column=1,
            row=200,
            columnspan=1,
            pady=0,
            padx=0,
        )

        tkinter.Label(text="続きを全てダウンロード").grid(
            column=0,
            row=201,
            columnspan=1,
            pady=0,
            padx=0,
        )

        self.next_flag = tkinter.BooleanVar()
        self.next_checkbox = tkinter.Checkbutton(variable=self.next_flag)
        self.next_checkbox.grid(
            column=1,
            row=201,
            columnspan=1,
            pady=0,
            padx=0,
        )

        tkinter.Label(text="遅延(秒)").grid(
            column=0,
            row=202,
            columnspan=1,
            pady=0,
            padx=0,
        )

        self.wait_box = tkinter.StringVar(self.window)
        self.wait_box.set("0")
        tkinter.Entry(self.window, textvariable=self.wait_box).grid(
            column=1,
            row=202,
            columnspan=2,
            pady=0,
            padx=0,
        )

        tkinter.Label(
            self.window,
            wraplength=380,
            text="このツールは不正ダウンロードを助長するものではありません。利用が終わった際は速やかにダウンロードした著作物を記録媒体から削除して下さい。ダウンロードした著作物をアーカイブしたり第三者に公開、アップロードする行為は著作権法違反です。",
        ).grid(
            column=0,
            row=300,
            columnspan=2,
            pady=10,
            padx=0,
        )

        enter_button = tkinter.Button(self.window, text="ダウンロード", width=50)
        enter_button.bind("<ButtonPress>", self.click)
        enter_button.grid(
            column=0,
            row=400,
            columnspan=2,
            pady=0,
            padx=20,
        )

        enter_update = tkinter.Button(self.window, text="アップデートの確認", width=50)
        enter_update.bind("<ButtonPress>", self.update_dialog)
        enter_update.grid(
            column=0,
            row=401,
            columnspan=2,
            pady=10,
            padx=20,
        )

        tkinter.Label(
            self.window,
            text="{app_name} v{version}".format(app_name=APP_NAME, version=VERSION),
        ).grid(
            column=0,
            row=500,
            columnspan=2,
        )
        return self

    def folder_dialog(self, event=None):
        folder_name = tkinter.filedialog.askdirectory(initialdir=self.folder_name.get())
        if len(folder_name) > 0:
            self.folder_name.set(folder_name)

    def update_dialog(self, event=None):
        webbrowser.open(
            "https://github.com/fa0311/jump-downloader-for-windows/releases"
        )

    def click(self, event=None):
        if self.debug:
            self.download()
        else:
            asyncio.new_event_loop().run_in_executor(None, self.download)

    def download(self):
        url = self.url_box.get()
        dir = self.folder_name.get().replace("\\", "/") + "/"
        if not str.isdigit(self.wait_box.get()):
            self.wait_box.set("0")
        progress_window().run().jpd_run(dir=dir).login(
            email_address=self.email_address.get(), password=self.password.get()
        ).download(
            url,
            next_flag=self.next_flag.get(),
            sleeptime=int(self.wait_box.get()),
            pdfConversion=self.pdf_flag.get(),
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

    def force_exit(self, event=None):
        if self.exit:
            self.add_log("既に終了しています")
        else:
            self.add_log("終了しています")
            self._exit()

    def _exit(self):
        self.exit = True

    def jpd_run(self, dir="./"):
        self.jpd = jumpplus_downloader.jumpplus_downloader(dir=dir)
        return self

    def login(self, **kwargs):
        if len(kwargs["email_address"]) > 0 and len(kwargs["password"]) > 0:
            json = self.jpd.login(**kwargs).response.json()
            if json.get("ok", False):
                self.add_log("ログインに成功しました")
            else:
                self.add_log(json["error"]["message"])
                self.force_exit()
        return self

    def download(self, url, next_flag=False, **kwargs):
        try:
            while url and not self.exit:
                self.add_log(f"ダウンロードしています: {url}")
                self.jpd.auto_list_download(url=url, **kwargs)
                url = self.jpd.list["readableProduct"]["nextReadableProductUri"]
                self.add_log(
                    "ダウンロードが完了しました: {title}".format(
                        title=self.jpd.list["readableProduct"]["title"]
                    )
                )
                if not next_flag:
                    self._exit()
        except:
            self.add_log("エラーが発生しました")
            self._exit()
        self.add_log("終了しました")
        self._exit()

    def add_log(self, log):
        self.progress.insert("end", f"{log}\n")
        self.progress.see("end")
        print(log)


if __name__ == "__main__":
    input_window(debug=False).run().window.mainloop()
