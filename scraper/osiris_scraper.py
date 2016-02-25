import scrapy
from scrapy.spiders import Spider
from scrapy.http import Response, FormRequest, Request
from scrapy.http.cookies import CookieJar

from getpass import getpass

class Osiris_spider(Spider):
    name = 'student.osiris.hro.nl' #overrides
    start_urls = ['https://student.osiris.hro.nl:9021/osiris_student/Personalia.do'] #["https://thepirateboat.eu"]
    login_url = "https://login.hro.nl/v1/login"

    def __init_(self):
        self.cookie = None

    #overrides
    def parse(self, response):
        if "thepirateboat" in response.url:
            print("[+] url: " + response.url)

            yield FormRequest.from_response(response, formdata = {"inp" : "test"})
        if "logged in as" in response.body:
                Request(self.start_urls[0])
        if 'login' in response.url:
            yield FormRequest.from_response(response, callback = self.login_check, dont_click = False, formdata = {
                                                                            'username': '0897778',
                                                                            'password': getpass("password: ")})
        elif 'Personalia' in response.url:
            print("[+]Personalia reached!")
            yield self.parse_courses(response)
        else:
            print("[-]Spider got lost at: '" + response.url + "'")

    def parse_courses(self, response):
        raise NotImplementedError("[-]parse_courses not implemented yet!")

    def login_check(self, response):
        if "logged in as" in response.body:
            print("[+]login success!")
            self.cookie = response.headers['Set-Cookie'] #if logged in save cookie
            return False
        elif "attempt to re-submit" in response.body:
            return Request(self.login_url, callback = self.login_check)
        else:
            print("[-]login failed!")
            return True

if __name__ == '__main__':
    print("this is a module, and can only be imported not run!")


cookie = \
"""
Cookie:BIGipServerosiris6-student_POOL=2483099793.15651.0000; JSESSIONID=QJLLWkgMYx8TQmSJflPBGLRWZDHyyrTPbMcjtsYy1yfRzngnkkJQ!1351995286; _pk_ref.5.3a55=%5B%22%22%2C%22%22%2C1449435315%2C%22https%3A%2F%2Flogin.hro.nl%2Fv1%2Flogin%3Frcl%3D65%26service%3Dhttps%3A%2F%2Fstudent.osiris.hro.nl%3A9021%2Fosiris_student%2FOnderwijsZoekCursus.do%22%5D; oracle.uix=0^^GMT+1:00; _pk_id.5.3a55=dad4bfa691b4e0e1.1449432431.2.1449435327.1449435315.; _pk_ses.5.3a55=*
"""