# -*- coding: utf-8 -*-

from urllib.request import Request, urlopen
import urllib
import re


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


if __name__ == "__main__":
    request = Request('https://exponea.com/')
    response = urlopen(request)
    data = response.read().decode('utf-8')

    pic_name = 0

    # https://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python
    links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data)
    if links:
        for link in links:

            pic_or_link = picture_or_link(link)
            if pic_or_link[0] == 'picture':
                pic_name += 1
                download_picture(name=pic_name, file_type=pic_or_link[1], url=link)
