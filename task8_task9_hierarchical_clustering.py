# -*- coding: utf-8 -*-
from pymongo import Connection
import re
import random
from Tkinter import *


class cluster_object:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance


class HierarchicalCluster(object):
    def __init__(self, data):
        self.data = []
        for i in range(len(data[0])):
            newrow = [data[j][i] for j in range(len(data))]
            self.data.append(newrow)

    def clustering(self):
        distances = {}
        currentclustid = -1
        clust = [cluster_object(self.data[i], id=i) for i in range(len(self.data))]
        while len(clust) > 1:
            lowestpair = (0, 1)
            closest = self.tanamoto(clust[0].vec, clust[1].vec)
            for i in range(len(clust)):
                for j in range(i + 1, len(clust)):
                    if (clust[i].id, clust[j].id) not in distances:
                        distances[(clust[i].id, clust[j].id)] = self.tanamoto(clust[i].vec, clust[j].vec)
                    d = distances[(clust[i].id, clust[j].id)]
                    if d < closest:
                        closest = d
                        lowestpair = (i, j)
            mergevec = [(clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]) / 2.0 for i in
                        range(len(clust[0].vec))]
            newcluster = cluster_object(mergevec, left=clust[lowestpair[0]], right=clust[lowestpair[1]],
                                        distance=closest,
                                        id=currentclustid)
            currentclustid -= 1
            del clust[lowestpair[1]]
            del clust[lowestpair[0]]
            clust.append(newcluster)
        return clust[0]

    def tanamoto(self, v1, v2):
        c1, c2, shr = 0, 0, 0
        for i in range(len(v1)):
            if v1[i] != 0: c1 += 1
            if v2[i] != 0: c2 += 1
            if v1[i] != 0 and v2[i] != 0: shr += 1
        return 1.0 - (float(shr) / (c1 + c2 - shr))


class DrawHierarchicalClusters(object):
    def draw_node(self, draw, clust, x, y, scaling, labels):
        if clust.id < 0:
            h1 = self.getheight(clust.left) * 20
            h2 = self.getheight(clust.right) * 20
            top = y - (h1 + h2) / 2
            bottom = y + (h1 + h2) / 2
            ll = clust.distance * scaling
            draw.create_line([x, top + h1 / 2, x, bottom - h2 / 2], fill='green')
            draw.create_line([x, top + h1 / 2, x + ll, top + h1 / 2], fill='green')
            draw.create_line([x, bottom - h2 / 2, x + ll, bottom - h2 / 2], fill='green')
            self.draw_node(draw, clust.left, x + ll, top + h1 / 2, scaling, labels)
            self.draw_node(draw, clust.right, x + ll, bottom - h2 / 2, scaling, labels)
        else:
            label = (labels[clust.id]).encode('utf-8')
            draw.create_text(x + 5, y - 7, text=label)

    def draw_hierarchical(self, clust, labels, jpeg='clusters.png'):
        h = self.getheight(clust) * 20
        w = 1200
        depth = self.getdepth(clust)
        scaling = float(w - 150) / depth
        root = Tk()
        cv = Canvas(root, width=w, height=700, bg='white', scrollregion=(0, 0, w, h))
        vbar = Scrollbar(root, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=cv.yview)
        cv.config(yscrollcommand=vbar.set)
        cv.pack()
        cv.create_line([0, h / 2, 10, h / 2], fill='green')
        self.draw_node(cv, clust, 10, (h / 2), scaling, labels)
        root.mainloop()

    def getheight(self, clust):
        if clust.left == None and clust.right == None: return 1
        return self.getheight(clust.left) + self.getheight(clust.right)

    def getdepth(self, clust):
        if clust.left == None and clust.right == None: return 0
        return max(self.getdepth(clust.left), self.getdepth(clust.right)) + clust.distance


def read_data():
    rownames = []
    tmp_rownames = []
    colnames = []
    data = []
    connection = Connection()
    db = connection.urfu
    students = db.new_groups.find({}, {'interests': 1})
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
        students = db.new_groups.find({}, {'interests': 1, 'vk_id': 1})
        for st in students:
            for data in st['interests']:
                if data == interes:
                    if st['vk_id'] not in tmp_rownames:
                        tmp_rownames.append(st['vk_id'])

    data = []
    for i in tmp_rownames:
        tmp = []
        students = db.new_groups.find_one({'vk_id': i})
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
clust = HierarchicalCluster(data).clustering()
DrawHierarchicalClusters().draw_hierarchical(clust, interests)
