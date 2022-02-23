# Клиентская часть
import json
import sys
import time
import logging
import log.config_client_log

from errors import ReqFieldMissingError
from common.variables import DEF_IP_ADDR, DEF_PORT, ACTION, TIME, ACCOUNT_NAME, USER, PRESENCE, RESPONSE, ERROR
from socket import socket, AF_INET, SOCK_STREAM
from common.utils import get_message, send_message

# Инициализация клиентского логера
CLIENT_LOGGER = logging.getLogger('client')


def create_precense(account_name='Guest'):
    """
    Создаём сообщение приветствие для сервера

    :param account_name:
    :return:
    """
    CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
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
    CLIENT_LOGGER.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            CLIENT_LOGGER.debug('Сообщение корректное {RESPONSE: 200}')
            return '200 : OK'
        CLIENT_LOGGER.error("Сообщение ошибочное {RESPONSE: 400, ERROR: 'Bad Request'}")
        return f'400 : {message[ERROR]}'
    raise ValueError

def command_line_def():
    """
    Обработка командной строки

    :return:
    """
    CLIENT_LOGGER.debug(f'Разбираем коммандную строку : {sys.argv}')
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError

    except IndexError:
        server_address = DEF_IP_ADDR
        server_port = DEF_PORT
        CLIENT_LOGGER.debug(f'адрес и порт не указаны в коммандной строке.'
                            f'Назначены значения по умолчанию {server_address}, порт: {server_port}')
    except ValueError:
        CLIENT_LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
            f' Допустимы адреса с 1024 до 65535. Клиент завершается.')

        print('порт должен быть в диапазоне от 1024 до 56535')
        sys.exit(1)
    CLIENT_LOGGER.info(f'Запущен клиент с парамертами: '
                       f'адрес сервера: {server_address}, порт: {server_port}')
    return server_address, server_port


def main():
    # Инициализация сокета и обмен
    server_address, server_port = command_line_def()

    transport = socket(AF_INET, SOCK_STREAM)
    transport.connect((server_address, server_port))
    message_to_server = create_precense()
    send_message(transport, message_to_server)
    try:
        answer = process_ans(get_message(transport))
        CLIENT_LOGGER.info(f'Принят ответ от сервера {answer}')
        # print(answer)
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                            f'{missing_error.missing_field}')
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                               f'конечный компьютер отверг запрос на подключение.')


if __name__ == '__main__':
    main()
