from flask import Flask,redirect,render_template,jsonify
from flask import request
from pipeline import ChatBot
app = Flask(__name__)
bot = ChatBot()
@app.route('/response',methods = ['GET','POST'])
def response():
    input_arg = request.get_json()
    message = input_arg['message']
    return jsonify(bot.return_reponse(message))

if __name__ == '__main__':
    app.run(debug = True)