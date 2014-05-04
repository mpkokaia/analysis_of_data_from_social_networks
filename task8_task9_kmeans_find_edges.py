# -*- coding: utf-8 -*-
from pymongo import Connection
import re

connection = Connection()
db = connection.urfu

f = open('k_means_result.txt')
data = f.readlines()
f.close()

numb_cluster = None
interests_cluster = {}
cluster_interests = {}
cluster = []
for line in data:
    line = line.strip()
    if re.search('[1-9]+', line):
        if numb_cluster:
            cluster_interests[numb_cluster] = cluster[:]
        numb_cluster = line
        cluster = []
    else:
        interests_cluster[line] = numb_cluster
        cluster.append(line)
cluster_interests[numb_cluster] = cluster[:]

hubs = []
for group in db.new_new_groups.find():
    if group['group'] not in interests_cluster:
        hubs.append(group['group'])

hub_group = {}
hub_list = []
for line in data:
    line = line.strip()
    if re.search('[1-9]+', line):
        numb_cluster = line
    else:
        cluster = []
        for user in db.interest_new_groups.find():
            interest = user['interests']
            if line in interest:
                for h in hubs:
                    if h in interest:
                        for inter in interest:
                            if inter in interests_cluster:
                                if h in hub_group:
                                    if interests_cluster[inter] not in hub_group[h]:
                                        hub_group[h].append(interests_cluster[inter])
                                else:
                                    hub_group[h] = [interests_cluster[inter]]

f_inp = open('hubs.txt', 'w')
for h in hub_group:
    if len(hub_group[h]) > 1:
        hub_list.append(hub_group[h])
        f_inp.write(' '.join(hub_group[h]))
        f_inp.write('\n')
f_inp.close()

