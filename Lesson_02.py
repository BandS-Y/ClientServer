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

import chardet
import re
import csv

file_names = ['info_1.txt', 'info_2.txt', 'info_3.txt']
out_file = 'main_data.csv'


# МОЙ КОМЕНТАРИЙ
# если честно, то задание немного путанное, что и куда помещать до конца не ясно, поэтому буду делать, как придумал

# def find_line(base_param, line):
#     key_res = re.match(r'base_param, line)
#     if key_res:
#         res = re.findall(r':\s*(\w+.*)', line)
#         return res[0]

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
        # print(encoding)

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
    return main_data


def write_to_csv(file_name):
    with open(file_name, 'w', encoding='utf-8') as f_n:
        writer = csv.writer(f_n)
        writer.writerows(file_read(file_names))


write_to_csv(out_file)
