from flask import Flask,redirect,render_template,jsonify
from flask import request
from pipeline import ChatBot
from flask_cors import CORS

app = Flask(__name__)
# CORS(app)

# app = Flask(__name__)
bot = ChatBot()

@app.route('/response',methods = ['POST'])
def response():
    input_arg = request.get_json()
    message = input_arg['message']
    return bot.return_reponse(message)

if __name__ == '__main__':
    app.run(debug = True)