# -*- coding: utf-8 -*-
from re import search, findall
from pymongo import Connection
import re

connection = Connection()
db = connection.urfu

f = open('output')
data = f.readlines()
f.close
interests = []
for line in data:
    line = line.decode('utf-8')
    if search(r'[0-9]', line):
        if len(interests) > 1:
            db.users_interest.save({'vk_id': interests[0].strip(), 'interests': interests[1:]})
        interests = []
        interests.append(line)
    else:
        words = findall('{([^{]+)}', line)
        one_interest = []
        for w in words:
            var = w.split('|')
            if len(var) > 1:
                if re.findall(u'[а-яА-Я]{4,}', unicode(w)):
                    one_interest.append(re.findall(u'[а-яА-Я]{4,}', unicode(w))[0])
            else:
                if re.findall(u'[а-яА-Я]{4,}', unicode(w)):
                    one_interest.append(re.findall(u'[а-яА-Я]{4,}', unicode(w))[0])
        if one_interest:
            interests.append(' '.join(one_interest[:]))
if len(interests) > 1:
    db.users_interest.save({'vk_id': interests[0].strip(), 'interests': interests[1:]})
