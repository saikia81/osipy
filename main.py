__author__ = 'Pablo'
import pickle
from Scraper import *

from scraper.Selenium import *


def find_courses():
    username = "0897778"
    password = get_password()

    driver = Driver('firefox')
    driver.home()
    assert (driver.login(username, password))
    driver.goto_menu("Onderwijs")
    driver.fillout()

    scraper = Scraper(driver)
    scraper.find_courses()
    scraper.print_courses()
    scraper.find_courses_names()
    scraper.scrape_course_elements()
    driver.shutdown()

    with open("courses.dat", 'wb+') as courses_file:
        pickle.dump(scraper.courses, courses_file)

    for course in scraper.courses:
        print(course)

    return scraper.courses

def load(file_name = "courses.dat"):
    with open(file_name, "r") as courses_file:
        courses = pickle.load(courses_file)
        print("[+]course list loaded")
    for course in courses:
        print(course)
    return courses

def main():
    find_courses()

if __name__ == "__main__":
        main()