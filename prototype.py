# -*- coding: utf-8 -*-

from urllib.request import Request, urlopen
import re

if __name__ == "__main__":
    request = Request('https://exponea.com/')
    response = urlopen(request)
    data = response.read().decode('utf-8')

    # https://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python
    pic1 = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data)
    if pic1:
        for x in pic1:
            print(x)
