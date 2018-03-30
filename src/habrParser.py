#!/usr/bin/env python3
# encoding: utf-8

import os
import re
from lxml.html import parse
from lxml.builder import E
from urllib.request import urlopen 

# 3k -> 3000
# 10 -> 10
# 3,2k -> 3200
def _normalize_views_count(views_string):
    r = re.search(r'([0-9]+\,[0-9]|[0-9]+)(k|m)?',views_string)
    num_part = float(r.group(1).replace(',','.') if ',' in r.group(1) else r.group(1))
    if r.group(2) == 'k':
        mult_part = 1000
    else:
        mult_part = 1

    try:
        return int(num_part*mult_part)
    except:
        return -1

def _body2text(body):
    # TODO: Сделать преобразование тела поста в plain text
    return 'Not implemented, TODO body2text'

_find_tags = {
    'title': '//h1[@class="post__title post__title_full"]/span[@class="post__title-text"]',
    'author': '//span[@class="user-info__nickname user-info__nickname_small"]',
    'body': '//div[@class="post__text post__text-html js-mediator-article"]',
    'rating': '//span[@class="voting-wjt__counter voting-wjt__counter_positive  js-score"]',
    'comments count': '//strong[@class="comments-section__head-counter"]',
    'views count': '//span[@class="post-stats__views-count"]',
    'bookmarks count': '//span[@class="bookmark__counter js-favs_count"]'
}
def parseHabr(link):
    try:
        post = {
            'title': None,
            'body': None, 
            'author': None, 
            'rating': None, 
            'comments': None,
            'views': None,
            'bookmarks': None
            }

        data = parse(urlopen(link))

        post['title'] = data.find(_find_tags['title']).text
        try:
            post['author'] = data.find(_find_tags['author']).text
        except: # TODO: test this error
            post['author'] = None

        try:
            post['body'] = _body2text(data.find(_find_tags['body']))
        except:
            post['body'] = None

        try:
            post['rating'] = int(data.find(_find_tags['rating']).text)
        except: 
            post['rating']=None

        try:
            # TODO: А если комментариев > 1000, то будет число, или же 1k?
            post['comments'] = int(data.find(_find_tags['comments count']).text)
        except: 
            post['comments'] = None

        try:
            raw_views = data.find(_find_tags['views count']).text
            post['views'] = _normalize_views_count(raw_views)
        except:
            post['views'] = None

        try:
            post['bookmarks'] = int(data.find(_find_tags['bookmarks count']).text)
        except:
            post['bookmarks'] = None

        return post
    except IOError as e:
        print(e)
