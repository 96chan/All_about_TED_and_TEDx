#!/usr/bin/python

__author__ = 'JT Huang'
__email__ = 'jthuang@ischool.berkeley.edu'
__python_version = '3.3.0'

import json

#TODO: not orig
SITE_JSON = "tedx_video.json"
YOUTUBE_JSON = "tedx_v5.txt"
MERGED_JSON = "final_tedx.json"

SITE_ATTR_LIST = ['lang', 'event', 'country', 'topic']

# import JSON from site
site_json_file = open(SITE_JSON)
site_json = json.load(site_json_file)
site_json_file.close()

# make video dict site JSON
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
with open(YOUTUBE_JSON, "r") as youtube_json_file:
    for line in youtube_json_file:
        youtube_item_cnt += 1
        youtube_json = json.loads(line)
        vid = youtube_json['id']
        if vid not in video_dict:
            print("No matched: %s" % (vid))
            nomatch_cnt += 1
        else:
            merged_video = {}
            merged_video['id'] = vid
            merged_video['data'] = youtube_json['data']
            for attr in SITE_ATTR_LIST:
                if attr in video_dict[vid]:
                    merged_video['data'][attr] = video_dict[vid][attr]
                    print(json.dumps(merged_video), file=merged_json_file)
            merged_item_cnt += 1

youtube_json_file.close()
merged_json_file.close()

print("site: %d, YouTube: %d, nomatch: %d, merged: %d" % (len(video_dict), youtube_item_cnt, nomatch_cnt, merged_item_cnt))
