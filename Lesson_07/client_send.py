# Клиентская часть
import argparse
import json
import sys
import time
import logging
import log.config_client_log

from errors import ReqFieldMissingError, ServerError
from common.variables import DEF_IP_ADDR, DEF_PORT, ACTION, TIME, ACCOUNT_NAME, USER, PRESENCE, RESPONSE, ERROR,\
MESSAGE, MESSAGE_TEXT, SENDER
from socket import socket, AF_INET, SOCK_STREAM
from common.utils import get_message, send_message
from decos import log

# Инициализация клиентского логера
CLIENT_LOGGER = logging.getLogger('client')

@log
def message_from_server(message):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
    CLIENT_LOGGER.error(f'Запускаем обработку сообщение с сервера: {message}')
    if ACTION in message \
        and message[ACTION] == MESSAGE and \
        SENDER in message \
        and MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя '
              f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        CLIENT_LOGGER.info(f'Получено сообщение от пользователя '
                    f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')



@log
def create_message(sock, account_name='Guest'):
    """Функция запрашивает текст сообщения и возвращает его.
    Так же завершает работу при вводе подобной комманды
    """
    message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    if message == '!!!':
        sock.close()
        CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


@log
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


@log
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
        elif message[RESPONSE] == 400:
            raise ServerError(f'400 : {message[ERROR]}')
        CLIENT_LOGGER.error("Сообщение ошибочное {RESPONSE: 400, ERROR: 'Bad Request'}")
        return f'400 : {message[ERROR]}'
    raise ReqFieldMissingError(RESPONSE)


@log
def command_line_def():
    """
    Обработка командной строки

    :return:
    """
    CLIENT_LOGGER.debug(f'Разбираем коммандную строку : {sys.argv}')

    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEF_IP_ADDR, nargs='?')
    parser.add_argument('port', default=DEF_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='send', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    # except IndexError:
    #     server_address = DEF_IP_ADDR
    #     server_port = DEF_PORT
    #     CLIENT_LOGGER.debug(f'адрес и порт не указаны в коммандной строке.'
    #                         f'Назначены значения по умолчанию {server_address}, порт: {server_port}')
    # except ValueError:
    #     CLIENT_LOGGER.critical(
    #         f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
    #         f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
    #
    #     print('порт должен быть в диапазоне от 1024 до 56535')
    #     sys.exit(1)

    CLIENT_LOGGER.info(f'Запущен клиент с парамертами: '
                       f'адрес сервера: {server_address}, порт: {server_port}')

    # Проверим допустим ли выбранный режим работы клиента
    if client_mode not in ('listen', 'send'):
        CLIENT_LOGGER.critical(f'Указан недопустимый режим работы {client_mode}, '
                        f'допустимые режимы: listen , send')
        sys.exit(1)

    return server_address, server_port, client_mode


def main():
    # Инициализация сокета и обмен
    server_address, server_port, client_mode = command_line_def()

    transport = socket(AF_INET, SOCK_STREAM)
    transport.connect((server_address, server_port))

    CLIENT_LOGGER.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_address}, '
        f'порт: {server_port}, режим работы: {client_mode}')

    message_to_server = create_precense()
    send_message(transport, message_to_server)

    try:
        answer = process_ans(get_message(transport))
        CLIENT_LOGGER.info(f'Принят ответ от сервера {answer}')
        # print(answer)
        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                            f'{missing_error.missing_field}')
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                               f'конечный компьютер отверг запрос на подключение.')
    except ServerError as error:
        CLIENT_LOGGER.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    else:
        # Если соединение с сервером установлено корректно,
        # начинаем обмен с ним, согласно требуемому режиму.
        # основной цикл прогрммы:
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')
        while True:
            # режим работы - отправка сообщений
            if client_mode == 'send':
                try:
                    CLIENT_LOGGER.info(f' сообщение отправляем {transport}')
                    send_message(transport, create_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)

            # Режим работы приём:
            if client_mode == 'listen':
                try:
                    message_from_server(get_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)


if __name__ == '__main__':
    main()
