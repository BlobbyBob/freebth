#!/usr/bin/env python

import urllib.request

from CustomHTMLParser import CustomHTMLParser

if __name__ == '__main__':
    # Fetch list of gyms
    gyms = []
    baseUrl = 'https://stadtplan.bonn.de/cms/cms.pl?Amt=Stadtplan&set=5_1_1_1&act=1&Drucken=1&umtausch=&geoid='

    for i in range(0, 210, 10):
        req = urllib.request.urlopen(baseUrl + str(i))
        contentType = req.info().get('Content-Type')
        resp = req.read().decode(contentType.split('=')[1])
        parser = CustomHTMLParser()
        parser.feed(resp)
        print(parser.infos)
        break  # todo remove in productin
