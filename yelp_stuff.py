import requests
import json

DEFAULT_TERM = 'restaurant'
DEFAULT_LOCATION = 'Porto, PT'
SEARCH_LIMIT = 50
OFFSETS=20
CLIENT_ID = "UEpOw_GR3E0vb7-CxYCPlA"
API_KEY = "-py7MDWBERptrew8wySEC99T13FKIvHpjKOe9laLGX-fvyvQB4K93HJNvUQMf0wKeh4P4n61Ab2xxK1tT_sQVh3S7aF0yD2yaK52_Bs3OJSP2XU1qUVfHQQXhBjRWnYx"
URL = "https://api.yelp.com/v3/businesses/search"

def createNewQuestion(location):
    question = {
        "A": {"nome": "Café do barbosa", "tipo": "cafe",
              "img_url": "http://oje-50ea.kxcdn.com/wp-content/uploads/2017/03/cafe-925x578.jpg"},
        "B": {"nome": "Café do Zé", "tipo": "cafe",
              "img_url": "https://i.imgur.com/LoL7n.jpg"}
    }
    answer = "Café do Zé"
    return question, answer

def getAllInformationAvailable(location):
    offsets=OFFSETS
    temp={"businesses":[]}
    for i in range(0,offsets):
        response=request(URL,API_KEY,DEFAULT_TERM,location,i)
        responses=json.loads(response)
        # if response.find("404"):
        #     break
        # else:
        #     print("test")no
        # value=responses
        temp["businesses"]=temp["businesses"]+responses["businesses"]

    return temp


def request(url,api_key,term,location,offset):
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT,
        'offset':offset
    }
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }
    response = requests.request('GET', url, headers=headers, params=url_params)
    response=json.dumps(response.json())
    return response
"""
Creates a Json File with the first 1000 results of the restaurants of a given location.

String location- Ex:"Porto, PT" 
"""
def create_json(location):
    responses = getAllInformationAvailable(location)
    location=location.replace(", ", '')
    locationDataFile=open(location+'.json', 'w')
    locationDataFile.write(json.dumps(responses, indent=4, sort_keys=True))
    locationDataFile.close()
if __name__ == "__main__":
    #responses =request(URL,API_KEY,DEFAULT_TERM,DEFAULT_LOCATION,0)
    location=DEFAULT_LOCATION
    create_json(location)
    #print(responses)
