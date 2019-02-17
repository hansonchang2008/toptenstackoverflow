#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/16 3:39 PM
# @File    : utils.py
# @Software: PyCharm
import requests

headers = {'User-Agent':
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) '
               'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'}


def get(url):
    s = requests.session()
    s.keep_alive = False
    requests.adapters.DEFAULT_RETRIES = 5
    response = s.get(url, headers=headers, timeout=200)
    return response


def xpath_parse(resp, xpath):
    def l_strip(l):
        for i, k in enumerate(l):
            l[i] = k.text.strip()
        return l

    from lxml import etree
    from lxml.etree import HTMLParser
    html = etree.HTML(resp, HTMLParser())
    return html.xpath(xpath), l_strip(html.xpath(xpath))


def top10_newest():
    url = 'https://stackoverflow.com/questions/tagged/android?sort=newest'
    r = get(url)
    questions, questions_text = xpath_parse(r.text, '//*[@class="question-summary"]/div[2]/h3/a')
    links = [i.xpath('./attribute::href')[0].split('/')[2] for i in questions]
    return zip(links[:10], questions_text[:10])


def top10_rated():
    url = 'https://stackoverflow.com/questions/tagged/android?sort=votes'
    r = get(url)
    questions, questions_text = xpath_parse(r.text, '//*[@class="question-summary"]/div[2]/h3/a')
    links = [i.xpath('./attribute::href')[0].split('/')[2] for i in questions]
    return list(zip(links[:10], questions_text[:10]))


if __name__ == '__main__':
    print(top10_rated())
