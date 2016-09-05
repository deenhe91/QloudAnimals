from firebase import Firebase
import urllib3 as urllib
from urllib.parse import urlparse
import pickle

with open('google_results', 'rb') as f:
	googlers = pickle.load(f)

with open('urls', 'rb') as f:
	urls = pickle.load(f) 



f = Firebase('https://firebase.q-dev-challenge-hannah.firebaseapp.com', auth_token='D9TpBzyLhSv6yJX59YeBcijiNAYWTkSMlvmAPBAK')


for g in range(len(googlers)):
	for label in googlers[g]:
		f.push({'label': label['description'], 'score': label['score'], 'url': urls[g]})

