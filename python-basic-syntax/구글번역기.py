import os
import sys
import tkinter
from tkinter import filedialog
import glob as gb
import requests
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium. webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import subprocess
import bs4
import time
import datetime as dt
import getpass
import shutil

class MyClass:
    def __init__(self,file_language='auto',trans_language="english",mkdir=False) -> None:
        self.info={}
        self.mkdir=mkdir
        #self.dir=None
        self.name=getpass.getuser()
        #self.search=None
        #self.save_root=None
        Lang={"auto":'auto',
            "english" : 'en',
            "korean" : 'ko',
            "japan" : "ja"
        }
        file_language=file_language.lower()
        trans_language=trans_language.lower()
        if (file_language not in Lang) or (trans_language not in Lang):
            raise Exception("올바른 언어가 아닙니다. English,Korean,Japan 중 하나를 선택해주세요")
        else:
            self.language=list(map(lambda x:Lang[x],[file_language,trans_language]))
        pass

    def __folder__(self):
        root=tkinter.Tk()
        search=filedialog.askdirectory()
        self.info['search']=search
        root.destroy()
        os.chdir(search)

        file_dic={
        "pdf":[]}
        #"txt":{}}

        for x in file_dic:
            # file_dic[x]=list(map(lambda x: absroot+"/"+x,gb.glob(f"*.{x}")))
            file_dic[x]=gb.glob(f"*.{x}")
        self.info['file_name']=file_dic
        #try:
            #if not any(file_dic.values()):
                #raise Exception("해당폴더에 아무런 파일이 존재하지 않습니다")
        #except Exception as e:
            #print(e,"\n","파일을 다시 선택해주십시오")
        if not any(file_dic.values()):
                raise Exception("해당폴더에 아무런 파일이 존재하지 않습니다")

    def __save__(self):    
        Data={
            "Text":"translate",
            "PDF":"docs"}
        #driv.get("https://translate.google.com/")
        try:
            shutil.rmtree("C:\chrometemp")
        except FileNotFoundError:
            pass

        subprocess.Popen('C:/Program Files/Google/Chrome/Application/chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')
        option=Options()
        option.add_experimental_option("debuggerAddress","127.0.0.1:9222")
        chrome_ver=chromedriver_autoinstaller.get_chrome_version().split(".")[0]
        service=Service(executable_path=f"./{chrome_ver}/chromedriver.exe")
        try:
            driv=webdriver.Chrome(service=service,options=option)
        except:
            chromedriver_autoinstaller.install(True)
            driv=webdriver.Chrome(service=service,options=option)
        driv.implicitly_wait(8)
        def pdf(url):
            driv.get(f'https://translate.google.com/?hl=ko&sl={self.language[0]}&tl={self.language[1]}&op={Data["PDF"]}')
            time.sleep(1)

            test=WebDriverWait(driv,3).until(lambda x:x.find_element(By.CSS_SELECTOR,".D7BEKc>input"))
            time.sleep(1)
            test.send_keys(url) #자료 보내기<절대경로>

            t='.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-Bz112c-M1Soyc.nCP5yc.AjY5Oe.LQeN7.k2RlOb'
            # step2 : 번역시키는 버튼
            while True:
                time.sleep(1)
                try:
                    btn2=WebDriverWait(driv,3).until(lambda x:x.find_element(By.CSS_SELECTOR,t))
                    btn2.click()
                    break
                except:
                    continue

            ul2='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-Bz112c-M1Soyc nCP5yc AjY5Oe LQeN7 sWFiQe'
            k="."+".".join(ul2.split(" "))
            i=0
            while i<11:
                time.sleep(1)
                i+=1
                try:
                    btn3=WebDriverWait(driv,3).until(lambda x:x.find_element(By.CSS_SELECTOR,k))
                    btn3.click()
                    time.sleep(1)
                    break
                except:
                    continue
        for fl in self.info['file_name']["pdf"]:
            pdf(self.info["search"]+"/"+fl)
        driv.quit()
    def __where__(self):
        if self.mkdir:
            root=tkinter.Tk()
            save_root=filedialog.askdirectory()
            root.destroy()
        else:
            save_root=self.info["search"]
        os.chdir(save_root)
        name=dt.datetime.now().strftime("%Y%m%d")
        os.makedirs(f"{self.name}({name})",exist_ok=True) #저장할 파일 생성
        # os.chdir(save_root+'/'+name) #여기가 저장경로
        self.info["save"]=save_root+'/'+f"{self.name}({name})"

        #다운로드 경로에 가서 번역된 파일 탐색
        os.chdir(f'c:/Users/{self.name}/Downloads')
        down_files=[]
        for x in self.info["file_name"]["pdf"]:
            down_files.extend(gb.glob(f'*{x.split(".")[0]}*'))
        for y in down_files:
            shutil.move(f"./{y}",f'{self.info["save"]}'+f'/{y}')     

    def start(self):
        MyClass.__folder__(self)
        MyClass.__save__(self)
        MyClass.__where__(self) 