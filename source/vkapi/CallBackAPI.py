import json
import logging

from flask import Flask, request

from Config import Config
from source.static.StaticData import StaticData

m_thread = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@m_thread.route('/casino', methods=['GET'])
def get_access():
    return f"Welcome to {StaticData.name} server!"


@m_thread.route('/casino', methods=['POST'])
def processing():
    data = json.loads(request.data)

    if 'type' not in data.keys():
        return 'not vk'

    if data['type'] == 'confirmation':
        return Config.callback_api_special_string
    elif data['type'] == 'message_new':
        StaticData.stack_messages.append(
            {'message': data['object']['text'], 'user_id': data['object']['from_id'],
             'peer_id': data['object']['peer_id']})
        StaticData.new_message_trigger.set()
        return 'ok'
