
# Flickr API [get photo list]

import requests

flickr_key = '11edab83a734a506db6af791bf0c86f9'
flickr_secret = 'ff2f0298eaf3853a'

r = requests.get('https://api.flickr.com/services/rest/?method=flickr.groups.pools.getPhotos&api_key=21450f186812ae1b7a79ac7c3e1cd4ef&group_id=61595479%40N00&format=json&nojsoncallback=1')
flickr_list = r.json()

img_info = flickr_list['photos']['photo']
print('\nnumber of photos: ', len(img_info))


# Compile URLs
# format: https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}.jpg
import shutil
import base64

'''define a function here and then do for img in images apply function'''

for img in img_info:
	url = 'https://c1.staticflickr.com/'+str(img['farm'])+'/'+str(img['server'])+'/'+str(img['id'])+'_'+str(img['secret'])+'_b.jpg'

# Download image at URL
	response = requests.get(url, stream=True)
	with open('img.png', 'wb') as out_file:
    	shutil.copyfileobj(response.raw, out_file)
	del response

# 64base encode image
	with open("img.png", "rb") as image_file:
    	encoded_string = base64.b64encode(image_file.read())


# Vision API [get labels for encoded photo]
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import os

	DISCOVERY_URL = 'https://vision.googleapis.com/$discovery/rest?version=v1'
	os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'q-dev-challenge-hannah-47b6d0e98d36.json'
    
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials,
                              discoveryServiceUrl=DISCOVERY_URL)

service_request = service.images().annotate(body={
	'requests': [{
		'image': {
		'content': encoded_string.decode('UTF-8')
	},
	'features': [{
		'type': 'LABEL_DETECTION',
		'maxResults': 10
	}]
}]
})

response = service_request.execute()
label = response['responses'][0]['labelAnnotations'][0]['description']
print('Found label: %s for %s' % (label, photo_file))
return 0

# Send labels and URL to Firebase store













