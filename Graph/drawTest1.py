import networkx as nx
import matplotlib.pyplot as mp
#regular graphy


rg=nx.random_regular_graph(4,10)
ps=nx.spectral_layout(rg)
nx.draw(rg,ps,with_labels=False,node_size=30)
mp.show()