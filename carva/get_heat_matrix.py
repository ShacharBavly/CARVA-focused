from netcoloc import netprop
import numpy as np
import sys
from network_utils import load_network
import os
import pandas as pd
import networkx as nx
import argparse

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Generate network diffusion matrices and node metadata.")
    parser.add_argument("--outdir", help="Output directory")
    parser.add_argument("--uuid", help="UUID of the network to load", required=False)
    parser.add_argument("--netfile", help="Filepath of network to load", required=False)
    parser.add_argument("--name", help="Base name for output files")
    parser.add_argument("--filter", help="Filter in the format <column>_<threshold> (e.g., score_10)", required=False, default=None)
    args = parser.parse_args()
    outdir = args.outdir
    uuid = args.uuid
    name = args.name
    if uuid is not None:
        G_PC = load_network(uuid)
    elif args.netfile is not None:
        df = pd.read_csv(args.netfile, sep='\t')
        try:
            G_PC = nx.from_pandas_edgelist(df, source='Entrez_A', target='Entrez_B')
        except KeyError:
            G_PC = nx.from_pandas_edgelist(df, source='Node_A', target='Node_B')
    print(len(G_PC.edges()), len(G_PC.nodes()))
    
    if args.filter is not None:
        filter_col, filter_th = args.filter.split('_')
        filter_th = float(filter_th)
        G_PC = nx.Graph([(u,v,d) for u,v,d in G_PC.edges(data=True) if float(d[filter_col])>=filter_th])
        print(len(G_PC.edges()), len(G_PC.nodes()))


    w_prime = netprop.get_normalized_adjacency_matrix(G_PC, conserve_heat=True, weighted=False)
    np.save(os.path.join(outdir, name+"_w_prime.npy"), w_prime)
    indiv_heats = netprop.get_individual_heats_matrix(w_prime, alpha=0.5)
    np.save(os.path.join(outdir,name+"_individual_heats.npy"), indiv_heats)
    pc_nodes_df = pd.DataFrame({'node': G_PC.nodes})
    pc_nodes_df.to_csv(os.path.join(outdir, name+ "_nodes.txt"), sep='\t', header=False, index=False)
    degree_map = pd.DataFrame(G_PC.degree())
    degree_map.to_csv(os.path.join(outdir, name+ "_degrees.txt"), sep='\t', header=False, index=False)