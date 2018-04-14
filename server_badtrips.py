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
    session['id'] = id
    app.logger.debug('New game created with location: '+ request.form['location'] +' id: ' + str(id))
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
    app.logger.debug("New question from "+ str(session['id']) +"\nGame object: "+ str(game) +"\n"  )
    if game['state'] != "playing":
        return jsonify({"state":"no no no no"})
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
    if game['state'] != "playing":
        return jsonify({"state":"no no no no"})
    response, correct_answer = check_answer(answer, session['id'], game)
    app.logger.debug("New answer from " + str(session['id']) +"\nGame object: " + str(game) + "\nAnswer: " + answer)
    if response:
        return jsonify({"correct": True, "answer": correct_answer})
    else:
        register_gameover(session['id'], game)
        return jsonify({"correct": False, "answer": correct_answer})

def newGame(location, username):
    '''
    create a new game that has a location, username, id, score and state
    :return: session id
    '''
    id = os.urandom(32)
    game = {
        "location": location,
        "score": 0,
        "username": username,
        "state": "playing"
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
    r.set(id, json.dumps(game))

def leaderboard():
    l = r.zrevrange("scores", 0, 10, withscores=True)
    print(l)
    return l

def register_gameover(id, game):
    '''
    Register in the db this user score and set the state to gameover
    :param id:
    :param game:
    :return:
    '''
    game['state'] = 'gameover'
    r.set(id, json.dumps(game))
    score = r.zscore("scores", game["username"])
    if score:
        if score < game['score']:
            r.zadd("scores", game['username'], game['score'])

def check_answer(answer, id, game):
    '''
    Check if the user answer is correct and updates the user score in the db
    :param answer: the user answer
    :param id: this game id
    :param game: this game session
    :return: True if is correct,false if incorrect and
    '''
    if game["answer"] == answer:
        game["score"] += 1
        r.set(id, json.dumps(game))
        return True, game["answer"]
    return False, game["answer"]