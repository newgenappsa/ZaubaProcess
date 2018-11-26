from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException,WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



class AccountVerify:

    def __init__(self,address):
        self.address = address
        self.path = '/Users/macbook/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs'
        self.driver = webdriver.PhantomJS(executable_path = self.path)
        self.yahoolink = "https://login.yahoo.com/config/login_verify2?MsgId=8934_0_1252_1721_9103_0_67_428&.src=ym&.intl=us"
        self.outlook = "https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1540886182&rver=7.0.6737.0&wp=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fowa%2f%3fnlp%3d1%26RpsCsrfState%3da9e68d0f-e99e-2082-2698-11c4e8bf0cba&id=292841&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=90015"
        self.gmail = 'https://mail.google.com/mail/u/0/#inbox'

    def yahoo_verification(self):
        print("yahoo")
        try:
            self.driver.get(self.yahoolink)
            self.driver.find_element_by_id("login-username").send_keys(self.address)
            self.driver.find_element_by_id("login-signin").click()
        except TimeoutException:
            self.driver.quit()
            self.yahoo_verification()
        try:
            #WebDriverWait(self.driver,8).until(EC.visibility_of_element_located((By.XPATH,"//input[@id='login-passwd']")))
            self.driver.find_element_by_xpath("//input[@id='login-passwd']")
            self.driver.quit()
            return True
        except NoSuchElementException:
            self.driver.quit()
            return False

    def outlook_verification(self):
         print("outlook")
         try:
             self.driver.get(self.outlook)
             WebDriverWait(self.driver,8).until(EC.visibility_of_element_located((By.ID,"i0116")))
             self.driver.find_element_by_id("i0116").send_keys(self.address)
             self.driver.find_element_by_id("idSIButton9").click()
             print("try1")
         except TimeoutException:
             self.driver.quit()
             print("except1")
             self.outlook_verification()
         try:
             WebDriverWait(self.driver,8).until(EC.visibility_of_element_located((By.XPATH,"//div[@id='displayName']")))
             self.driver.find_element_by_xpath("//div[@id='displayName']")
             self.driver.quit()
             print("try2")
             return True
         except TimeoutException:
             print("except2")
             self.driver.quit()
             return False

    def gmail_verification(self):
        print("gmail")
        try:
             self.driver.get(self.gmail)
             #WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.ID,"identifierId")))
             self.driver.find_element_by_id('identifierId').send_keys(self.address)
             self.driver.find_element_by_id('identifierNext').click()
             self.driver.implicitly_wait(1)
        except TimeoutException:
            self.gmail_verification()
            self.driver.quit()
        try:
             self.driver.find_element_by_xpath("//div[@id='passwordNext']")
             self.driver.quit()
             return True
        except NoSuchElementException:
             self.driver.quit()
             return False

    def check_through_all(self):
         self.response = self.gmail_verification()
         if self.response == False:
             self.driver = webdriver.PhantomJS(executable_path = self.path)
             self.response = self.outlook_verification()
             if self.response == False:
                  self.driver = webdriver.PhantomJS(executable_path = self.path)
                  self.response = self.yahoo_verification()
                  print(self.response)
         return self.response
