import os
import unittest
from pprint import pprint
import sys

sys.path.append(os.path.join(os.getcwd(),'..'))
# pprint(sys.path)

from common.variables import *
from server import process_client_message, port_define, addres_define
from unittest.mock import patch

class TestServer(unittest.TestCase):
    """
    Тестирование Сервера
    """

    ok_dict = {RESPONSE: 200}
    err_dict = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    def test_ok_check(self):
        # Тестируем правильный ответ
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}), self.ok_dict)

    def test_no_action(self):
        # Отсутствует поле действия
        self.assertEqual(process_client_message(
            {TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_wrong_action(self):
        # Неизвестное действие
        self.assertEqual(process_client_message(
            {ACTION: 'Hello World!', TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_no_time(self):
        # Тестируем отсутствие поля времени
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE,  USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_no_user(self):
        # Тестируем отсутствие поля пользователя
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 1.1}), self.err_dict)

    def test_ok_check(self):
        # Тестируем не правильное имя пользователя
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Admin'}}), self.err_dict)

    def test_command_line_right_port(self):
        #
        with patch.object(sys, 'argv', ['server.py', '-p', '8888']):
            self.assertEqual(port_define(),8888)

    # Тесть с портом за пределами диапазона пока реализовать не смог.
    # Попробоую после разбора ДЗ
    # def test_command_line_wrong_port(self):
    #     # Тест с портом за пределами диапазона
    #     with patch.object(sys, 'argv', ['server.py', '-p', '1000']):
    #         self.assertRaises(ValueError, port_define())

    def test_command_line_right_addres(self):
        # Тест с правильным ИП адресом
        with patch.object(sys, 'argv', ['server.py', '-a', '127.0.0.1']):
            self.assertEqual(addres_define(),'127.0.0.1')

    def test_command_line_right_emty_port(self):
        # Тест с правильным портом
        with patch.object(sys, 'argv', ['server.py']):
            self.assertEqual(port_define(), 7777)

    def test_command_line_right_empty_addres(self):
        # Тест с пустой командной строкой
        with patch.object(sys, 'argv', ['server.py']):
            self.assertEqual(addres_define(),'')



if __name__ == '__main__':
    unittest.main()