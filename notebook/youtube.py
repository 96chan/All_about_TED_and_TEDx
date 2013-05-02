#https://developers.google.com/youtube/articles/view_youtube_jsonc_responses
#https://developers.google.com/youtube/2.0/developers_guide_jsonc

import requests
import json
import time

f= open('tedx_v7.txt','w')

user_id = "tedxtalks"
page = 1
maxcount = 25
count = 0
start_index = 0

# Obtaining Total page number
s = requests.get("https://gdata.youtube.com/feeds/api/users/"+user_id+"/uploads?v=2&alt=jsonc&start-index=1&max-result=1")
data = [json.loads(row) for row in s.content.split("\n") if row]
totalcount = data[0]['data']['totalItems']
pagenumber = totalcount/maxcount +1

key = ['id', 'uploaded', 'category', 'title', 'tags', 'thumbnail', 'duration', 'likeCount', 'rating', 'ratingCount', 'viewCount', 'favoriteCount', 'commentCount'] 
tedx ={'id':'',
        'data':{
                   'uploaded':'',
                   'title':'',
                   'tags':'',
                   'thumbnail':'',
                   'duration':'',
                   'likeCount':'',
                   'rating':'',
                   'ratingCount':'',
                   'viewCount':'',
                   'favoriteCount':'',
                   'commentCount':''
       }
}

# Obtaining Data from each page
for index in range(1,pagenumber):
    # changing index number 
    if index == 1:
        start_index = 1
    else:
        start_index = index*maxcount
    
    s = requests.get("https://gdata.youtube.com/feeds/api/users/"+user_id+"/uploads?v=2&alt=jsonc&start-index="+str(start_index)+"&max-result="+str(maxcount))
    data = [json.loads(row) for row in s.content.split("\n") if row]
    metadata = data[0]['data']['items']
    
    # obtaining each data in a page (25 items)
    for i in range(len(metadata)):
        count +=1
        u = metadata[i]

        #missing key-value pair
        for j in key:
            if j=='id':
                tedx['id']=u['id']
            elif j =='thumbnail':
                tedx['data'][j] = u[j][u'hqDefault']
            elif j == 'title': 
                tedx['data'][j] = u[j].encode('utf-8')
            else:
                tedx['data'][j] = u[j] if not j in list(set(key) -set(u.keys())) else '-'
        
        the_dump = json.dumps(tedx)
        print >>f, the_dump
#        print count, tedx['id']    
    print 'completed '+str(count)

    # delay
    time.sleep(1)

# https://developers.google.com/youtube/2.0/developers_guide_jsonc 
    

