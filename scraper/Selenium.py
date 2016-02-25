__author__ = 'Pablo'

import time

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import *
import getpass

def get_password():
    password = ""
    password_is_correct = False
    while len(password) < 5 or not password_is_correct:
        password = getpass.getpass()
        if len(password) < 5:
            print("password length is too short!")
            continue
        if not password_is_correct:
            if input("is the password correct?[y/n]: ")[0].lower() == 'y':
                password_is_correct = True

    return password

class Driver(object):
    def __init__(self, driver_choice):
        self.username = None
        self.password = None
        if driver_choice.lower() == "firefox":
            self.driver = webdriver.Firefox()
        elif driver_choice.lower() == "selenium":
            self.driver = webdriver.Remote("http://localhost:4444/wd/hub",
                                           webdriver.DesiredCapabilities.HTMLUNITWITHJS)
        else:
            self.driver = webdriver.Firefox()

    def shutdown(self):
        print("[+]shutting down!")
        self.driver.close()

    def home(self):
        self.driver.get("http://student.osiris.hro.nl/")

    def wait(self, sleep_time = 1):
        while len(self.driver.find_elements(By.ID. self.username)) == 0:
            time.sleep(sleep_time)

    def get_list(self, search_terms, element_type):
        print("[+]Searching for elements")
        course_elements = []

        for search_term in search_terms:
            try:
                course_element = self.driver.find_element(element_type, search_term)
            except NoSuchElementException:
                print("[=]Waring: search term was not found!")
                print(" > " + search_term)
                continue
            course_elements.append(course_element)

        for course_element in course_elements:
            print("[+]course found: " + course_element.text) #debug

        if len(course_elements) == 0:
            print("[-]no courses were found!")

        return course_elements

    def login(self, username, password):
        self.username = username

        print("[+]logging in")
        user_element = self.driver.find_element_by_id("username")
        user_element.send_keys(username)
        passw_element = self.driver.find_element_by_id("password")
        passw_element.send_keys(password)
        passw_element.send_keys(Keys.RETURN)

        self.driver.find_element_by_class_name('UnselectedButton').click()

        time.sleep(1)
        if len(self.driver.find_elements(By.PARTIAL_LINK_TEXT, "Uitloggen")) == 0: #find condition!
            print("[-]login failed!")
            return True #change this

        return True

    def goto(self, address):
        if type(address) == str:
            try:
                self.driver.find_element(By.XPATH, address).click()
                time.sleep(1)
                return True
            except NoSuchElementException:
                return False
        elif type(address) == WebElement:
            try:
                address.click()
                time.sleep(1)
                return True
            except StaleElementReferenceException:
                return False

    def goto_menu(self, menu):
        self.driver.get("https://student.osiris.hro.nl:9021/osiris_student/" + menu + ".do")

    def fillout(self, jaar = 2015, block = 2):
        self.driver.find_element(By.NAME, "jaar_1").click()
        time.sleep(1)
        self.driver.find_element(By.NAME, "aanvangs_blok").send_keys(Keys.ARROW_DOWN * (block + 1) + Keys.RETURN)
        time.sleep(1)
        self.driver.find_element(By.NAME, "faculteit").send_keys(Keys.ARROW_UP * 3 + Keys.RETURN)
        time.sleep(1)
        self.driver.find_element(By.ID, "M__Ida").click()


