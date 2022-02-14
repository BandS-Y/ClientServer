# Клиентская часть
import json
import sys
import time

from common.variables import DEF_IP_ADDR, DEF_PORT, ACTION, TIME, ACCOUNT_NAME, USER, PRESENCE, RESPONSE, ERROR
from socket import socket, AF_INET, SOCK_STREAM
from common.utils import get_message, send_message


def create_precense(account_name='Guest'):
    """
    Создаём сообщение приветствие для сервера

    :param account_name:
    :return:
    """

    return {
        ACTION : PRESENCE,
        TIME: time.time(),
        USER: {ACCOUNT_NAME: account_name}
    }


def process_ans(message):
    """
    Разбираем ответ сервера

    :param message:
    :return:
    """

    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200: OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


def main():
    """
    Обработка командной строки

    :return:
    """

    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = DEF_IP_ADDR
        server_port = DEF_PORT
    except ValueError:
        print('порт должен быть в диапазоне от 1024 до 56535')
        sys.exit(1)

    transport = socket(AF_INET, SOCK_STREAM)
    transport.connect((server_address, server_port))
    message_to_server = create_precense()
    send_message(transport, message_to_server)
    try:
        answer = process_ans(get_message(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера')
        
        
if __name__ == '__main__':
    main()
