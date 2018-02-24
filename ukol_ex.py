# -*- coding: utf-8 -*-

from urllib.request import Request, urlopen
import urllib
import re


class Task(object):

    def __init__(self):
        self.all_links = []
        self.pictures_link = []
        self.picture_id = 0

    def is_exponea_page(self, url):
        exponea_page = re.match('https://exponea.*', url)

        if exponea_page:
            return True
        else:
            return False

    def skip_page(self, url):
        pdf_pages = re.match(r'.*pdf$', url)

        if pdf_pages:
            return False

        return True

    def picture_or_link(self, url):
        png = re.match(r'.*png$', url)
        jpg = re.match(r'.*jpg$', url)
        jpeg = re.match(r'.*jpeg$', url)

        if png:
            return 'picture', 'png'

        if jpg:
            return 'picture', 'jpg'

        if jpeg:
            return 'picture', 'jpeg'

        return 'link'

    def download_picture(self, name, file_type, url):
        result_name = str(name) + '.' + file_type

        f = open(result_name, 'wb')
        f.write(urlopen(url).read())
        f.close()

    def final_url_process(self, link):
        if link in self.all_links:
            return

        pic_or_link = self.picture_or_link(link)

        if pic_or_link[0] == 'l':

            if self.is_exponea_page(link):
                print(link)
                self.all_links.append(link)
                self.do_the_job(link)

        if pic_or_link[0] == 'picture' and link not in self.pictures_link:
            self.picture_id += 1
            self.pictures_link.append(link)
            self.download_picture(name=self.picture_id, file_type=pic_or_link[1], url=link)

    def do_the_job(self, url):
        """
        get url, check all links, down all pictures
        and do it over all pages and subpages
        """

        print("run job for = ", url)

        if self.skip_page(url):

            request = Request(url)
            response = None

            try:
                response = urlopen(request)
            except Exception as ex:
                # hey senty.com, can you make a log please? :)
                ...

            if response:
                data = response.read().decode('utf-8')

                # https://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python
                url_link_mask = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
                links = re.findall(url_link_mask, data)
                if links:
                    for link in links:
                        self.final_url_process(link)


if __name__ == "__main__":

    task = Task()
    task.do_the_job('https://exponea.com/')
