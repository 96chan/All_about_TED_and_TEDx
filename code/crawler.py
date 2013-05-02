#!/usr/bin/python

__author__ = 'JT Huang'
__email__ = 'jthuang@ischool.berkeley.edu'
__python_version = '3.3.0'

import urllib.request
from bs4 import BeautifulSoup
import re
import time
import json

####################
# TODO:
# 1. robot.txt
# 2. crawl policy
####################

TEDX_HOME_URL = "http://tedxtalks.ted.com"
PORTAL_URL_LIST = [("lang", "/browse/talks-by-language/"),
                   ("event", "/browse/talks-by-event/"),
                   ("country", "/browse/talks-by-country/"),
                   ("topic", "/browse/talks-by-topic/")]

VIDEO_LINK_PREFIX = "mvp_grid_panel_img_"
MSG_CLASS = "mvp_padded_message"
EMPTY_PAGE_MSG = "This page is empty."

'''
EX:
<embed type="application/x-shockwave-flash" src="http://www.youtube.com/v/lU-3IVqsW0Y&amp;rel=0&amp;fs=1&amp;showsearch=0&amp;enablejsapi=1&amp;modestbranding=1&amp;autoplay=1&amp;playerapiid=mvp_swfo_embed_SF55R92P9Q9B0TBH_331968286" width="634" height="382" style="undefined" id="mvp_swfo_embed_SF55R92P9Q9B0TBH_331968286" name="mvp_swfo_embed_SF55R92P9Q9B0TBH_331968286" quality="high" allowfullscreen="true" allowscriptaccess="always" wmode="opaque" loop="false">
'''
# NOTE: byte string
VIDEO_ID_RE = b"""
<embed.*\ src=\\\\\".*/v/(.*?)\\\\\".*>.*</embed>
"""

SLEEP_TIME = 1

JSON_FILE = "tedx_video.json"

# storing data structures
# TODO: may use dict instead of list to prevent link duplication
portal_links = { 'lang': [], 'event': [], 'country': [], 'topic': []}
video_dict = {} # { url: { 'lang': , 'event': , 'country': , 'topic': }, ... }


def req_resp(url):
    try:
        time.sleep(SLEEP_TIME)
        resp = urllib.request.urlopen(url)
        return resp
    except urllib.error.URLError as err:
        print("Error opening url {} .\nError is: {}".format(url, err))
        return False 

####################
# Stage 1 - Get Type Protals from Home URL
####################
def get_type_protal_links(home_url):
    resp = req_resp(home_url)
    if not resp: return False

    soup = BeautifulSoup(resp.readall())
    link_tags = soup.find_all('a', href=True)

    for link_tag in link_tags:
        link = link_tag['href']
        content = link_tag.next_element.next_element.next_element
        for ptype, burl in PORTAL_URL_LIST:
            if link.startswith(burl):
                # EX: http://tedxtalks.ted.com/browse/talks-by-language/chinese
                portal_links[ptype].append((link, content))
                print("%s: %s %s" % (ptype, content, link))
                break

####################
# Stage 2 - Go to Type Protals and Get Video Links (also paging)
####################
def get_video_links(ptype, ptype_val, portal_url):
    page = 1
    while(True):
        # EX: http://tedxtalks.ted.com/browse/talks-by-language/chinese?page=3
        url = portal_url + "?page=" + str(page)
        resp = req_resp(url)
        print("Reading URL: " + url)
        if not resp: return False

        soup = BeautifulSoup(resp.readall())
        link_tags = soup.find_all('a', id=re.compile(VIDEO_LINK_PREFIX), href=True)
        for link_tag in link_tags:
            link = link_tag['href']
            # EX: from /list/search%3Atag%3A%22chinese%22/video/The-tragedy-of-Hong-Kong-Archiv
            # to /video/The-tragedy-of-Hong-Kong-Archiv
            pos = link.find("/video")
            link = link[pos:]
            if link not in video_dict:
                video_dict[link] = {}
                video_dict[link][ptype] = ptype_val
                # get video ID
                video_dict[link]['id'] = get_video_ID(TEDX_HOME_URL+link)
            else:
                video_dict[link][ptype] = ptype_val

            print("video link: %s (attr %s: %s)" % (link, ptype, ptype_val))

        # if there is no Next page
        # <div class="mvp_padded_message">This page is empty.</div>
        msg_tag = soup.find('div', {'class': MSG_CLASS})
        if msg_tag and msg_tag.get_text() == EMPTY_PAGE_MSG:
            print("empty page.")
            break

        page += 1


####################
# Stage 3 - Get Video ID
####################
def get_video_ID(video_url):
    resp = req_resp(video_url)
    if not resp: return ""

    html = resp.readall()
    video_ids = re.findall(VIDEO_ID_RE, html, re.IGNORECASE|re.VERBOSE)
    for video_id in video_ids:
        # NOTE: byte string => need decode
        print("YouTube ID: %s (%s)" % (video_url, video_id.decode('utf-8')))
        return video_id.decode('utf-8')



####################
# Main
####################

'''
# NOTE: main section may take a long time to be executed
get_type_protal_links(TEDX_HOME_URL)
print(portal_links)

for ptype in portal_links:
    ptype_portal_list = portal_links[ptype]
    for link, ptype_val in ptype_portal_list:
        get_video_links(ptype, ptype_val, TEDX_HOME_URL+link)

f = open(JSON_FILE, 'w')
f.write(json.dumps(video_dict))
f.close()
'''

# test section
get_video_links("lang", "American Sign Language", "http://tedxtalks.ted.com/browse/talks-by-language/asl")
f = open(JSON_FILE, 'w')
f.write(json.dumps(video_dict))
f.close()

# test section 2
#get_video_ID("http://tedxtalks.ted.com/video/Quality-and-dynamic-longetivity"))
