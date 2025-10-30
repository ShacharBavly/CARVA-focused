from neteval.shuffle_networks import shuffle_network, parse_arguments
import neteval.data_import_export_tools as dit
import argparse
import sys
import os
import pandas as pd
import networkx as nx

def successive_shuffles(G, nSwaps, nshuffs, outpath, prefix):
    similarity_to_original = {}
    for i in range(nshuffs):
        if i == 0:
            G_shuff = shuffle_network(G, nSwaps)
        else:
            G_shuff = shuffle_network(G_shuff.copy(), nSwaps)
        similarity_to_original[i] = len(set(G.edges()).intersection(set(G_shuff.edges())))/len(set(G.edges()))
        write_network(G_shuff, outpath, prefix, suffix=f'_{i}.shuffled')
    pd.DataFrame({'sims':similarity_to_original}).to_csv(os.path.join(outpath, prefix+'_similarities.txt'))
        
        
def write_network(G, outpath, prefix, suffix):
    outfile = os.path.join(outpath, prefix + suffix)
    print(outfile)
    dit.write_networkx_to_file(G, outfilepath=outfile)



if __name__ == '__main__':
    args = parse_arguments(sys.argv[1:])
    prefix = os.path.split(args.datafile)[1]
    if args.verbose:
        print(args)
        print("Analysis of", args.datafile)  
    G = dit.load_edgelist_to_networkx(args.datafile, testmode=args.testMode)
    if args.verbose:
        print("Data Loaded")
    if len(G.edges) > 0:
        for i in range(3):
            successive_shuffles(G, args.nSwaps, nshuffs=20, outpath=args.o, prefix=prefix+f'shuffnet{i}')
            if args.verbose:
                print("Network Shuffled")

    else:
        print("NO EDGES:", args.datafile)