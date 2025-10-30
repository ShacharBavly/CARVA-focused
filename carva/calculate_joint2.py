import argparse
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os

def main():
    parser = argparse.ArgumentParser(description="Extract colocalized genes and plot their network.")
    parser.add_argument('--z_common', required=True, help='Path to common variant z-score file')
    parser.add_argument('--z_rare', required=True, help='Path to rare variant z-score file')
    parser.add_argument('--outdir', required=True, help='Directory to save outputs')
    parser.add_argument('--network', required=False, help='Optional: path to precomputed network (edge list .txt)')
    parser.add_argument('--z_coloc', type=float, default=3.0, help='Threshold for colocalized Z (default=3)')
    parser.add_argument('--z1z2', type=float, default=1.5, help='Threshold for individual Z1 and Z2 (default=1)')
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    # --- Load Z-score files ---
    z_common = pd.read_csv(args.z_common, sep="\t", header=None, index_col=0).squeeze("columns")
    z_rare = pd.read_csv(args.z_rare, sep="\t", header=None, index_col=0).squeeze("columns")

    z_df = pd.DataFrame({"Common": z_common, "Rare": z_rare}).dropna()

    # --- Compute joined (colocalization) Z-score ---
    z_df["Z_coloc"] = z_df["Common"] * z_df["Rare"]

    # --- Apply CARVA-like thresholds ---
    filtered = z_df[
        (z_df["Z_coloc"] >= args.z_coloc) &
        (z_df["Common"] >= args.z1z2) &
        (z_df["Rare"] >= args.z1z2)
    ]

    # --- Save filtered gene list ---
    out_path = os.path.join(args.outdir, "colocalized_genes.tsv")
    filtered.to_csv(out_path, sep="\t", index=False)
    print(f"Saved {len(filtered)} colocalized genes to {out_path}")

main()

