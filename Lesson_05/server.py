# Серверная часть
import json
import logging
import sys
import log.config_server_log

from common.variables import DEF_PORT, MAX_CONNECTIONS, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, \
RESPONDEFAULT_IP_ADDR, ERROR

from common.utils import get_message, send_message
from socket import socket, AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET

from errors import IncorrectDataRecivedError

#Инициализация логирования сервера.
SERVER_LOGGER = logging.getLogger('server')


def process_client_message(message):
    """
    Принимаем обращение от клиента
    разбираем, формиуем ответ

    :param message:
    :return:
    """
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    if ACTION in message \
        and message[ACTION] == PRESENCE \
        and TIME in message \
        and USER in message \
        and message[USER][ACCOUNT_NAME] == 'Guest':
        SERVER_LOGGER.debug('Сообщение корректное {RESPONSE: 200}')
        return {RESPONSE: 200}
    SERVER_LOGGER.error("Сообщение ошибочное {RESPONSE: 400, ERROR: 'Bad Request'}")
    return {RESPONSE: 400, ERROR: 'Bad Request'}

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

    transport.listen(MAX_CONNECTIONS)

    SERVER_LOGGER.info(f'Сервер запущен на IP адресе {listen_addres} и {listen_port} порту')

    while True:
        client, client_addr = transport.accept()
        SERVER_LOGGER.info(f'Подключен клинет с адреса {client_addr[0]} и потра {client_addr[1]}')
        try:
            message_from_client = get_message(client)
            SERVER_LOGGER.debug(f'Получено сообщение {message_from_client}')
            response = process_client_message(message_from_client)
            SERVER_LOGGER.info(f'Cформирован ответ клиенту {response}')
            send_message(client, response)
            SERVER_LOGGER.debug(f'Соединение с клиентом {client_addr} закрывается.')
            client.close()
            SERVER_LOGGER.debug(f'клинет с адреса {client_addr[0]} и потра {client_addr[1]} отключен')
        except json.JSONDecodeError:
            SERVER_LOGGER.error(f'Не удалось декодировать JSON строку, полученную от '
                                f'клиента {client_addr}. Соединение закрывается.')
            client.close()
        except IncorrectDataRecivedError:
            SERVER_LOGGER.error(f'От клиента {client_addr} приняты некорректные данные. '
                                f'Соединение закрывается.')
            client.close()


if __name__ == '__main__':
    main()



