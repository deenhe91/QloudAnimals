
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
import sys

# using the flickr API

flickr_key = '11edab83a734a506db6af791bf0c86f9'
flickr_secret = 'ff2f0298eaf4853a'

flickr_file = []

flickr_file = []

group_id = input("enter group id : ")
pages = input("enter number of pages (default set to 500 results per page) :\n\n ")

def get_flickrd(group_id, pages):
	for i in range(int(pages)):
		r = requests.get('https://api.flickr.com/services/rest/?method=flickr.groups.pools.getPhotos&api_key=2591413f0cceaf433dff5018e4ef3228&group_id='+str(group_id)+'&per_page=500&page='+str(i)+'&format=json&nojsoncallback=1')
		flickr_json = r.json()
		flickr_file.append(flickr_json)

	img_info = []
	for page in flickr_file:
		img_info.append(page['photos']['photo'])
	return img_info

img_info = get_flickrd(group_id, pages)

print('\nnumber of pages: ', len(img_info), ' , number of images per page: ', len(img_info[0]))

with open('flickr.json', 'w') as outfile:
	json.dump(flickr_file, outfile) # for these purposes save so can tackle stage by stage


'''with open('flickr.json') as file:
    img_info = json.load(file)'''

# FUNCTIONS: 
# 1. compile URLs, download image at url.

"""format: https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}.jpg"""

urls = [] # create list of urls. 

print('\ncompiling urls...\n')

for img in img_info:
	url = 'https://c1.staticflickr.com/'+str(img['farm'])+'/'+str(img['server'])+'/'+str(img['id'])+'_'+str(img['secret'])+'_b.jpg'
	urls.append(url)

with open('urls', 'wb') as f:
	pickle.dump(urls, f)

print('urls compiled and stored at urls\n')

b64_strings = [] # create list of b64_strings

print('\n downloading and b64 encoding images...\n')

i = 0

for url in urls:
	i += 1

	response = requests.get(url, stream=True)
	
	with open('img.png', 'wb') as f:
		shutil.copyfileobj(response.raw, f)

	with open('img.png', 'rb') as f:
		encoded_string = base64.b64encode(f.read())
		b64_strings.append(encoded_string)

	print('encoding image : '+str(i))

del response


# 2. encode downloaded image and send to google vision API for labeling.
# Save labels.

print('getting our machine learning on....')


DISCOVERY_URL = 'https://vision.googleapis.com/$discovery/rest?version=v1'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'q-dev-challenge-hannah-47b6d0e98d36.json'
credentials = GoogleCredentials.get_application_default()	

service = discovery.build('vision', 'v1', credentials=credentials, discoveryServiceUrl=DISCOVERY_URL)

googlers = [] #create list of google responses

i = 0

for string in b64_strings:
	i += 1

	service_request = service.images().annotate(body={'requests': [{'image': {'content': string.decode('UTF-8')},'features': [{'type': 'LABEL_DETECTION','maxResults': 5}]}]})
	
	response = service_request.execute()
	
	if 'labelAnnotations' in response['responses'][0]:
		labels = response['responses'][0]['labelAnnotations']
		googlers.append(labels)
		print('string :'+ str(i))
	else:
		print('SKIPPED string : ' +str(i))
	

print('googling done... saving results\n\n')

with open('google_results.json', 'wb') as f:
	pickle.dump(googlers, f)




fb_dictionary = {}

for i in range(len(googlers)):
	for label in googlers[i]:
		url_and_score = (label['score'], new_urls[i])
		
		if label['description'] in fb_dictionary:
			fb_dictionary[label['description']].append(url_and_score)
		else:
			fb_dictionary[label['description']] = [url_and_score]


# find only animal labels with google vision api??









