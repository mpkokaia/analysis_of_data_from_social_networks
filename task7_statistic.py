# -*- coding: utf-8 -*-
from pymongo import Connection

connection = Connection()
db = connection.urfu
students = db.users_interest.find({}, {'interests': 1})
interests = {}
for st in students:
    for data in st['interests']:
        if data in interests:
            interests[data] += 1
        else:
            interests[data] = 1
sort_interests = sorted(interests.items(), key=lambda (k, v): v, reverse=True)
for i in range(0, 20):
    print sort_interests[i][0] + ' - ' + str(sort_interests[i][1])
