from pprint import pprint
#оставить pprint на случай, если понадобится печатать промежуточный результат (несколько случаев)
import requests
import time
import json
#оставить json на случай, если понадобится печатать промежуточный результат (несколько случаев)

TOKENnetology = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'


#получение списка id групп жертвы
id='171691064'
def ids_of_victim_groups():
    response = requests.get('https://api.vk.com/method/groups.get',
                            params={
                                'access_token': TOKENnetology,
                                'v': 5.52,
                                'extended': 1,
                                'user_id': id
                            })

    # pprint (response.json())
    victim_data = response.json()
    # print (victim_data)
    global victim_groups
    victim_groups=[]
    for items in (victim_data['response']['items']):
        a=items['id']
        victim_groups.append(a)
    print ('Список id групп "жертвы":')
    print(*victim_groups, sep=', ')
ids_of_victim_groups() #активация вывода списка id групп жертвы



#получение всех id друзей "жертвы"
def friends_list_getting():
    response = requests.get('https://api.vk.com/method/friends.get?user_id=171691064',
                            params={
                                'access_token': TOKENnetology,
                                'v': 5.52,
                            })

    friends_ids=response.json()
    global friends_ids_list
    friends_ids_list=[]
    for items in (friends_ids['response']['items']):
        b=items
        friends_ids_list.append(b)
    # print (friends_ids_list)
friends_list_getting() #вывод id друзей "жертвы"



#начало вывода списка групп всех друзей
def getting_ids_groups():
    i=0
    global idslist
    idslist=[]
    # print ('Формирование списка из id групп всех друзей жертвы. Это займёт какое-то время, ожидайте, пожалуйста.')
    print ('Отcчёт, ниже - сигнализирует о том, что программа работает,и завершит свою работу, когда число отсчёта совпадёт с количеством друзей жертвы.')
    for ids in friends_ids_list:
            # print (ids)
            print (i)
            time.sleep(3)
            response = requests.get('https://api.vk.com/method/groups.get?user_id=171691064',
                                    params={
                                        'access_token': TOKENnetology,
                                        'v': 5.52,
                                        'extended': 1,
                                        'user_id': ids,
                                    })
            answer=response.json()
            try:
                items = (answer['response']['items'])
                # pprint (items)
                for elements in items:
                    idsnumbers=elements['id']
                    # string_idsnumbers=str(idsnumbers) #если понадобится поменять на тип "string"
                    idslist.append(idsnumbers)
                # print (idslist)
                i += 1
            except KeyError:
                idsnumbers=''
                idslist.append(idsnumbers)
                # print (idslist)
                i += 1
            # for idnumbers in range(len(idslist)):
            #     idslist[idnumbers] = int(idslist[idnumbers])
            # print (idslist) - цикл преобразует элементы string списка idsnumbers.
            # Сначала у меня почему-то питон отказывался формировать список из int'ов, поэтому преобразовывал в string.
            # чтобы преобразовать обратно для дальнейшего сравнения списков - пришлось ввести цикл преобразования обратно в int.
getting_ids_groups()



#Вывод списка групп, которые есть только у жертвы
def recieving_only_victim_groups():
    victim_set=set(victim_groups)
    friends_set=set(idslist)
    final_set = victim_set.difference(friends_set)
    # print(final_set)
    groups_names = []
    i=0
    for ids in final_set:
        # print(ids)
        # print(i)
        time.sleep(3)
        response = requests.get('https://api.vk.com/method/groups.getById',
                                params={
                                    'access_token': TOKENnetology,
                                    'v': 5.52,
                                    'group_ids': ids,
                                    'fields': 'name'
                                })
        answer = response.json()
        group_name = (answer['response'][0]['name'])
        groups_names.append(group_name)
        i += 1
    j = 1
    for element in groups_names:
        print(f'Название группы №{j}, которая имеется только у жертвы - {element}')
        j += 1
recieving_only_victim_groups()



#блок с комментариями и попытками разных методов, которые оказались нерелевантны
def commentaries_and_irrelevant_cycles():
    a=0 #почему-то если в функции оставить только комментарии - пишет "SyntaxError: unexpected EOF while parsing". Поэтому добавил всё в одно.
    #работа с именами друзей (для того, чтобы потом "совместить" их с их списками групп)
    # (уже неактуально, но код пусть останется, для моей доработки в дальнейшем, мне самому интересно)
    # i=0
    # names_list_full=[]
    # for ids in friends_ids_list:
    #     print (ids)
    #     print (i)
    #     time.sleep(3)
    #     response = requests.get('https://api.vk.com/method/users.get?user_id=171691064',
    #                             params={
    #                                 'access_token': TOKENnetology,
    #                                 'v': 5.52,
    #                                 'extended': 1,
    #                                 'user_id': ids,
    #                             })
    #
    #     single_name=response.json()
    #     names_list_full.append(single_name)
    #     i += 1
    # # print (names_list_full)
    # i=0
    # names_list_short=[]
    # for elements in names_list_full:
    #     name = (elements['response'][i]['first_name'])
    #     names_list_short.append(name)
    #     surname = (elements['response'][i]['last_name'])
    #     names_list_short.append(surname)
    # # print (names_list_short)
    #
    # res = [[names_list_short[i], names_list_short[i + 1]]
    #        for i in range(len(names_list_short) - 1)]
    # del res[1::2]
    # pprint(res) #вывод списка друзей полный



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
