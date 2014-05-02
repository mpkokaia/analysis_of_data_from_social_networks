# -*- coding: utf-8 -*-
from pymongo import Connection
import re

connection = Connection()
db = connection.urfu
students = db.users.distinct('vkid')
f = open('input.txt', 'w')
for student in students:
    user = db.users.find_one({'vkid': student}, {'_id': 0, 'users_get': 1})
    if u'interests' in user['users_get']:
        interests = user['users_get']['interests']
        sentanses = re.findall(u'[а-яА-Я ]{4,}', interests)
        if sentanses:
            f.write(str(student) + '\n')
            for sentans in sentanses:
                f.write(sentans.strip().encode('utf-8') + '\n')
f.close()
