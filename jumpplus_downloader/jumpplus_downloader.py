import requests
import json
import os
import time
from PIL import Image
from io import BytesIO
import img2pdf
import math


class jumpplus_downloader:
    def __init__(self, dir="./"):
        self.file = 0
        self.h = 1200
        self.w = 760
        self.session = requests.session()
        self.dir = dir

    def __get_headers(self):
        return {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
        }

    def login(self, email_address, password, return_location_path="/"):
        data = {
            "email_address": email_address,
            "password": password,
            "return_location_path": return_location_path,
        }
        headers = {"x-requested-with": "XMLHttpRequest"}
        self.response = self.session.post(
            "https://shonenjumpplus.com/user_account/login",
            headers=dict(self.__get_headers(), **headers),
            data=data,
        )
        return self

    def auto_list_download(self, url, sleeptime=2, pdfConversion=True, zero_padding=True):
        self.json_download(url)
        self.file = 0
        if os.path.isdir(self.dir + self.list["readableProduct"]["title"]) != True:
            os.mkdir(self.dir + self.list["readableProduct"]["title"])
        for page in self.list["readableProduct"]["pageStructure"]["pages"]:
            time.sleep(sleeptime)
            if page["type"] == "main":
                self.h = page["height"]
                self.w = page["width"]
                self.download(page["src"], False)
                self.processing()
                self.output(self.dir + self.list["readableProduct"]["title"] + "/", zero_padding=zero_padding)
        if pdfConversion:
            self.convertToPdf(self.dir + self.list["readableProduct"]["title"] + "/")

    def json_download(self, url):
        # Counterfeit User agent for absolutely successfully connection.
        json_data = self.session.get(url + ".json", headers=self.__get_headers()).text
        self.list = json.loads(json_data)

    def json_localread(self, filepath):
        with open(filepath) as json_file:
            json_data = json.load(json_file)
            self.list = json_data

    def download(self, url, fakeque=False):
        if fakeque:
            print("Emulating Download : " + url)
            self.img = url
        else:
            self.img = self.session.get(url, headers=self.__get_headers())

    def processing(self):
        readImage = Image.open(BytesIO(self.img.content))
        imageSize = readImage.size
        divideNum = 4
        multiple = 8
        width = math.floor(float(imageSize[0]) / (divideNum * multiple)) * multiple
        height = math.floor(float(imageSize[1]) / (divideNum * multiple)) * multiple
        buff = []
        counterX = 0
        counterY = 0

        for wx in range(4):
            inbuff = []
            for lx in range(4):
                cropped = readImage.crop(
                    box=(
                        width * counterX,
                        height * counterY,
                        width * (counterX + 1),
                        height * (counterY + 1),
                    )
                )
                inbuff.append(cropped)
                counterY += 1
            buff.append(inbuff)
            counterX += 1
            counterY = 0

        self.converted_img = readImage.copy()
        counterX = 0
        counterY = 0
        for wdx in buff:
            for ldx in wdx:
                self.converted_img.paste(
                    ldx, (int(width * counterX), int(height * counterY))
                )
                counterX += 1
            counterX = 0
            counterY += 1

    def output(self, dir,zero_padding=True):
        file = str(self.file)
        if zero_padding:
            index = 1
            zfill = 0
            while len(self.list["readableProduct"]["pageStructure"]["pages"]) >= index:
                index *= 10
                zfill += 1
            file = file.zfill(zfill)
        self.converted_img.save(dir + file + ".png")
        self.file += 1

    def convertToPdf(self, dir):
        img = [i.replace("\\","/") for i in glob.glob(f"{dir}/*") if not i.endswith(".pdf")]
        with open(dir + "output.pdf", "wb") as f:
            f.write(img2pdf.convert(img))

    # A simple Json Dumper for debugging.
    def dumpSimplifiedJson(self, jsObject):
        f = open("JSON.json", "w")
        json.dump(
            jsObject,
            f,
            ensure_ascii=False,
            indent=4,
            sort_keys=True,
            separators=(",", ": "),
        )