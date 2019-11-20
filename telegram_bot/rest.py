from flask import Flask, jsonify
from telegram_bot.google_parse import mistakes_correction
app = Flask(__name__)

#Метод GET позволяет ответить на первый вопрос, POST на вопрос с ушами
@app.route('/', methods=['GET'])
def index():
    return '''<h> Привет, я помогу отличить кота от хлеба! Для этого перейди по этой ссылке <a href="http://127.0.0.1:5000/api/telegram_bot/<nick>/<mes>">http://127.0.0.1:5000/api/telegram_bot/nick/message</a> 
    Объект перед тобой квадратный? Впиши ответ в ссылке, вместо "nick" напиши свое имя, вместо "message" впиши ответ.</h>'''

@app.route('/api/telegram_bot/<nick>/<mes>', methods=['GET'])
def response_get(mes, nick):
    mis = ' '.join(mistakes_correction(mes))
    if mes == 'ага' or mes == 'да' or mes == 'пожалуй':
        return jsonify({'nickname':nick,
                        'response':'Это хлеб!'})
    elif mes == 'нет' or mes == 'ноуп' or mes == 'найн':
        return jsonify({'nickname':nick,
                        'response':'У него есть уши? Чтобы ответить, сделай POST запрос с твоим ответом, вместо "message"'})
    else: return jsonify({'nickname':nick,
                        'response':"Возможно, ты и имел в виду '"+mis+"', но я тебя не понял, я лишь отличаю кота от хлеба"})

@app.route('/api/telegram_bot/<nick>/<mes>', methods=['POST'])
def response_post(mes, nick):
    mis = ' '.join(mistakes_correction(mes))
    if mes == 'ага' or mes == 'да' or mes == 'пожалуй':
        return jsonify({'nickname':nick,
                        'response':'Это кот!'})
    elif mes == 'нет' or mes == 'ноуп' or mes == 'найн':
        return jsonify({'nickname':nick,
                        'response':'Это хлеб!!'})
    else: return jsonify({'nickname':nick,
                        'response':"Возможно, ты и имел в виду '"+mis+"', но я тебя не понял, я лишь отличаю кота от хлеба"})

if __name__=='__main__':
    app.run(debug=True)

