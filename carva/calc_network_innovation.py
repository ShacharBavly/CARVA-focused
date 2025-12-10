import ndex2
import pandas as pd
import os
import sys
import json
from pathlib import Path


def get_node_display_name(network, node_id):
    """
    Determines the display name based on the logic:
    1. CD_CommunityName (if it exists and is not '(none)')
    2. name attribute
    3. node_id (fallback)
    """
    # Try CD_CommunityName
    comm_name = network.get_node_attribute(node_id, "CD_CommunityName")
    
    if comm_name:
        val = comm_name['v']
        # Check if valid string and not "(none)"
        if isinstance(val, str) and val.lower() != "(none)":
            return val

    # Fallback to 'name' attribute
    name_attr = network.get_node_attribute(node_id, "name")
    if name_attr:
        return name_attr['v']

    # Final fallback
    return str(node_id)

def process_network(cx_filepath, output_filepath, rare_genes, common_genes):
    
    exclusion_set = set(rare_genes).union(set(common_genes))
    print("size of exclusion set is", len(exclusion_set))

    print(f"Loading network {cx_filepath}...")
    network = ndex2.create_nice_cx_from_file(cx_filepath)

    print("\n--- Processing Communities ---")

    for node_id, node in network.get_nodes():
        # 1. Determine Display Name
        display_name = get_node_display_name(network, node_id)
        
        # 2. Get Member List
        member_attr = network.get_node_attribute(node_id, "CD_MemberList")
        
        if member_attr:
            # Ensure it is treated as a string
            raw_val = member_attr['v']
            if isinstance(raw_val, str):
                # Split string by space
                community_genes = [g.strip() for g in raw_val.split(' ') if g.strip()]
            else:
                # Skip if not a string representation
                continue

            total = len(community_genes)
            
            if total > 0:
                # 3. Calculate Unlisted Genes
                unlisted = [g for g in community_genes if g not in exclusion_set]
                count_unlisted = len(unlisted)
                fraction = count_unlisted / total

                # 4. Print to screen with custom name logic
                print(f"Community: {display_name} | Fraction Unlisted: {fraction:.4f} ({count_unlisted}/{total})")

                # 5. Set new attributes
                network.set_node_attribute(node_id, "Fraction_Unlisted", fraction, type="double")
                network.set_node_attribute(node_id, "Unlisted_Genes", " ".join(unlisted), type="string")

    print("------------------------------")
    print(f"Writing CX file to {output_filepath}...")
    
    # Writing the CX file structure to disk
    with open(output_filepath, 'w') as f:
        json.dump(network.to_cx(), f)

    print("Done.")

datadir = Path("../data")
common_df = pd.read_csv(datadir / "lupus_no-overlap_cv.txt", sep="\t")
commons = common_df["Entrez"].to_numpy(dtype=str)
rare_df = pd.read_csv(datadir / "lupus_rani_no-score_no-overlap_rv.txt", sep="\t")
rares  =rare_df["Entrez"].to_numpy(dtype=str)
print(type (rares[1]))

net_path = Path("../out") / "net_out/lupus"

process_network(net_path / "lupus_no-overlap_cdap.cx", net_path / "lupus_no-overlap_cdap_frac.cx", rares, commons)
