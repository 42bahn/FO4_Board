import re
import requests
from bs4 import BeautifulSoup

from selenium import webdriver

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

from selenium.webdriver.chrome.service import Service
from subprocess import CREATE_NO_WINDOW

form_class = uic.loadUiType("fifa_board.ui")[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.refreshButton.clicked.connect(self.refresh)
        
        self.fifa_board()
    
    def fifa_board(self):
        def init_webdriver(url):
            # service = Service('C:\\Users\\bbu07\\Desktop\\WebScraping\\chromedriver.exe')
            # service.creationflags = CREATE_NO_WINDOW
            options = webdriver.ChromeOptions()
            options.headless = True # True == 웹 브라우저를 띄우지 않음 / False == 웹 브라우저를 띄움
            options.add_argument("window-size=1440,960") # 웹
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36")
            options.add_argument("--disable-gpu")
            options.add_experimental_option('excludeSwitches', ['enable-logging']) # WebDriver 로드 시 터미널에 출력되는 로그 기록을 끔
            driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
            driver.get(url)
            return (driver)

        url = "http://fifaonline4.nexon.com/community/free/list"
        driver = init_webdriver(url)
        soup = BeautifulSoup(driver.page_source, "lxml")
        
        lists = soup.find("div", attrs="tbody").find_all("span", attrs={"class":"subject"})
        btn_next = driver.find_element_by_class_name("btn_next")
        for index in range(1, 10):
            for list in lists:
                if list.find("span", attrs={"class":"ico"}):
                    list.find("span", attrs={"class":"ico"}).decompose()
                if list.find("span", attrs={"class":"count_comment"}):
                    list.find("span", attrs={"class":"count_comment"}).decompose()
                self.listWidget.addItem(str(list.a.get_text().strip()))
            btn_next.click()
    
    def refresh(self) :
        self.listWidget.clear()
        self.fifa_board()

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()