import pandas as pd
import numpy as np
import argparse
import os

def get_args():
    parser = argparse.ArgumentParser(description="Generate random sample files from an input list.")
    parser.add_argument('-i', '--input', required=True, help="Path to input file (single headerless column).")
    parser.add_argument('-o', '--outdir', required=True, help="Directory to save the output files.")
    return parser.parse_args()

def generate_row_count():
    """
    Generates a random integer centered around 40.
    Range: [5, 150]
    Distribution: Normal (Gaussian) with Mean=40, SD=35.
    """
    # loc=40 centers the curve at 40.
    # scale=50 ensures the tail is fat enough to occasionally reach 110.

    val = np.random.normal(loc=40, scale=50)
    
    # Clip values to ensure they stay within the 5-150 range
    val = max(5, val)
    val = min(150, val)
    
    return int(val)

def main():
    args = get_args()

    # Create output directory if it doesn't exist
    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)
        print(f"Created output directory: {args.outdir}")

    # Read the headerless input file and give it a basic header
    try:
        df_master = pd.read_csv(args.input, header=None, names=['Entrez'], sep="\t")
    except Exception as e:
        print(f"Error reading input file: {e}")
        return

    print(f"Loaded input file with {len(df_master)} rows.")

    # Generate 100 files
    for i in range(100):
        # 1. Determine Sample Size (N)
        n_rows = generate_row_count()

        # 2. Sample N rows from the master file
        # replace=False prevents picking the same Entrez ID twice in one file
        # If input file has fewer rows than n_rows, we must use replace=True
        use_replace = len(df_master) < n_rows
        sample_df = df_master.sample(n=n_rows, replace=use_replace).copy()

        # 3. Generate P-values
        # We use a Log-Uniform distribution. 
        # A simple uniform(1e-10, 1e-6) would make values like 1e-10 statistically impossible to see 
        # compared to 1e-6. Log-uniform ensures equal probability across magnitudes.
        exponents = np.random.uniform(-10, -6, size=n_rows)
        p_values = 10 ** exponents
        
        sample_df['P-value'] = p_values

        # 4. Save to file
        # Filename format: rand_i_xv.txt
        filename = f"rand_{i}_xv.txt"
        out_path = os.path.join(args.outdir, filename)
        
        sample_df.to_csv(out_path, sep='\t', index=False)

    print(f"Successfully created 100 files in {args.outdir}")

if __name__ == "__main__":
    main()