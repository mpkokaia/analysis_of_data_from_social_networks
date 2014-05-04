import warnings
import pygraphviz as pgv
from pymongo import Connection
import re

connection = Connection()
db = connection.urfu

warnings.simplefilter('ignore', RuntimeWarning)
A = pgv.AGraph(layout='fdp', overlap=False, splines=True)

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
        cluster.append(line)
cluster_interests[numb_cluster] = cluster[:]
Cluster = []
for cl in cluster_interests:
    line = ''
    for i in cluster_interests[cl]:
        line += i.decode('utf-8') + ', '
    interests_cluster[cl] = line
    Cluster.append(line)
A.add_nodes_from(Cluster, color='red')
f = open('hubs')
data_hubs = f.readlines()
f.close()
hubs = []
for line in data_hubs:
    data = line.split()
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            A.add_edge(interests_cluster[data[i]], interests_cluster[data[j]])
A.draw('2Dgraph_kmean.png', prog='dot')
