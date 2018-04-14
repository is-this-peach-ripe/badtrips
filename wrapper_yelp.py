import requests
import pandas as pd
from pandas.io.json import json_normalize
import json
import random

DEFAULT_LOCATION = 'Porto, PT'
SEARCH_LIMIT = 50
OFFSETS = 20
CLIENT_ID = "UEpOw_GR3E0vb7-CxYCPlA"
API_KEY = "-py7MDWBERptrew8wySEC99T13FKIvHpjKOe9laLGX-fvyvQB4K93HJNvUQMf0wKeh4P4n61Ab2xxK1tT_sQVh3S7aF0yD2yaK52_Bs3OJSP2XU1qUVfHQQXhBjRWnYx"
URL = "https://api.yelp.com/v3/businesses/search"
BASE_URL = "https://api.yelp.com/v3/businesses/"
SORT_PARAM = "distance"

ratings = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

data = json.load(open("Porto.json"))
df = json_normalize(data["businesses"])


def createNewQuestion(location, difficulty=None):
    a = df.sample(n=1, axis=0)
    rating_a = a['rating'].values[0]
    if difficulty is not None:
        # TODO: don't send with the same rating!
        rand = random.choice([0, 1])
        if difficulty is 'e':
            rating_b = random.sample(set([float(rating_a - 1.5), float(rating_a + 1.5)]), 2)[rand]
            rating_b = 1.0 if rating_b < 1.0 else 5.0 if rating_b > 5.0 else rating_b
            if rating_a == rating_b:
                if rating_b == 5.0:
                    rating_b = rating_b - 1.5
                elif rating_b == 1.0:
                    rating_b = rating_b + 1.5
        elif difficulty is 'm':
            rating_b = random.sample(set([float(rating_a - 1), float(rating_a + 1)]), 2)[rand]
            rating_b = 1.0 if rating_b < 1.0 else 5.0 if rating_b > 5.0 else rating_b
            if rating_a == rating_b:
                if rating_b == 5.0:
                    rating_b = rating_b - 1.0
                elif rating_b == 1.0:
                    rating_b = rating_b + 1.0
        elif difficulty is 'h':
            rating_b = random.sample(set([float(rating_a - 0.5), float(rating_a + 0.5)]), 2)[rand]
            rating_b = 1.0 if rating_b < 1.0 else 5.0 if rating_b > 5.0 else rating_b
            if rating_a == rating_b:
                if rating_b == 5.0:
                    rating_b = rating_b - 0.5
                elif rating_b == 1.0:
                    rating_b = rating_b + 0.5
        question_ratings = [rating_a, rating_b]
        question = {
            "A": json.loads(a.drop(['rating'], axis=1).sample(n=1, axis=0).to_json(orient='records'))[0],
            "B": json.loads(df.loc[df['rating'] == rating_b].drop(['rating'], axis=1).sample(n=1, axis=0).to_json(
                orient='records'))[0],
        }

        if (question_ratings.index(min(question_ratings)) == 0):
            answer = question['A']['name']
            worst_review = getWorstReview(question['A']['id'])
        else:
            answer = question['B']['name']
            worst_review = getWorstReview(question['B']['id'])

    else:

        question_ratings = random.sample(set(ratings), 2)
        question = {
            "A": json.loads(
                df.loc[df['rating'] == question_ratings[0]].drop(['rating'], axis=1).sample(n=1, axis=0).to_json(
                    orient='records'))[0],
            "B": json.loads(
                df.loc[df['rating'] == question_ratings[1]].drop(['rating'], axis=1).sample(n=1, axis=0).to_json(
                    orient='records'))[0],
        }
        if (question_ratings.index(min(question_ratings)) == 0):
            answer = question['A']['name']
            worst_review = getWorstReview(question['A']['id'])
        else:
            answer = question['B']['name']
            worst_review = getWorstReview(question['B']['id'])

    return question, answer, worst_review


def request(url, api_key, location, offset):
    url_params = {
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT,
        'sort_by': SORT_PARAM,
        'offset': offset,
    }
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }
    response = requests.request('GET', url, headers=headers, params=url_params)
    return response.json()


def getReviews(url, api_key, business_id):
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }
    response = requests.request('GET', url + business_id + "/reviews", headers=headers)
    return response.json()


def getWorstReview(business_id):
    reviews = getReviews(BASE_URL, API_KEY, business_id)
    worst_review = None
    worst_rating = 6
    if len(reviews['reviews']) > 0:
        for review in reviews['reviews']:
            if int(review['rating']) < worst_rating:
                worst_rating = int(review['rating'])
                worst_review = review
    return worst_review


def getJson():
    out = {
        'businesses': [],
    }
    response = request(URL, API_KEY, DEFAULT_LOCATION, 0)
    out['businesses'].extend(response['businesses'])
    offset = int(response['total'] / 50) + 1

    for i in range(1, offset):
        response = request(URL, API_KEY, DEFAULT_LOCATION, i * 50)
        out['businesses'].extend(response['businesses'])
    locationDataFile = open('test.json', 'w')
    locationDataFile.write(json.dumps(out, indent=4, sort_keys=True))
    locationDataFile.close()


createNewQuestion(DEFAULT_LOCATION, 'h')
# print(getReviews(BASE_URL, API_KEY, "yMUNfRmBfo_qvl-0p_kAwg"))
