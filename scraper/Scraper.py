__author__ = 'Pablo'

from Selenium import By
from Course import *
from selenium.common.exceptions import *


class Scraper(object):
    def __init__(self, driver = None):
        print("[+]Scraper initialized")
        self.driver = driver
        self.courses = []
        self.course_elements = []
        self.course_xpath = []
        self.course_names = []

    def find_courses(self):
        search_terms = []
        for index in range(2, 31):
            search_terms.append('//*[@id="OnderwijsZoekCursus"]/table/tbody/tr[2]/td/table/tbody/tr[{0}]/td[1]/a' \
                                .format(repr(index)))
        self.course_elements = self.driver.get_list(search_terms, By.XPATH)
        self.course_xpath.extend(search_terms)

    def find_courses_names(self):
        self.course_names = [x.text for x in self.course_elements]

    def print_courses(self):
        print("[+]displaying courses")
        if len(self.course_names) == 0:
            print("course list is empty!")
        for course in self.course_names:
            print(" > " + course.text)

    def find_course_information(self):
        information = {}

        for element_number in range(1, 9):
            information_id = self.driver.driver.find_element(By.XPATH,
                                                             '//*[@id="curs"]/table[1]/tbody/tr[2]/td[2]/table/tbody/tr[{0}]/td[1]/span' \
                                                             .format(element_number)).text
            print(' > //*[@id="curs"]/table[1]/tbody/tr[2]/td[2]/table/tbody/tr[{0}]/td[1]/span\t'.format(
                element_number) + information_id)

            information[information_id] = self.driver.driver.find_element(By.XPATH,
                                                                          '//*[@id="curs"]/table[1]/tbody/tr[2]/td[2]/table/tbody/tr[{0}]/td[3]/span' \
                                                                          .format(element_number)).text
            print(' > //*[@id="curs"]/table[1]/tbody/tr[2]/td[2]/table/tbody/tr[{0}]/td[3]/span\t'.format(
                element_number) + information[information_id])

        try:
            information_id = self.driver.driver.find_element(By.XPATH,
                                                             '//*[@id="OnderwijsCursusDocent"]/table/tbody/tr/td/table/tbody/tr[1]/td[1]/span').text
            print(' > //*[@id="OnderwijsCursusDocent"]/table/tbody/tr/td/table/tbody/tr[1]/td[1]/span\t'.format(
                element_number) + information_id)

            information[information_id] = self.driver.driver.find_element(By.XPATH,
                                                                          '//*[@id="OnderwijsCursusDocent"]/table/tbody/tr/td/table/tbody/tr[1]/td[3]/span').text
            print(' > //*[@id="OnderwijsCursusDocent"]/table/tbody/tr/td/table/tbody/tr[1]/td[3]/span\t' + information[
                information_id])
        except NoSuchElementException:
            print(" > [-]no teacher found")

        for element_number in range(2, 17):
            information_id = self.driver.driver.find_element(By.XPATH,
                                                             '//*[@id="curs"]/table[1]/tbody/tr[2]/td[5]/table/tbody/tr[{0}]/td[1]/span'
                                                             .format(element_number)).text
            print(' > //*[@id="curs"]/table[1]/tbody/tr[2]/td[5]/table/tbody/tr[{0}]/td[1]/span\t'.format(
                element_number) + information_id)

            try:
                information[information_id] = self.driver.driver.find_element(By.XPATH,
                                                                              '//*[@id="curs"]/table[1]/tbody/tr[2]/td[5]/table/tbody/tr[{0}]/td[3]/span'
                                                                              .format(element_number)).text
                print(' > //*[@id="curs"]/table[1]/tbody/tr[2]/td[5]/table/tbody/tr[{0}]/td[3]/span\t'.format(
                    element_number) + information[information_id])
            except NoSuchElementException:
                information[information_id] = self.driver.driver.find_element(By.XPATH,
                                                                              '//*[@id="curs"]/table[1]/tbody/tr[2]/td[5]/table/tbody/tr[{0}]/td[3]'
                                                                              .format(element_number)).text
                print(' > //*[@id="curs"]/table[1]/tbody/tr[2]/td[5]/table/tbody/tr[{0}]/td[3] \t' + information[
                    information_id])

        print(" > " + repr(self.driver.driver.find_element(By.XPATH, '//*[@id="curs"]/table[2]/tbody/tr[2]/td[2]')))

        print(" > " + repr(information))

        return information

    def next_course_page(self):
        return self.driver.goto(
            '//*[@id="OnderwijsZoekCursus"]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/table/tbody/tr/td[5]/a')

    def previous_course_page(self):
        return self.driver.goto(
            '//*[@id="OnderwijsZoekCursus"]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/a')

    def scrape_course_elements(self):
        print("[+]scraping courses")
        has_next_page = True

        if has_next_page:
            for course in self.course_xpath:
                self.driver.goto(course)
                information = self.find_course_information()
                self.courses.append(Course(information))
                self.driver.goto(
                    '//*[@id="pl"]/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td/table/tbody/tr/td[1]/a')
            print("[+]page finished")

            has_next_page = self.next_course_page()
