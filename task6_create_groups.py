# -*- coding: utf-8 -*-
from pymongo import Connection

connection = Connection()
db = connection.urfu

u_interest = []
groups = {}

us_gr = db.groups.find({}, {'interests': 1, 'group': 1})

counter = 0
for u in us_gr:
    counter += 1
    u_interest += u['interests']
    groups[str(counter)] = u['group']

students = db.interest.find({}, {'interests': 1})

interests_dict = {}
interests_list = []
for st in students:
    for data in st['interests']:
        if data in interests_dict:
            interests_dict[data] += 1
        else:
            interests_dict[data] = 1

for interes in interests_dict:
    if interests_dict[interes] > 2 and interes not in u_interest:
        interests_list.append(interes)

interests = []

for inte in interests_list:
    if inte not in interests:
        for gr in sorted(groups):
            print gr + ' - ' + groups[gr]
        print '\n' + inte
        inp = raw_input('')
        if inp == '0' or inp == '':
            name = raw_input(u'group: ')
            groups[str(len(groups) + 1)] = name
            db.groups.save({'group': name.strip(), 'interests': [inte]})
        else:
            us_gr = db.groups.find_one({'group': groups[inp]}, {'interests': 1})['interests']
            us_gr.append(inte)
            db.groups.update({'group': groups[inp]}, {'$set': {'interests': us_gr}})
        interests.append(inte)

