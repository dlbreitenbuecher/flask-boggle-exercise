from unittest import TestCase
from flask import session, jsonify

from app import app, boards
from app import SESS_BOARD_UUID_KEY


# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True
# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            # Tests to ensure the session key is present
            self.assertIn(SESS_BOARD_UUID_KEY, session)

            # Tests to ensure the expected html elements (form and table) are present
            self.assertIn('<form action="/api/score-word" method="POST">', html)

    def test_word_submission(self):
        """Test if we receive the correct JSON response for a word submitted in a post request"""
        # TODO - Ask why we use self.client instead of app.client (as the notes indicate)
        with self.client as client:
            
            # print('board key:', boards)
            #make request to root route, 
            client.get("/")
            
            # print("client get", test)
            uuid_key = session[SESS_BOARD_UUID_KEY]
            current_board = boards[uuid_key]
            current_board[0] = ['C','A','T','S','A']

            response = client.post('/api/score-word', data={'entry': 'CAT'})
            api_response = response.get_data(as_text=True)

            print("type of api_res,", api_response)

            api_expected = {"result": "ok", "word": "CAT"}
            # self.assertIn(word, current_board)
            self.assertIsNot(api_response, '{\n  "result": "ok", \n  "word": "CAT"\n}')