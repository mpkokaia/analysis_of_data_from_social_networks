# -*- coding: utf-8 -*-
from pymongo import Connection
import re
import random


class KCluster(object):
    def __init__(self, data, k):
        self.rotatematrix(data)
        self.k = k

    def rotatematrix(self, data):
        self.data = []
        for i in range(len(data[0])):
            newrow = [data[j][i] for j in range(len(data))]
            self.data.append(newrow)

    def pearson(self, v1, v2):
        sum1 = sum(v1)
        sum2 = sum(v2)
        sum1Sq = sum([pow(v, 2) for v in v1])
        sum2Sq = sum([pow(v, 2) for v in v2])
        pSum = sum([v1[i] * v2[i] for i in range(len(v1))])
        num = pSum - (sum1 * sum2 / len(v1))
        den = pow((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2) / len(v1)), 1 / 2)
        if den == 0: return 0
        return 1.0 - num / den

    def clustering(self):
        ranges = [(min([row[i] for row in self.data]), max([row[i] for row in self.data])) for i in
                  range(len(self.data[0]))]
        clusters = [[random.random() * (ranges[i][1] - ranges[i][0]) + ranges[i][0] for i in range(len(self.data[0]))]
                    for j in
                    range(self.k)]
        lastmatches = None
        for t in range(100):
            bestmatches = [[] for i in range(self.k)]
            for j in range(len(self.data)):
                row = self.data[j]
                bestmatch = 0
                for i in range(self.k):
                    d = self.pearson(clusters[i], row)
                    if d < self.pearson(clusters[bestmatch], row):
                        bestmatch = i
                bestmatches[bestmatch].append(j)
            if bestmatches == lastmatches: break
            lastmatches = bestmatches
            for i in range(self.k):
                avgs = [0.0] * len(self.data[0])
                if len(bestmatches[i]) > 0:
                    for rowid in bestmatches[i]:
                        for m in range(len(self.data[rowid])):
                            avgs[m] += self.data[rowid][m]
                    for j in range(len(avgs)):
                        avgs[j] /= len(bestmatches[i])
                    clusters[i] = avgs
        return bestmatches


def read_data():
    rownames = []
    tmp_rownames = []
    colnames = []
    data = []
    connection = Connection()
    db = connection.urfu
    students = db.interest_new_groups.find({}, {'interests': 1})
    interest = {}
    for st in students:
        for data in st['interests']:
            if data in interest:
                interest[data] += 1
            else:
                interest[data] = 1
    for interes in interest:
        if interest[interes] > 2:
            colnames.append(interes)
    for interes in colnames:
        students = db.interest_new_groups.find({}, {'interests': 1, 'vk_id': 1})
        for st in students:
            for data in st['interests']:
                if data == interes:
                    if st['vk_id'] not in tmp_rownames:
                        tmp_rownames.append(st['vk_id'])
    data = []
    for i in tmp_rownames:
        tmp = []
        students = db.interest_new_groups.find_one({'vk_id': i})
        for j in colnames:
            if j in students['interests']:
                tmp.append(1)
            else:
                tmp.append(0)
        if sum(tmp) > 2:
            data.append(tmp[:])
            rownames.append(i)
    return colnames, rownames, data


interests, people, data = read_data()
kclust = KCluster(data, 27).clustering()
f = open('k_means_result.txt', 'w')
counter = 1
for i in range(27):
    f.write(str(counter) + '\n')
    counter += 1
    for r in kclust[i]:
        f.write(interests[r])
        f.write('\n')
f.close()
