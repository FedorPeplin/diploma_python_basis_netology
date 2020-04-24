from pprint import pprint
import urllib
import urllib3
from urllib.parse import urlencode
import requests
import time
from ast import literal_eval
import json
import ast

TOKENnetology = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'


response = requests.get('https://api.vk.com/method/groups.get?user_id=171691064',
                        params={
                            'access_token': TOKENnetology,
                            'v': 5.52,
                            'extended': 1
                        })

# pprint (response.json())
evgenii_data = response.json()

evgenii_groups=[]
for items in (evgenii_data['response']['items']):
    a=items['name']
    evgenii_groups.append(a)
# print (evgenii_groups) #получили список групп Евгения

#получение всех id друзей Евгения
response = requests.get('https://api.vk.com/method/friends.get?user_id=171691064',
                        params={
                            'access_token': TOKENnetology,
                            'v': 5.52,
                        })

friends_ids=response.json()

friends_ids_list=[]
for items in (friends_ids['response']['items']):
    b=items
    friends_ids_list.append(b)

# print (friends_ids_list) - вывод id всех друзей


# работа с именами друзей (для того, чтобы потом "совместить" их с их списками групп)
i=0
names_list_full=[]
for ids in friends_ids_list:
    # print (ids)
    # print (i)
    time.sleep(3)
    response = requests.get('https://api.vk.com/method/users.get?user_id=171691064',
                            params={
                                'access_token': TOKENnetology,
                                'v': 5.52,
                                'extended': 1,
                                'user_id': ids,
                            })

    single_name=response.json()
    names_list_full.append(single_name)
    i += 1
# print (names_list_full)
i=0
names_list_short=[]
for elements in names_list_full:
    name = (elements['response'][i]['first_name'])
    names_list_short.append(name)
    surname = (elements['response'][i]['last_name'])
    names_list_short.append(surname)
# print (names_list_short)

res = [[names_list_short[i], names_list_short[i + 1]]
       for i in range(len(names_list_short) - 1)]
del res[1::2]
# pprint(res) вывод списка друзей полный


#начало вывода списка групп
i=0
users_group_list_full = []
users_group_list_shorted=[]
for ids in friends_ids_list:
        print (ids)
        print (i)
        time.sleep(3)
        response = requests.get('https://api.vk.com/method/groups.get?user_id=171691064',
                                params={
                                    'access_token': TOKENnetology,
                                    'v': 5.52,
                                    'extended': 1,
                                    'user_id': ids,
                                })
        users_group_list_full.append(response.json())
        i += 1
        # pprint (users_group_list_full)
        for elements in users_group_list_full:
            for elements2 in (elements['response']['items']):
                group_name=(elements2['name'])
                users_group_list_shorted.append(group_name)
        print (users_group_list_shorted)
#эксмеримент неудачен - выводятся группы некорректно, т.е.:
#1. выводится спискок групп пользователя №1, всё ок
#2. к нему добавляется не просто список групп друга номер 2 (почему-то не как отдельный элемент, а как продолжение списка, но это я ещё подумаю как исправить
#3. результат некорректен - выводится список групп (друга номер 1), список групп (друга номер 1+ (друга номер1+друга номер 2)), список групп (друга номер 1 + (друга номер 1+ друга номер 2) + (друга номер 1+друга номер 2+друга номер 3)
#пока не знаю, где сделать нормальное разграничение.
#


#         неудачная попытка вывода списка групп
#         try:
#             a=(users_group_list_full[i]['response']['items'][i]['name'])
#             print (a)
#             users_group_list_shorted.append(a)
#             i+=1
#         # except KeyError:
#         #         a='Нерабочая группа'
#         #         print(a)
#         #         users_group_list_shorted.append(a)
#         except IndexError:
#                 a='Нерабочая группа'
#                 print(a)
#                 users_group_list_shorted.append(a)
#         continue
# i += 1



# неудачная попытка записать в файл имена
# list = [{'response': [{'id': 1, 'first_name': 'John', 'last_name': 'Wick'}]}, {'response': [{'id': 2, 'first_name': 'Keanu', 'last_name': 'Reaves'}]}]
# with open('output.txt', 'w') as outfile:
#     for elements in list:
#         line =  ''.join([str(value) for key,value in elements.items()]) + '\n'
#         outfile.write(line)
#
# d = {}
# with open("output.txt", 'r') as file:
#     for line in file:
#         key, *value = line.split()
#         d[key] = value
# print (d)
