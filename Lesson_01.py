
print('\n--------------- Задача 1 ---------------\n')

# 1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание
# соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode
# и также проверить тип и содержимое переменных.

words_1 = ['разработка', 'сокет', 'декоратор']
words_2 = [b'\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
           b'\u0441\u043e\u043a\u0435\u0442', b'\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440']

def test_word(words):
    for word in words:
        print('содержание = ', word, 'тип = ', type(word))


test_word(words_1)
test_word(words_2)


print ('\n--------------- Задача 2 ---------------\n')

# 2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность
# кодов (не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.

words = ['class', 'function', 'method']

def covert_to_byte(words):
    for word in words:
        print('input = ', word, ' type = ', type(word), 'len = ', len(word))
        word = eval ("b'" + word + "'")
        print('after convert  = ', word, ' type = ', type(word), 'len = ', len(word), '\n')

covert_to_byte(words)


print ('\n--------------- Задача 3 ---------------\n')

# 3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе. Важно:
# решение должно быть универсальным, т.е. не зависеть от того, какие конкретно слова мы исследуем.

words = ['attribute', 'класс',  'функция', 'type']
word_in_byte = ''

def byte_convert_1(word):
    try:
        word_in_byte = word.encode('ascii')
        print(word, word_in_byte)

    except UnicodeEncodeError:
        print('ошибка декодирования')

def byte_convert_2(word):
    try:
        word_in_byte = word.encode('ascii')
        print()
        print(word, word_in_byte)
    except UnicodeEncodeError:
        print()
        word_in_byte = word.encode('ascii',  errors='ignore')
        print(word, word_in_byte)
        word_in_byte = word.encode('ascii',  errors='replace')
        print(word, word_in_byte)
        word_in_byte = word.encode('ascii',  errors='xmlcharrefreplace')
        print(word, word_in_byte)
        word_in_byte = word.encode('ascii',  errors='backslashreplace')
        print(word, word_in_byte)
        word_in_byte = word.encode('ascii',  errors='namereplace')
        print(word, word_in_byte)

print ('\n--------------- Решение 1 ---------------\n')
for word in words:
    byte_convert_1(word)

print ('\n--------------- Решение 2 ---------------\n')
for word in words:
    byte_convert_2(word)


print ('\n--------------- Задача 4 ---------------\n')
# 4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в
# байтовое и выполнить обратное преобразование (используя методы encode и decode).

words = ['разработка', 'администрирование', 'protocol', 'standard']

for word in words:
    print('\n--------------- ', word, ' ---------------\n')
    print(word, type(word))
    word = word.encode('utf-8')
    print(word, type(word))
    word = word.decode('utf-8')
    print(word, type(word))



# 5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый
# тип на кириллице.

print ('\n--------------- Задача 5 ---------------\n')

import chardet
import subprocess
import platform

sites = ['yandex.ru', 'youtube.com']

def my_ping(site):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    args = ['ping', param, '2', site]
    result = subprocess.Popen(args, stdout=subprocess.PIPE)

    for line in result.stdout:
        result = chardet.detect(line)
        # у меня, как ни странно стоит Windows  и по умолчанию СР1251, но результаты пинга выдавались
        # {'encoding': 'IBM866', 'confidence': 0.99, 'language': 'Russian'}
        # поэтому решение с кодировкой по умолчанию не прошло
        # print(result)
        line = line.decode(result['encoding']).encode('utf-8')
        print(line.decode('utf-8'))

for site in sites:
    my_ping(site)



print ('\n--------------- Задача 6 ---------------\n')

# 6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет»,
# «декоратор». Далее забыть о том, что мы сами только что создали этот файл и исходить из того, что перед нами файл
# в неизвестной кодировке. Задача: открыть этот файл БЕЗ ОШИБОК вне зависимости от того, в какой кодировке он был создан.

words = ['сетевое программирование', 'сокет', 'декоратор']
file_name = 'test.txt'

def file_write(file_name, words):
    with open(file_name, 'w') as f:
        for word in words:
            f.write(word + '\n')


def file_read(file_name):
    with open(file_name, 'rb') as f:
        content = f.read()
    encoding = chardet.detect(content)['encoding']

    with open(file_name, encoding=encoding) as f:
        for line in f:
            print(line, end='')
        print()

file_write(file_name, words)
file_read(file_name)