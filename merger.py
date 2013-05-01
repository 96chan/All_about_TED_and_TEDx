#!/usr/bin/python

__author__ = 'JT Huang'
__email__ = 'jthuang@ischool.berkeley.edu'
__python_version = '3.3.0'

import json

#TODO: not orig
SITE_JSON = "tedx_video.json"
YOUTUBE_JSON = "tedx_v7.txt"
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
losing_cnt = {'lang': 0, 'topic': 0, 'event': 0, 'country': 0}
losing_attr_cnt = 0
chinese_match_cnt = 0
chinese_nomatch_cnt = 0
with open(YOUTUBE_JSON, "r") as youtube_json_file:
    for line in youtube_json_file:
        youtube_item_cnt += 1
        youtube_json = json.loads(line)
        vid = youtube_json['id']
        merged_video = youtube_json['data']
        merged_video['id'] = vid
        if vid not in video_dict:
            print("No matched: %s" % (vid))
            nomatch_cnt += 1
        else:
            video_dict[vid]['checked'] = True
            if 'lang' in video_dict[vid] and (video_dict[vid]['lang'] == "Chinese"):
                chinese_match_cnt += 1
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
        if 'lang' in video_dict[vid] and (video_dict[vid]['lang'] == "Chinese"):
            chinese_nomatch_cnt += 1
        for attr in SITE_ATTR_LIST:
            if attr in video_dict[vid]:
                merged_video[attr] = video_dict[vid][attr]
        print(json.dumps(merged_video), file=merged_json_file)

youtube_json_file.close()
merged_json_file.close()

print("site: %d, YouTube: %d, nomatch: %d, merged: %d (losing_cnt: %d)" % (len(video_dict), youtube_item_cnt, nomatch_cnt, merged_item_cnt, losing_attr_cnt))
for attr in SITE_ATTR_LIST:
    print("losing %s: %d" % (attr, losing_cnt[attr]))
print(chinese_match_cnt, chinese_nomatch_cnt)
