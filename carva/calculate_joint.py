import pandas as pd
import sys

def main(zcommon_path, zrare_path, output_path):
    # Load the input TSV files
    zcommon = pd.read_csv(zcommon_path, sep='\t', header=None, names=['gene', 'z_common'])
    zrare = pd.read_csv(zrare_path, sep='\t', header=None, names=['gene', 'z_rare'])

    # Ensure both DataFrames are aligned by gene
    if not zcommon['gene'].equals(zrare['gene']):
        print("Error: Gene names in the two files do not match in order.")
        sys.exit(1)

    # Compute joint Z score
    joint_z = zcommon['z_common'] * zrare['z_rare']
    result = pd.DataFrame({
        'gene': zcommon['gene'],
        'joint_z': joint_z
    })

    # Apply filtering conditions
    mask = (zcommon['z_common'] >= 1) & (zrare['z_rare'] >= 1) & (joint_z >= 3)
    filtered_result = result[mask]

    # Save to output file
    filtered_result.to_csv(output_path, sep='\t', index=False, header=False)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python calculate.py <zcommon.tsv> <zrare.tsv> <output.tsv>")
        sys.exit(1)

    zcommon_file = sys.argv[1]
    zrare_file = sys.argv[2]
    output_file = sys.argv[3]

    main(zcommon_file, zrare_file, output_file)
