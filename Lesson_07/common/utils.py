# Общие функции клиента и сервера

import json
from common.variables import MAX_LEN_MESSAGE, ENCODING
from decos import log
from errors import IncorrectDataRecivedError


@log
def get_message(client):
    """
    Функция получения сообщения

    :param client:
    :return:
    """

    encoded_resp = client.recv(MAX_LEN_MESSAGE)  # Получаем сообщение
    if isinstance(encoded_resp, bytes): # Проверяем байты ли мы получли
        print(f' 1 get_message {encoded_resp}')
        json_resp = encoded_resp.decode(ENCODING) # Декодируем в строку
        print(f' 2 get_message {json_resp}')
        if isinstance(json_resp, str): # Проверяем строку ли мы получили
            response = json.loads(json_resp) # декодируем в словарь
            print(f' 3 get_message {response}')
            if isinstance(response, dict): # Проверяем словарь ли мы получили
                return response # Передаём словарь в ответ
            raise ValueError
        raise ValueError
    raise ValueError


@log
def send_message(sock, message):
    """
    Функция отправки сообщения

    :param sock:
    :param message:
    :return:
    """
    if not isinstance(message, dict):
        raise TypeError
    print(f' 1 send {message}')
    json_message = json.dumps(message)
    print(f' 2 send {json_message}')
    encoded_message = json_message.encode(ENCODING)
    print(f' 3 send {encoded_message}')
    sock.send(encoded_message)
