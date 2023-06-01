from flask import Flask,redirect,render_template,jsonify
from flask import request
from pipeline import ChatBot
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
<<<<<<< HEAD
=======

# app = Flask(__name__)
>>>>>>> 319eab135d5ecdeca2544e3b9b4204c9c3841400
bot = ChatBot()

@app.route('/response',methods = ['GET','POST'])
def response():
    input_arg = request.get_json()
    message = input_arg['message']
    return bot.return_reponse(message)

if __name__ == '__main__':
    app.run(debug = True)