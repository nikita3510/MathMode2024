import time
from datetime import datetime
from flask import Flask, request, abort
from pydantic import BaseModel

app = Flask(__name__)

db = [
    {
        'time': time.time(),
        'name': 'Jack',
        'text': 'Привет всем!',
    },
    {
        'time': time.time(),
        'name': 'Mary',
        'text': 'Привет, Jack',
     }
]


class Message(BaseModel):
    name: str
    text: str


@app.route("/")
def hello():
    return "Hello, World 123!"


@app.route("/status")
def status():
    dt_now = datetime.now()
    num_users = len(set(message["name"] for message in db))
    num_messages = len(db)
    status_data = {
        'status': True,
        'name': 'Messenger',
        'time': dt_now.strftime('%d/%m/%Y %H:%M:%S'),
        'total_users': num_users,
        'total_messages': num_messages
    }
    return status_data

@app.route("/send", methods=['POST'])
def send_message():
    data = request.json

    try:
        message = Message (**data)
    except Exception as e:
        return abort(400,str(e))

    message_dict = message.dict()
    message_dict['time'] = time.time()

    db.append(message_dict)

    return {'ok': True}


@app.route("/messages")
def get_messages():
    """messages from db after given timestamp"""
    try:
        after = float(request.args['after'])
    except:
        return abort(400)

    result = []
    for message in db:
        if message['time'] > after:
            result.append(message)
            if len(result) >= 100:
                break

    return {'message': result}


@app.route("/commands", methods=['POST'])
def handle_command(command):
    if command == "\\help":
        return "Для отправки сообщения используйте метод '/send' с параметрами 'name' и 'text'. " \
               "Для получения информации о пользователе используйте GET запрос на /status. " \
               "Для получения списка сообщений после определенного времени используйте GET запрос на /messages с параметром 'after'."
    else:
        return "Неизвестная команда. Используйте '\\help' для просмотра списка команд."


app.run()