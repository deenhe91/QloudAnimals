
# Flickr API [get photo list]

import requests #requesting
import shutil #image processing
import base64 #image processing
from googleapiclient import discovery #google api
from oauth2client.client import GoogleCredentials #google api
import os #google api (making environmental variable)
from collections import defaultdict # initially storing labels and urls
 # transfer of info to firebase storage
from firebase.firebase import FirebaseApplication, FirebaseAuthentication
from firebase import firebase

import json

# using the flickr API

flickr_key = '11edab83a734a506db6af791bf0c86f9'
flickr_secret = 'ff2f0298eaf4853a'

r = requests.get('https://api.flickr.com/services/rest/?method=flickr.groups.pools.getPhotos&api_key=6d3c21bdbff3887ae3eb063c75fd0195&group_id=61595479%40N00&per_page=500&format=json&nojsoncallback=1')
flickr_list = r.json()

img_info = flickr_list['photos']['photo']
print('\nnumber of photos: ', len(img_info))

with open('flickr_response', 'w') as outfile:
	json.dump(img_info, outfile) # for these purposes save so can tackle stage by stage

# FUNCTIONS: 
# 1. compile URLs, download image at url.

"""format: https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}.jpg"""

def get_URL(img):
	url = 'https://c1.staticflickr.com/'+str(img['farm'])+'/'+str(img['server'])+'/'+str(img['id'])+'_'+str(img['secret'])+'_b.jpg'
	response = requests.get(url, stream=True)
	
	with open('img.png', 'wb') as out_file:
		shutil.copyfileobj(response.raw, out_file)

	del response
	return url


urls = [] # create list of urls. 

for img in img_info:
	url = get_URL(img)
	urls.append(url)


b64_strings = [] # create list of b64_strings

for url in urls:
	response = requests.get(url, stream=True)
	
	with open('img.png', 'wb') as f:
		shutil.copyfileobj(response.raw, f)
	with open('img.png', 'rb') as f:
		encoded_string = base64.b64encode(f.read())
		b64_strings.append(encoded_string)

del response


# 2. encode downloaded image and send to google vision API for labeling.
# Save labels.

DISCOVERY_URL = 'https://vision.googleapis.com/$discovery/rest?version=v1'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'q-dev-challenge-hannah-47b6d0e98d36.json'
credentials = GoogleCredentials.get_application_default()	

service = discovery.build('vision', 'v1', credentials=credentials, discoveryServiceUrl=DISCOVERY_URL)

googlers = [] #create list of google responses

for string in b64_strings:
	service_request = service.images().annotate(body={'requests': [{'image': {'content': string.decode('UTF-8')},'features': [{'type': 'LABEL_DETECTION','maxResults': 5}]}]})
	response = service_request.execute()
	labels = response['responses'][0]['labelAnnotations']
	googlers.append(labels)




# firebase firebase firebase

if __name__ == '__main__':
    SECRET = 'D9TpBzyLhSv6yJX59YeBcijiNAYWTkSMlvmAPBAK'
    DSN = 'https://firebase.q-dev-challenge-hannah.firebaseapp.com'
    EMAIL = 'hannah.deen91@email.com'
    authentication = FirebaseAuthentication(SECRET,EMAIL, True, True)
    firebase = FirebaseApplication(DSN, authentication)


# firebase = firebase.FirebaseApplication('https://q-dev-challenge-hannah.firebaseio.com', None)
firebase.get('/labels', None, params={'print': 'pretty'})


with open('flickr_response') as f:
	img_info = json.load(f)



i = 0
for img in img_info[1:10]:
	url = get_URL(img)
	labels = Googlify('img.png')

	for label in labels:
		data = {'label': label['description'], 'score': label['score'], 'image_url': url}
		snapshot = firebase.post('/labels', data)
		# print(snapshot['label'])
	def callback_get(response):
        with open('/dev/null', 'w') as f:
            f.write(response)
    firebase.get_async('/labels', snapshot['name'], callback=callback_get)
	
	i = i+1
	print('Image ', i)
	os.remove('img.png')













