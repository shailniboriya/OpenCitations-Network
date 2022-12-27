'''
Opencitations Network
fetching citation data of a specific research paper using COCI REST API
'''


import requests
import pandas as pd

#user input
doi=input("enter doi, ex- 10.1021/ci500020m : ")


doilist=[doi] #list of all DOIs in network
lst = []

for z in doilist:
    res=requests.get(f'https://opencitations.net/index/coci/api/v1/citations/{z}')
    datax = res.json()
    dlen=len(datax)
    n=dlen
    for j in range(n):
        data1x=datax[j]
        dfy=list(data1x.keys())
        dfx=list(data1x.values())
        datf=pd.DataFrame({"value":dfx,"key":dfy})
        lst.append(dfx)
        y=datf.loc[datf['key'] == 'citing', 'value'].iloc[0]
        doilist.append(y)
        
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


#extracting metadata of all the DOIs in the network for further data analysis

metalist=[] # contains metadata of all DOIs in network
for k in doilist:
    metares=requests.get(f'https://opencitations.net/index/coci/api/v1/metadata/{k}')
    datam=metares.json()
    metalist.append(datam)

#extracting urls of all the open access DOIs in the network

from urlextract import URLExtract
metastr=str(metalist)
extractor = URLExtract()
urls = extractor.find_urls(metastr)
    
