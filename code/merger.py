#!/usr/bin/python
from __future__ import print_function

__author__ = 'JT Huang'
__email__ = 'jthuang@ischool.berkeley.edu'
__python_version = '3.3.0'

import json
import requests
import time

SITE_JSON = "../data/tedx_video.json"
YOUTUBE_JSON = "../data/datamining_sample.txt"
MERGED_JSON = "../data/final_datamining_ted.json"
VIDEO_URL_PREFIX = "http://www.youtube.com/watch?v="

TEDX_SEP = "************ tedxtalks\n"
TED_SEP = "************ TEDtalksDirector\n"

SITE_ATTR_LIST = ['lang', 'event', 'country', 'topic']
SITE_ATTR_DEF = {'lang': 'English', 'event': 'TEDTalks', 'country': 'United States', 'topic': ''}


def add_social_attr(video_data):
    # Getting Facebook
    FB_url = "http://graph.facebook.com/fql?q=SELECT%20share_count,like_count,comment_count,total_count,commentsbox_count,click_count%20FROM%20link_stat%20WHERE%20url='" + VIDEO_URL_PREFIX + video_data['id'] + "'" 
    print("Getting FB data for %s" % (video_data['id']))
    time.sleep(1)
    r = requests.get(FB_url)

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
    json_data = json.loads(r.content)
    FB_data = json_data["data"][0]
    for key in FB_data:
        video_data["FB_" + key] = FB_data[key]

    # Getting Twitter
    twitter_url = "http://urls.api.twitter.com/1/urls/count.json?url=" + VIDEO_URL_PREFIX + video_data['id']
    print("Getting Twitter data for %s" % (video_data['id']))
    try:
        r = requests.get(twitter_url)
    except requests.exceptions.ConnectionError as err:
        print("Losting Twitter attr of %s" % (video_data['id']))

    '''
    EX:
    {"count":13,"url":"http:\/\/www.youtube.com\/watch\/?v=Ws2y-cGoWqQ"}
    '''
    json_data = json.loads(r.content)
    video_data["twitter_count"] = json_data['count']
        

    return video_data



# import JSON from site
site_json_file = open(SITE_JSON)
site_json = json.load(site_json_file)
site_json_file.close()

# make video dict from site JSON
video_dict = {}
for video in site_json:
    vid = site_json[video]['id']
    video_dict[vid] = {}
    for attr in SITE_ATTR_LIST:
        if attr in site_json[video]:
            video_dict[vid][attr] = site_json[video][attr]

# get JSON from YouTube and print to merged result file
merged_json_file = open(MERGED_JSON, "w")
merged_item_cnt = 0
youtube_item_cnt = 0
nomatch_cnt = 0
losing_cnt = {'lang': 0, 'topic': 0, 'event': 0, 'country': 0}
losing_attr_cnt = 0
is_ted = False
with open(YOUTUBE_JSON, "r") as youtube_json_file:
    for line in youtube_json_file:
        if line == TED_SEP:
            is_ted = True
            continue
        elif line == TEDX_SEP:
            continue

        youtube_item_cnt += 1
        if (youtube_item_cnt % 600 == 0):
            time.sleep(1)
        youtube_json = json.loads(line)
        vid = youtube_json['id']
        merged_video = youtube_json
        merged_video = add_social_attr(merged_video)

        if is_ted:
            for key in SITE_ATTR_DEF:
                merged_video[key] = SITE_ATTR_DEF[key]
            merged_item_cnt += 1
        elif vid not in video_dict:
            print("No matched: %s" % (vid))
            nomatch_cnt += 1
        else:
            video_dict[vid]['checked'] = True
            for attr in SITE_ATTR_LIST:
                if attr in video_dict[vid]:
                    merged_video[attr] = video_dict[vid][attr]
                else:
                    print("losing attr %s of %s" % (attr, vid))
                    losing_cnt[attr] += 1
                    losing_attr_cnt += 1
            merged_item_cnt += 1
        print(json.dumps(merged_video), file=merged_json_file)

for vid in video_dict:
    if 'checked' not in video_dict[vid]:
        merged_video = {}
        merged_video['id'] = vid
        for attr in SITE_ATTR_LIST:
            if attr in video_dict[vid]:
                merged_video[attr] = video_dict[vid][attr]
        print(json.dumps(merged_video), file=merged_json_file)

youtube_json_file.close()
merged_json_file.close()

print("site: %d, YouTube: %d, nomatch: %d, merged: %d (losing_cnt: %d)" % (len(video_dict), youtube_item_cnt, nomatch_cnt, merged_item_cnt, losing_attr_cnt))
for attr in SITE_ATTR_LIST:
    print("losing %s: %d" % (attr, losing_cnt[attr]))
