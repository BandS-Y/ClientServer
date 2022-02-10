# 1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из
# файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV.
# Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание
# данных. В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
# «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить в
# соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list,
# os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data — и
# поместить в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта»,
# «Тип системы». Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для
# каждого файла);
# Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение данных
# через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
# Проверить работу программы через вызов функции write_to_csv().
import json

import chardet
import re
import csv
import yaml

file_names = ['info_1.txt', 'info_2.txt', 'info_3.txt']
out_file = 'main_data.csv'


# МОЙ КОМЕНТАРИЙ
# если честно, то задание немного путанное, что и куда помещать до конца не ясно, поэтому буду делать, как придумал

def file_read(file_names):
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]

    for file_name in file_names:  # определяем кодировку файла
        with open(file_name, 'rb') as f:
            content = f.read()
        encoding = chardet.detect(content)['encoding']

        with open(file_name, encoding=encoding) as f:  # перебираем файлы, в каждом из которых ищем нужные записи.
            for line in f:
                key_res = re.match(r'Изготовитель системы', line)  # хотел оформить в отдельную функцию, но слишком
                if key_res:  # много передавать параметров получается
                    res = re.findall(r':\s*(\w+.*)', line)  # ищем значение параметра
                    os_prod_list.append(res[0])  # добавляем значение параметра в список
                key_res = re.match(r'Название ОС:', line)
                if key_res:
                    res = re.findall(r':\s*(\w+.*)', line)
                    os_name_list.append(res[0])
                key_res = re.match(r'Код продукта:', line)
                if key_res:
                    res = re.findall(r':\s*(\w+.*)', line)
                    os_code_list.append(res[0])
                key_res = re.match(r'Тип системы:', line)
                if key_res:
                    res = re.findall(r':\s*(\w+.*)', line)
                    os_type_list.append(res[0])

    len_of_data = range(len(os_prod_list))
    [main_data.append([]) for i in len_of_data]  # формируем список списков
    for i in len_of_data:  # распределяем данные по столбцам
        main_data[i + 1].append(os_prod_list[i])
        main_data[i + 1].append(os_name_list[i])
        main_data[i + 1].append(os_code_list[i])
        main_data[i + 1].append(os_type_list[i])
    return main_data  # отдаём готовые данные


def write_to_csv(file_name):
    with open(file_name, 'w', encoding='utf-8') as f_n:
        writer = csv.writer(f_n)
        writer.writerows(file_read(file_names))


# write_to_csv(out_file)


# 2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. Написать
# скрипт, автоматизирующий его заполнение данными. Для этого:
# Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity),
# цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в файл
# orders.json. При записи данных указать величину отступа в 4 пробельных символа;
# Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.

orders_empty = {'orders': []}  # создадим словарь, чтоб обнулить файл

# перезапишем файл пустыми данными, чтоб он не переполнялся
with open('orders.json', 'w', encoding='utf-8') as f_n:
    json.dump(orders_empty, f_n, sort_keys=True, indent=4, ensure_ascii=False)


def write_order_to_json(item, quantity, price, buyer, date):
    # открывваем и читаем данные из файла
    with open('orders.json', encoding='utf-8') as f_n:
        orders = json.load(f_n)

    # добавляем новые данные
    orders['orders'].append({'item': item, 'quantity': quantity, 'price': price, 'buyer': buyer, 'date': date})

    # записываем новые данные
    with open('orders.json', 'w', encoding='utf-8') as f_n:
        json.dump(orders, f_n, sort_keys=True, indent=4, ensure_ascii=False)


# последовательно заполняем файл данными
write_order_to_json('pen', 10, 3.50, 'Petrov P.P.', '20.12.2020')
write_order_to_json('pencil', 15, 4.50, 'Smirnov P.P.', '10.12.2020')
write_order_to_json('unpen', 1, 599.99, 'Gaurgoff P.P.', '11.12.2021')
write_order_to_json('penal', 100, 50.99, 'Trov P.P.', '01.12.2021')
write_order_to_json('pencle', 12, 15.50, 'Petrov P.P.', '29.11.2020')


# 3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле
# YAML-формата. Для этого:
# Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число,
# третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом, отсутствующим в
# кодировке ASCII (например, €);
# Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию
# файла с помощью параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;
# Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.

first_key = ['first', 'second', 'third']
second_key = 123
third_key = {'1212€': {'first': 23, 'second': 25, 'third': 28}, '323¥' : {'first': 13, 'second': 15, 'third': 18}}
all_data = {'first_key': first_key, 'second_key': second_key, 'third_key': third_key}

with open('file.yaml', 'w', encoding='utf-8') as f_n:
    yaml.dump(all_data, f_n, default_flow_style=False, allow_unicode=True)

with open('file.yaml', 'r', encoding='utf-8') as f_n:
    F_N_CONTENT = yaml.load(f_n, Loader=yaml.FullLoader)

print(F_N_CONTENT)
print(all_data==F_N_CONTENT)
