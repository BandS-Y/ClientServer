import os
from pprint import pprint
import sys
from unittest.mock import patch

sys.path.append(os.path.join(os.getcwd(),'..'))
# pprint(sys.path)

from client import create_precense, process_ans, command_line_def

from common.variables import *
import unittest

class TestClass(unittest.TestCase):
    """
    Тестирование клиента
    """


    def test_def_presense(self):
        # тест коректного запроса
        test = create_precense('Guest')
        test[TIME] = 1.1  # время необходимо приравнять принудительно иначе тест никогда не будет пройден
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_def_presense_wrong_name(self):
        # Тест не коррктного имени
        test = create_precense('Guest')
        test[TIME] = 1.1  # время необходимо приравнять принудительно иначе тест никогда не будет пройден
        self.assertNotEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Admin'}})


    def test_200_ans(self):
        # тест корректтного разбора ответа 200
        self.assertEqual(process_ans({RESPONSE: 200}), '200 : OK')


    def test_400_ans(self):
        # тест корректного разбора 400
        self.assertEqual(process_ans({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')


    def test_no_response(self):
        # тест исключения без поля RESPONSE
        self.assertRaises(ValueError, process_ans, {ERROR: 'Bad Request'})

    def test_command_line_right_addres(self):
        # Тест корректного порта
        with patch.object(sys, 'argv', ['client_listen.py', '127.0.0.1', '7788']):
            self.assertEqual(command_line_def(),('127.0.0.1', 7788))

    def test_command_line_empty(self):
        # Тест корректной пустой строки
        with patch.object(sys, 'argv', ['client_listen.py']):
            self.assertEqual(command_line_def(),('127.0.0.1', 7777))

    # ест с ошибкой пока сделать не смог. Попробую после разбора ДЗ
    # def test_command_line_wrong_port(self):
    #     with patch.object(sys, 'argv', ['client_listen.py', '127.0.0.1', '1000']):
    #         self.assertRaises(SystemExit, command_line_def(),('127.0.0.1', 7777))

if __name__ == '__main__':
    unittest.main()
