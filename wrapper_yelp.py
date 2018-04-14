import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
import json
import random

DEFAULT_LOCATION = 'Porto, PT'
SEARCH_LIMIT = 50
OFFSETS=20
CLIENT_ID = "UEpOw_GR3E0vb7-CxYCPlA"
API_KEY = "-py7MDWBERptrew8wySEC99T13FKIvHpjKOe9laLGX-fvyvQB4K93HJNvUQMf0wKeh4P4n61Ab2xxK1tT_sQVh3S7aF0yD2yaK52_Bs3OJSP2XU1qUVfHQQXhBjRWnYx"
URL = "https://api.yelp.com/v3/businesses/search"
SORT_PARAM = "distance"

ratings = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

data = json.load(open("Porto.json"))
df = json_normalize(data["businesses"])


def createNewQuestion(location, difficulty=None):
	if difficulty is not None:
		return
        # TODO
	else:
		rand_ratings = random.sample(set(ratings), 2)
		question = {
			"A" : json.loads(df.loc[df['rating'] == rand_ratings[0]].sample(n = 1, axis = 0).to_json(orient='records'))[0],
			"B" : json.loads(df.loc[df['rating'] == rand_ratings[1]].sample(n = 1, axis = 0).to_json(orient='records'))[0],
		}
		if(rand_ratings.index(min(rand_ratings)) == 0):
			answer = question['A']['name']
		else:
			answer = question['B']['name']
		#print(answer)
		return question, answer

def request(url,api_key,location,offset):
    url_params = {
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT,
        'sort_by': SORT_PARAM,
        'offset':offset,
    }
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }
    response = requests.request('GET', url, headers=headers, params=url_params)
    return response.json()


def getJson():
	out = {
		'businesses': [],
	}
	response = request(URL, API_KEY, DEFAULT_LOCATION, 0)
	out['businesses'].extend(response['businesses'])
	offset = int(response['total']/50) + 1

	for i in range (1, offset):
		response = request(URL, API_KEY, DEFAULT_LOCATION, i*50)
		out['businesses'].extend(response['businesses'])

	locationDataFile=open('test.json', 'w')
	locationDataFile.write(json.dumps(out, indent=4, sort_keys=True))
	locationDataFile.close()

createNewQuestion(DEFAULT_LOCATION)