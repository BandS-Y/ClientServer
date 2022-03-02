# Общие функции клиента и сервера

import json
from common.variables import MAX_LEN_MESSAGE, ENCODING
from decos import log


@log
def get_message(client):
    """
    Функция получения сообщения

    :param client:
    :return:
    """

    encoded_resp = client.recv(MAX_LEN_MESSAGE)  # Получаем сообщение
    if isinstance(encoded_resp, bytes): # Проверяем байты ли мы получли
        json_resp = encoded_resp.decode(ENCODING) # Декодируем в строку
        if isinstance(json_resp, str): # Проверяем строку ли мы получили
            response = json.loads(json_resp) # декодируем в словарь
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
    json_message = json.dumps(message)
    encoded_message = json_message.encode(ENCODING)
    sock.send(encoded_message)
