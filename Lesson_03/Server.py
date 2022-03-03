# Серверная часть
import json
import sys

from common.variables import DEF_PORT, MAX_CONNECTIONS, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, \
RESPONDEFAULT_IP_ADDR, ERROR

from common.utils import get_message, send_message
from socket import socket, AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET

def process_client_message(message):
    """
    Принимаем обращение от клиента
    разбираем, формиуем ответ

    :param message:
    :return:
    """

    if ACTION in message \
        and message[ACTION] == PRESENCE \
        and TIME in message \
        and USER in message \
        and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {RESPONDEFAULT_IP_ADDR: 400, ERROR: 'Bad Request'}



def main():
    """
    Обработка командной строки с параметрами порта и IP адреса.
    Если параметры не заданы, то по умолчанию из файла variables
    server.py -p 7777 -a 127.0.0.1

    :return:
    """

    # Проверяем параметр порта
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEF_PORT
        if listen_port < 1024 or listen_port> 65535:
            raise ValueError
    except IndexError:
        print('После параметра -р необходимо указать номер порта')
        sys.exit(1)
    except ValueError:
        print('порт должен быть в диапазоне от 1024 до 56535')
        sys.exit(1)


    # Проверяем парамет IP адреса
    try:
        if '-a' in sys.argv:
            listen_addres = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_addres = ''
    except IndexError:
        print('После параметра -a необходимо указать IP адрес, который будет слушать сервер')
        sys.exit(1)
    print(listen_port)
    print(listen_addres)
    # Организуем сокет

    transport = socket(AF_INET, SOCK_STREAM)
    transport.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    transport.bind((listen_addres, listen_port))

    transport.listen(MAX_CONNECTIONS)

    print(f'Сервер запущен на IP адресе {listen_addres} и {listen_port} порту')

    while True:
        client, client_addr = transport.accept()
        print(f'Подключен клинет с адреса {client_addr[0]} и потра {client_addr[1]}')
        try:
            message_from_client = get_message(client)
            print(message_from_client)
            response = process_client_message(message_from_client)
            send_message(client, response)
            client.close()
            print(f'клинет с адреса {client_addr[0]} и потра {client_addr[1]} отключен')
        except (ValueError, json.JSONDecodeError):
            print('Принято некорректное сообщение от клиента')
            client.close()

if __name__ == '__main__':
    main()



