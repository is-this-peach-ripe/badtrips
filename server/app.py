from flask import Flask, session, request, jsonify
import redis
import yelp_stuff
app = Flask(__name__)
app.secret_key = ''

@app.route('/')
def index():
    '''
    Starting page
    user chooses the location of the game
    :return:
    '''
    pass

@app.route('/play', methods=['POST'])
def play():
    '''
    Must recieve a location in the request
    if we dont have a location generate a random one?

    :return:
    '''
    id = newGame(request.form['location'])
    session['id'] = id

    # return play page and call /newquestion
    pass

@app.route('/newquestion', methos=['POST'])
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
    question, answer = yelp_stuff.createNewQuestion(game['location'])
    question = {
        "A": {"nome": "Café do barbosa", "tipo": "cafe", "img_url":"http://oje-50ea.kxcdn.com/wp-content/uploads/2017/03/cafe-925x578.jpg"},
        "B": {"nome": "Café do Zé", "tipo": "cafe", "img_url":"http://oje-50ea.kxcdn.com/wp-content/uploads/2017/03/cafe-925x578.jpg"}
    }
    answer = "Café do Zé"
    store_answer(answer, game)
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

def newGame(location):
    '''
    create a new game that has a location, username, id and score
    :return: session id
    '''
    pass

def getGame(id):
    '''
    get a game session from redis
    :param id:
    :return:
    '''

def store_answer(answer, game):
    '''
    store a answer for a game
    :param answer:
    :param game:
    :return:
    '''
    pass

def check_answer(answer, game):
    pass