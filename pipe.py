
# Flickr API [get photo list]

import requests #requesting
import shutil #image processing
import base64 #image processing
from googleapiclient import discovery #google api
from oauth2client.client import GoogleCredentials #google api
import os #google api (making environmental variable)
from collections import defaultdict # initially storing labels and urls
 # transfer of info to firebase storage
# from firebase.firebase import FirebaseApplication, FirebaseAuthentication
# from firebase import firebase

import json
import pickle

# using the flickr API

# flickr_key = '11edab83a734a506db6af791bf0c86f9'
# flickr_secret = 'ff2f0298eaf4853a'

# r = requests.get('https://api.flickr.com/services/rest/?method=flickr.groups.pools.getPhotos&api_key=2591413f0cceaf433dff5018e4ef3228&group_id=61595479%40N00&per_page=500&page=2&format=json&nojsoncallback=1')
# flickr_list2 = r.json()

# img_info2 = flickr_list2['photos']['photo']
# print('\nnumber of photos: ', len(img_info2))

# with open('flickr_response2', 'w') as outfile:
# 	json.dump(img_info2, outfile) # for these purposes save so can tackle stage by stage


with open('flickr_response2') as file:
    img_info2 = json.load(file)

# FUNCTIONS: 
# 1. compile URLs, download image at url.

"""format: https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}.jpg"""

# def get_URL(img):
# 	url = 'https://c1.staticflickr.com/'+str(img['farm'])+'/'+str(img['server'])+'/'+str(img['id'])+'_'+str(img['secret'])+'_b.jpg'
# 	response = requests.get(url, stream=True)
	
# 	with open('img.png', 'wb') as out_file:
# 		shutil.copyfileobj(response.raw, out_file)

# 	del response
# 	return url


urls2 = [] # create list of urls. 

print('\ncompiling urls...\n')

for img in img_info2:
	url = url = 'https://c1.staticflickr.com/'+str(img['farm'])+'/'+str(img['server'])+'/'+str(img['id'])+'_'+str(img['secret'])+'_b.jpg'
	urls2.append(url)

print('urls compiled and stored at urls2\n')

b64_strings2 = [] # create list of b64_strings

print('\n downloading and b64 encoding images...\n')

i = 0

for url in urls2:
	i += 1
	response = requests.get(url, stream=True)
	
	with open('img.png', 'wb') as f:
		shutil.copyfileobj(response.raw, f)
	with open('img.png', 'rb') as f:
		encoded_string = base64.b64encode(f.read())
		b64_strings2.append(encoded_string)
	print(i)

del response


# 2. encode downloaded image and send to google vision API for labeling.
# Save labels.

print('getting our machine learning on....')


DISCOVERY_URL = 'https://vision.googleapis.com/$discovery/rest?version=v1'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'q-dev-challenge-hannah-47b6d0e98d36.json'
credentials = GoogleCredentials.get_application_default()	

service = discovery.build('vision', 'v1', credentials=credentials, discoveryServiceUrl=DISCOVERY_URL)

# googlers2 = [] #create list of google responses

i = 0

for string in b64_strings2:
	i += 1
	service_request = service.images().annotate(body={'requests': [{'image': {'content': string.decode('UTF-8')},'features': [{'type': 'LABEL_DETECTION','maxResults': 5}]}]})
	response = service_request.execute()
	labels = response['responses'][0]['labelAnnotations']
	print('string :'+ str(i))
	googlers2.append(labels)

# print('googling done... saving results\n\n')

# with open('google_results2.json', 'wb') as f:
# 	pickle.dump(googlers2, f)

# with open('urls2', 'wb') as f:
# 	pickle.dump(urls2, f)

# googlers : 498 label sets
# short_urls : urls relevant to googler results



# with open('flickr_response2') as f:
# 	img_info = json.load(f)



# i = 0
# for img in img_info[1:10]:
# 	url = get_URL(img)
# 	labels = Googlify('img.png')

# 	for label in labels:
# 		data = {'label': label['description'], 'score': label['score'], 'image_url': url}
# 		snapshot = firebase.post('/labels', data)
# 		# print(snapshot['label'])
# 	def callback_get(response):
#         with open('/dev/null', 'w') as f:
#             f.write(response)
#     firebase.get_async('/labels', snapshot['name'], callback=callback_get)
	
# 	i = i+1
# 	print('Image ', i)
# 	os.remove('img.png')


fb_dictionary = {}

for i in range(len(googlers2)):
	for label in googlers[i]:
		url_and_score = (label['score'], sh_urls2[i])
		
		if label['description'] in fb_dictionary:
			fb_dictionary[label['description']].append(url_and_score)
		else:
			fb_dictionary[label['description']] = [url_and_score]


# find only animal labels with google vision api??









