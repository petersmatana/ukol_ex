# -*- coding: utf-8 -*-

from urllib.request import Request, urlopen
import urllib
import re


def skip_page(url):
    pdf_pages = re.match(r'.*pdf$', url)

    if pdf_pages:
        return False

    return True


def picture_or_link(url):
    png = re.match(r'.*png$', url)

    if png:
        return 'picture', 'png'
    else:
        return 'link'


def download_picture(name, file_type, url):
    result_name = str(name) + '.' + file_type

    f = open(result_name, 'wb')
    f.write(urlopen(url).read())
    f.close()


def do_the_job(url, all_links):
    """
    get url, check all links, down all pictures
    and do it over all pages and subpages
    """

    print("run job for = ", url)

    if skip_page(url):

        request = Request(url)
        response = None

        try:
            response = urlopen(request)
        except Exception as ex:
            # hey senty.com, can you make a log please? :)
            ...

        if response:
            data = response.read().decode('utf-8')

            pic_name = 0

            # https://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python
            links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data)
            if links:
                for link in links:

                    if link in all_links:
                        continue

                    pic_or_link = picture_or_link(link)

                    if pic_or_link[0] == 'l':

                        exponea_page = re.match('https://exponea.*', link)
                        if exponea_page:
                            print(link)
                            all_links.append(link)
                            do_the_job(link, all_links)

                    if pic_or_link[0] == 'picture':
                        pic_name += 1
                        # download_picture(name=pic_name, file_type=pic_or_link[1], url=link)


if __name__ == "__main__":

    all_links = []

    do_the_job('https://exponea.com/', all_links)
