# -*- coding: utf-8 -*-
from pymongo import Connection

connection = Connection()
db = connection.urfu
students = db.interest.find()
interest = []
for st in students:
    for data in st['interests']:
        groups = db.groups.find()
        for gr in groups:
            for i in gr['interests']:
                if i == data:
                    if gr['group'] not in interest:
                        interest.append(gr['group'])
    db.new_groups.save({'interests': interest[:], 'vk_id': st['vk_id']})
    interest = []