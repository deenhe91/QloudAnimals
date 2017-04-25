import requests
import sys
import json
import shutil #image processing
import base64 #image processing
from googleapiclient import discovery #google api
from oauth2client.client import GoogleCredentials #google api
import os #google api (making environmental variable)

import pickle

flickr_key = 
flickr_secret = 

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




print('compiling urls. . . \n')

urls = []

for page in img_info:
	for img in page:
		url = 'https://c1.staticflickr.com/'+str(img['farm'])+'/'+str(img['server'])+'/'+str(img['id'])+'_'+str(img['secret'])+'_b.jpg'
		urls.append(url)

with open('pickles/urls', 'wb') as f:
	pickle.dump(urls, f)

print('urls compiled and saved in pickles/urls. \n')


print('getting our machine learning on....')


DISCOVERY_URL = 'https://vision.googleapis.com/$discovery/rest?version=v1'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'q-dev-challenge-hannah-47b6d0e98d36.json'
credentials = GoogleCredentials.get_application_default()

service = discovery.build('vision', 'v1', credentials=credentials, discoveryServiceUrl=DISCOVERY_URL)


def google(url):
	response = requests.get(url, stream=True)
	with open('img.png', 'wb') as f:
		shutil.copyfileobj(response.raw, f)
	with open('img.png', 'rb') as f:
		encoded_string = base64.b64encode(f.read())
	service_request = service.images().annotate(body={'requests': [{'image': {'content': encoded_string.decode('UTF-8')},'features': [{'type': 'LABEL_DETECTION','maxResults': 5}]}]})
	response = service_request.execute()
	if 'labelAnnotations' in response['responses'][0]:
		labels = response['responses'][0]['labelAnnotations']
		print('complete')
	else:
		print('SKIPPED image')
	return labels


googlers = []

i = 0

for url in urls:
	i += 1
	g = google(url)
	googlers.append(g)
	print(i)

print('googling done... saving results\n\n')



with open('google_results.json', 'wb') as f:
	pickle.dump(googlers, f)

	print('encoding image : '+str(i))

del response

with open('pickles/dic.pickle', 'rb') as infile:
	dic = pickle.load(infile)

for i in range(len(googlers)):
	for label in googlers[i]:
		url_and_score = (label['score'], done_urls[i])
		
		if label['description'] in dic:
			dic[label['description']].append(url_and_score)
		else:
			dic[label['description']] = [url_and_score]



