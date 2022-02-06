# 1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание
# соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode
# и также проверить тип и содержимое переменных.

words_1 = ['разработка', 'сокет', 'декоратор']
words_2 = ['\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
           '\u0441\u043e\u043a\u0435\u0442', '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440']

def test_word(words):
    for word in words:
        print('содержание = ', word, 'тип = ', type(word))

print('\n--------------- Задача 1 ---------------\n')

test_word(words_1)
test_word(words_2)

# 2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность
# кодов (не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.

words = ['class', 'function', 'method']

def covert_to_byte(words):
    for word in words:
        print('input = ', word, ' type = ', type(word), 'len = ', len(word))
        word = eval ("b'" + word)
        print('input = ', word, ' type = ', type(word), 'len = ', len(word))

print ('\n--------------- Задача 2 ---------------\n')

# print(' word_a = ', word_a,' \n', 'word_b = ', word_b, '\n', 'word_c = ',  word_c)
# print(' type of word_a = ', type(word_a), '\n', 'len of word_a = ', len(word_a), '\n',
#       'type of word_b = ', type(word_b), '\n', 'len of word_b = ', len(word_b), '\n',
#       # 'type of word_d = ', type(word_d), '\n', 'len of word_d = ', len(word_d), '\n', # Пробуем перевести в байтовый тип
#       'type of word_c = ', type(word_c), '\n', 'len of word_c = ', len(word_c))

covert_to_byte(words)

# 3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе. Важно:
# решение должно быть универсальным, т.е. не зависеть от того, какие конкретно слова мы исследуем.

words = ['attribute', 'класс',  'функция', 'type']
word_in_byte = ''
print ('\n--------------- Задача 3 ---------------\n')
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


# 4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в
# байтовое и выполнить обратное преобразование (используя методы encode и decode).

words = ['разработка', 'администрирование', 'protocol', 'standard']
print ('\n--------------- Задача 4 ---------------\n')
for word in words:
    print('\n--------------- ', word, ' ---------------\n')
    print(word, type(word))
    word = word.encode()
    print(word, type(word))
    word = word.decode()
    print(word, type(word))

# 5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый
# тип на кириллице.

