#!/usr/bin/python

__author__ = 'JT Huang'
__email__ = 'jthuang@ischool.berkeley.edu'
__python_version = '3.3.0'

import json
import requests

def get_FB_info(url):
    url = "http://graph.facebook.com/fql?q=SELECT%20url,%20normalized_url,%20share_count,%20like_count,%20comment_count,%20total_count,commentsbox_count,%20comments_fbid,%20click_count%20FROM%20link_stat%20WHERE%20url='" + url + "'"
    r = requests.get(url)

    '''
    EX:
    {
        "data": [
            {
                "url": "http://www.youtube.com/watch?v=Ws2y-cGoWqQ",
                "normalized_url": "http://www.youtube.com/watch?v=Ws2y-cGoWqQ",
                "share_count": 99,
                "like_count": 131,
                "comment_count": 78,
                "total_count": 308,
                "commentsbox_count": 0,
                "comments_fbid": 462100607175333,
                "click_count": 0
            }
        ]
    }
    '''
    data = json.loads(r.content)["data"][0]
    print(data)
    print(data["total_count"])

def get_twitter_info(url):
    url = "http://urls.api.twitter.com/1/urls/count.json?url=" + url
    r = requests.get(url)

    '''
    EX:
    {"count":13,"url":"http:\/\/www.youtube.com\/watch\/?v=Ws2y-cGoWqQ"}
    '''
    data = json.loads(r.content)
    print(data)
    print(data["count"])


URL = "http://www.youtube.com/watch?v=Ws2y-cGoWqQ"
# get_FB_info(URL)
get_twitter_info(URL)
