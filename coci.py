'''
Opencitations Network
fetching citation data of a specific research paper using COCI REST API
'''


#import libraries
import requests
import pandas as pd
import math
#user input
doi=input("enter doi, ex- 10.1021/ci500020m : ")
cn=int(input("enter the number of citations to be used : "))
L=int(input("enter the number of levels : "))
sum = 0
for i in range (1, L+1):
  sum += (math.pow(cn, i))
sum=sum+1 #total number of nodes [1+cn+cn^2+.....+cn^L] 

doilist=[doi] #list of all DOIs in network
dflist=[] #list of list of dictionaries, contains data of all DOIs in network
lst = []

for z in doilist:
    res=requests.get(f'https://opencitations.net/index/coci/api/v1/citations/{z}')
    datax = res.json()
    dlen=len(datax)
    if dlen>=cn:
        n=cn
    else:
        n=dlen
    datay=datax[0:n]
    dflist.append(datay)
    for j in range(n):
        data1x=datax[j]
        dfy=list(data1x.keys())
        dfx=list(data1x.values())
        datf=pd.DataFrame({"value":dfx,"key":dfy})
        lst.append(dfx)
        y=datf.loc[datf['key'] == 'citing', 'value'].iloc[0]
        doilist.append(y)
    if sum==len(doilist):
      break
df = pd.DataFrame(lst, columns=dfy)

#Visualisation....................................

#Network
import networkx as nx
from pyvis.network import Network

G = nx.from_pandas_edgelist(df,'cited','citing')
net=Network(height='1000px',width='100%',bgcolor='#222222',font_color='white')
net.from_nx(G)
net.save_graph('coci.html')

#Tree
from anytree import Node, RenderTree
def add_nodes(nodes, parent, child):
    if parent not in nodes:
        nodes[parent] = Node(parent)  
    if child not in nodes:
        nodes[child] = Node(child)
    nodes[child].parent = nodes[parent]

data = df
nodes = {}  # store references to created nodes 
# data.apply(lambda x: add_nodes(nodes, x["Parent"], x["Child"]), axis=1)  # 1-liner
for parent, child in zip(data["cited"],data["citing"]):
    add_nodes(nodes, parent, child)

roots = list(data[~data["cited"].isin(data["citing"])]["cited"].unique())
for root in roots:         # you can skip this for roots[0], if there is no forest and just 1 tree
    for pre, _, node in RenderTree(nodes[root]):
        print("%s%s" % (pre, node.name))
