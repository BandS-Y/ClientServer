# Серверная часть
import json
import logging
import select
import sys
from datetime import time

import log.config_server_log

from common.variables import DEF_PORT, MAX_CONNECTIONS, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, \
RESPONDEFAULT_IP_ADDR, ERROR, MESSAGE, MESSAGE_TEXT, SENDER

from common.utils import get_message, send_message
from socket import socket, AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET

from errors import IncorrectDataRecivedError
from decos import log

#Инициализация логирования сервера.
SERVER_LOGGER = logging.getLogger('server')


@log
def process_client_message(message, messages_list, client):
    """
    Принимаем обращение от клиента
    разбираем, формиуем ответ

    :param message:
    :return:
    """
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {client} {message}')
    # Детектируем сообщение о присутствии. Отправляем сообщение об успехе
    if ACTION in message \
        and message[ACTION] == PRESENCE \
        and TIME in message \
        and USER in message \
        and message[USER][ACCOUNT_NAME] == 'Guest':
        SERVER_LOGGER.debug('Сообщение корректное {RESPONSE: 200}')
        send_message(client, {RESPONSE: 200})
        return
    # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
    elif ACTION in message\
        and message[ACTION] == MESSAGE\
        and TIME in message\
        and MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        SERVER_LOGGER.debug(f"Сообщение !{message[MESSAGE_TEXT]}! для {client} добавлено в список сообщений ")
        return
    # Иначе отдаём Bad request
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        SERVER_LOGGER.error("Сообщение ошибочное {RESPONSE: 400, ERROR: 'Bad Request'}")
        return


@log
def port_define():
    """
    Обработка командной строки с параметрами порта и IP адреса.
    Если параметры не заданы, то по умолчанию из файла variables
    server.py -p 7777 -a 127.0.0.1

    :return:
    """

    # Проверяем параметр порта
    SERVER_LOGGER.debug(f'Разбираем коммандную строку : {sys.argv}')
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEF_PORT
        if listen_port < 1024 or listen_port> 65535:
            raise ValueError
        SERVER_LOGGER.info(f'Запущен сервер, порт для подключений: {listen_port}, ')
        return listen_port
    except IndexError:
        SERVER_LOGGER.critical(f"Попытка запуска сервера ключом '-p' Без указания номера порта:"
                                  f"Необходимо указать номер потра из диапазона 1024 - 65535")
        # print('После параметра -р необходимо указать номер порта')
        sys.exit(1)
    except ValueError:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                               f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        # print('порт должен быть в диапазоне от 1024 до 56535')
        sys.exit(1)
        # raise ValueError


@log
def addres_define():
    # Проверяем парамет IP адреса
    try:
        if '-a' in sys.argv:
            listen_addres = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_addres = ''
        SERVER_LOGGER.info(f'Запущен сервер, адрес с которого принимаются подключения: {listen_addres}. '
                           f'Если адрес не указан, принимаются соединения с любых адресов.')
    except IndexError:
        SERVER_LOGGER.critical(f'После параметра -a необходимо указать IP адрес, который будет слушать сервер')
        # print('После параметра -a необходимо указать IP адрес, который будет слушать сервер')
        sys.exit(1)
    return listen_addres


def main():
    listen_port = port_define()
    # print(listen_port)
    listen_addres = addres_define()
    # print(listen_addres)
    # Организуем сокет

    transport = socket(AF_INET, SOCK_STREAM)
    transport.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    transport.bind((listen_addres, listen_port))
    transport.settimeout(1)

    # список клиентов , очередь сообщений
    clients = []
    messages = []

    # Слушаем порт
    transport.listen(MAX_CONNECTIONS)

    SERVER_LOGGER.info(f'Сервер запущен на IP адресе {listen_addres} и {listen_port} порту')

    while True:
        # Ждём подключения, если таймаут вышел, ловим исключение.
        try:
            client, client_addr = transport.accept()
        except OSError as err:
            print(err.errno)  # The error number returns None because it's just a timeout
            pass
        else:
            clients.append(client)
            SERVER_LOGGER.info(f'Подключен клинет с адреса {client_addr[0]} и потра {client_addr[1]}')

        # Список клиентов на получение, отправку и ошибочных
        recv_data_lst = []
        send_data_lst = []
        err_lst = []

        # Проверяем на наличие ждущих клиентов
        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        # принимаем сообщения и если там есть сообщения,
        # кладём в словарь, если ошибка, исключаем клиента.
        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    process_client_message(get_message(client_with_message),
                                           messages, client_with_message)
                except:
                    SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                f'отключился от сервера.')
                    clients.remove(client_with_message)

        # Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщение.
        if messages and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    SERVER_LOGGER.info(f'Пробуем отправить сообщение {message} Клиенту {waiting_client.getpeername()} ')
                    send_message(waiting_client, message)
                except:
                    SERVER_LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    waiting_client.close()
                    clients.remove(waiting_client)

        # try:
        #     message_from_client = get_message(client)
        #     SERVER_LOGGER.debug(f'Получено сообщение {message_from_client}')
        #     response = process_client_message(message_from_client)
        #     SERVER_LOGGER.info(f'Cформирован ответ клиенту {response}')
        #     send_message(client, response)
        #     SERVER_LOGGER.debug(f'Соединение с клиентом {client_addr} закрывается.')
        #     client.close()
        #     SERVER_LOGGER.debug(f'клинет с адреса {client_addr[0]} и потра {client_addr[1]} отключен')
        # except json.JSONDecodeError:
        #     SERVER_LOGGER.error(f'Не удалось декодировать JSON строку, полученную от '
        #                         f'клиента {client_addr}. Соединение закрывается.')
        #     client.close()
        # except IncorrectDataRecivedError:
        #     SERVER_LOGGER.error(f'От клиента {client_addr} приняты некорректные данные. '
        #                         f'Соединение закрывается.')
        #     client.close()


if __name__ == '__main__':
    main()



