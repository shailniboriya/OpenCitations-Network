'''
Opencitations Network
fetching citation data of a specific research paper using COCI REST API
'''


import requests
import pandas as pd

#user input
doi=input("enter doi, ex- 10.1021/ci500020m : ")
cn=int(input("enter the number of citations to be used : "))
l=int(input("enter the number of levels : "))
sum = 0
for i in range (1, l+1):
  sum += cn**i
sum=sum+1 #total number of nodes [1+cn+cn^2+.....+cn^L] 

doilist=[doi] #list of all DOIs in network
dflist=[] #contains citation data of all DOIs in network
lst = []
metalist=[] # contains metadata of all DOIs in network

for z in doilist:
    res=requests.get(f'https://opencitations.net/index/coci/api/v1/citations/{z}')
    metares=requests.get(f'https://opencitations.net/index/coci/api/v1/metadata/{z}')
    datax = res.json()
    datam=metares.json()
    dlen=len(datax)
    if dlen>=cn:
        n=cn
    else:
        n=dlen
    datay=datax[0:n]
    dflist.append(datay)
    metalist.append(datam)
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

import networkx as nx
from pyvis.network import Network
import IPython

G = nx.from_pandas_edgelist(df,'cited','citing')
net=Network(height='1000px',width='100%',bgcolor='#222222',font_color='white',directed='True') #add layout = 'True' for heirarchical tree layout
net.from_nx(G)
net.save_graph('coci.html')
IPython.display.HTML(filename='coci.html')
