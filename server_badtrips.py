from flask import Flask, session, request, jsonify, send_from_directory
import os
import json
import redis
import yelp_stuff

r = redis.Redis(host='localhost', port=6379, password='')
app = Flask("badtrips", static_url_path='')
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RZ'
static_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory(static_dir, path)

@app.route('/')
def index():
    '''
    Starting page
    user chooses the location of the game
    :return:
    '''
    return send_from_directory(static_dir, 'index.html')

@app.route('/play', methods=['POST'])
def play():
    '''
    Must recieve a location in the request
    if we dont have a location generate a random one?

    :return:
    '''
    id = newGame(request.form['location'], request.form['username'])
    print(id)
    session['id'] = id
    return send_from_directory(static_dir, 'play.html')

@app.route('/newquestion', methods=['POST'])
def newQuestion():
    '''
    Create a new question from yelp
    returns a json with:
     id: this question id, to check the correct responce
     A:
     B:
    :return:
    '''
    game = getGame(session['id'])
    print(session['id'])
    print(game)
    question, answer = yelp_stuff.createNewQuestion(game['location'])
    store_answer(answer, session['id'], game)
    return jsonify(question)

@app.route('/answer', methods=['POST'])
def answer():
    '''
    will recieve answer:<nome>
    :return:
    '''
    answer = request.form['answer']
    game = getGame(session['id'])

    responce = check_answer(answer, game)
    #devolve resposta correcta
    pass

def newGame(location, username):
    '''
    create a new game that has a location, username, id and score
    :return: session id
    '''
    id = os.urandom(32)
    game = {
        "location": location,
        "score": 0,
        "username": username
    }
    r.set(id, json.dumps(game))
    return id

def getGame(id):
    '''
    get a game session from redis
    :param id:
    :return:
    '''
    game = r.get(id)
    print("game from redis")
    print(game)
    return json.loads(game)

def store_answer(answer, id, game):
    '''
    store a answer for a game
    :param answer:
    :param game:
    :param id:
    :return:
    '''
    game["answer"] = answer
    r.set(id, game)

def check_answer(answer, game):
    return game["answer"] == answer
