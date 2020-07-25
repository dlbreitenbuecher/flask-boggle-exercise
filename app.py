from flask import Flask, render_template, session, request, jsonify
from uuid import uuid4

from boggle import BoggleWordList, BoggleBoard

# Sets the key name as a global variable so we avoid typos
SESS_BOARD_UUID_KEY = "board_uuid"

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

word_list = BoggleWordList()

# The boggle boards created, keyed by board uuid
boards = {}

'''
boards = {
    123412341: [[a,b,c], [a,b,c]]
}

'''


@app.route("/")
def homepage():
    """Show board."""

    # get a unique identifier for the board we're creating
    uuid = uuid4()

    # an instance of the class BoggleBoard - We pass this into the render_template
    board = BoggleBoard()
    # the unique uuid serves as the key in the global dictionary boards, while our instance of the BoggleBoard class serves as the value
    boards[uuid] = board

    # store the uuid for the board in the session so that later requests can
    # find it
    session[SESS_BOARD_UUID_KEY] = uuid

    return render_template(
        "index.html",
        board=board)

@app.route('/api/score-word', methods=['POST'])
def json_route():
    '''Return the JSON detailing if the word is legal or not. If it is legal, returns the result and the word'''
    
    word = request.form['entry']
    #print(word)
    current_board = boards[session[SESS_BOARD_UUID_KEY]]
    
    word_exists = word_list.check_word(word)
    
    word_on_board = current_board.check_word_on_board(word)

    if not word_exists:
        return jsonify(result='not-word')
    elif not word_on_board:
        return jsonify(result='not-on-board')
    else:
        return jsonify(result='ok', word=f"{word}")
