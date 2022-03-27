from flask import Flask, request
import logging
import json

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}
list_of_animals = ['Слона', 'Кролика']
i = 0


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')

    return json.dumps(response)


def handle_dialog(req, res):
    global i
    user_id = req['session']['user_id']

    if req['session']['new']:

        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                'Делать мне нечего!',
                "Отстань!",
            ]
        }

        res['response']['text'] = f'Привет! Купи {list_of_animals[i].lower()}!'

        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо',
        'я покупаю',
        'я куплю'
    ]:

        res['response']['text'] = f'{list_of_animals[i]} можно найти на Яндекс.Маркете!'
        if i == 0:
            i += 1
            res['response']['text'] = f'Привет! Купи {list_of_animals[i].lower()}!'
            sessionStorage[user_id] = {
                'suggests': [
                    "Не хочу.",
                    "Не буду.",
                    'Делать мне нечего!',
                    "Отстань!",
                ]
            }
            res['response']['buttons'] = get_suggests(user_id)
        else:
            res['response']['end_session'] = True
        return

    res['response']['text'] = \
        f"Все говорят '{req['request']['original_utterance']}', а ты купи {list_of_animals[i].lower()}!"
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": f"https://market.yandex.ru/search?text={list_of_animals[i][:-1]}",
            "hide": True
        })
        suggests.append({
            "title": "Я покупаю",
            "url": f"https://market.yandex.ru/search?text={list_of_animals[i][:-1]}",
            "hide": True
        })

    return suggests


if __name__ == '__main__':
    app.run()