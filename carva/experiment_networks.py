from netcoloc import netprop
import numpy as np
import sys
from network_utils import load_network
import os
import pandas as pd
import networkx as nx
import itertools

outdir=str(sys.argv[1]) # Output directory for the heat matrix and node information
uuid=str(sys.argv[2]) # NDEx UUID of the network to load
name=str(sys.argv[3]) # Name for the output files
try:
    filt=str(sys.argv[4]).split('_') # Filter specification in the format "column_threshold", e.g., "degree_10"
    filter_col = filt[0] # Column to filter on, e.g., "degree"
    filter_th = int(filt[1]) # Threshold for filtering, e.g., 10

except IndexError:
    filter_col = ""
    filter_th = 0

# Load the network from NDEx
G_PC = load_network(uuid)
print(len(G_PC.edges()), len(G_PC.nodes()))

for n, d in itertools.islice(G_PC.nodes(data=True), 3):
    print(n, d)

with open(os.path.join(outdir, name + "_graph.pkl"), "wb") as f:
    pickle.dump(G_PC, f)