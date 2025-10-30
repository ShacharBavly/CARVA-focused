import os
import pandas as pd
from pathlib import Path

base_dir = Path.cwd().parent / "out" / "pcnet2" 
print(base_dir)
output_file = "results_summary.tsv"

columns = [
    "trait_rare", "trait_common", "network",
    "transform", "normalization",
    "mean_nps", "null_mean_nps", "p_mean_nps",
    "size", "null_size", "p_size"
]

all_dfs = []

for root, _, files in os.walk(base_dir):
    for fname in files:
        if fname.startswith(("netcoloc", "qnetcoloc")) and fname.endswith((".tsv", ".txt", ".csv")):
            fpath = os.path.join(root, fname)
            coloc_type = "binary" if fname.startswith("netcoloc") else "quantitative"

            try:
                df = pd.read_csv(fpath, sep="\t", header=None)
            except Exception:
                df = pd.read_csv(fpath, sep=",", header=None)

            # Assign known columns
            if df.shape[1] == len(columns):
                df.columns = columns
            else:
                print(f"{fname}: unexpected column count ({df.shape[1]}). Skipping.")
                continue

            df["coloc_type"] = coloc_type
            all_dfs.append(df)

if all_dfs:
    combined = pd.concat(all_dfs, ignore_index=True)
    combined.to_csv(base_dir / output_file, sep="\t", index=False)
    print(f"Combined file saved: {output_file}")
    print(f"Total rows: {len(combined)}  ,  Files merged: {len(all_dfs)}")
else:
    print("No valid netcoloc/qnetcoloc files found.")

