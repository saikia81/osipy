import scrapy
from scrapy.spiders import Spider
from scrapy.http import Response, FormRequest, Request
from scrapy.http.cookies import CookieJar
from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule

from getpass import getpass

class Osiris_spider(Spider):
    name = 'google.nl' #overrides
    start_urls = ['https://www.google.nl/?gfe_rd=cr&ei=idpoVo_9GIO--QaGuomYCQ']

    def __init_(self):
        print( "[+]spider init")
        self.cookie = None
        self.password = getpass("\npassword: ")

    #overrides
    def parse(self, response):
        if "google" in response.url:
            print("[+] url: " + response.url)
            yield FormRequest.from_response(response, formdata = {})
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



class MySpider(InitSpider):
    name = 'myspider'
    allowed_domains = ['domain.com']
    login_page = 'http://www.domain.com/login'
    start_urls = ['http://www.domain.com/useful_page/',
                  'http://www.domain.com/another_useful_page/']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'-\w+.html$'),
             callback='parse_item', follow=True),
    )

    def init_request(self):
        """This function is called before crawling starts."""
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        """Generate a login request."""
        return FormRequest.from_response(response,
                    formdata={'name': 'herman', 'password': 'password'},
                    callback=self.check_login_response)

    def check_login_response(self, response):
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        if "Hi Herman" in response.body:
            self.log("Successfully logged in. Let's start crawling!")
            # Now the crawling can begin..
            self.initialized()
        else:
            self.log("Bad times :(")
            # Something went wrong, we couldn't log in, so nothing happens.

    def parse_item(self, response):

        # Scrape data from page

if __name__ == '__main__':
    print("this is a module, and can only be imported not run!")
