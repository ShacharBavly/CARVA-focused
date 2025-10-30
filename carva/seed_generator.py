import pandas as pd
import argparse
import sys


import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde

def sample_like_pvalues(tsv_file, column_name, num_samples):
    df = pd.read_csv(tsv_file, sep='\t')
    values = df[column_name].dropna().to_numpy()

    # if want to only sample
    return np.random.choice(values, size=num_samples, replace=True)
    # Build a kernel density estimate (continuous approximation)
    kde = gaussian_kde(values)
    
    # Draw samples from that estimated distribution
    samples = kde.resample(num_samples)[0]
    
    # Clip to valid p-value range [0, 1]
    samples = np.clip(samples, 0, 1)
    
    return samples


def select_random_lines(input_tsv_path: str, output_tsv_path: str, n: int, pvals: str):
    """
    Reads a TSV file, randomly selects 'n' unique lines, and writes them
    to a new TSV file.

    Args:
        input_tsv_path: Path to the input TSV file.
        output_tsv_path: Path to the output TSV file.
        n: The number of random lines to select.
    """
    try:
        # 1. Read the TSV file into a pandas DataFrame.
        # 'sep='\t'' specifies that the file is Tab-Separated.
        df = pd.read_csv(input_tsv_path, sep='\t')

        
        total_rows = len(df)
        
        if n <= 0:
            # Throw an error if n is not positive
            raise ValueError(f"Error: Number of lines to select (n={n}) must be a positive integer.")

        if n > total_rows:
            # Throw an error and terminate if n > total rows, as requested
            raise ValueError(
                f"Error: Requested lines (n={n}) is greater than the total lines in the file ({total_rows})."
            )

        if len(df.columns == 1):
            df.columns = ["Entrez"]

        random_selection_df = df.sample(n=n)
        if pvals:
            random_selection_df["P-value"] = sample_like_pvalues(pvals, "P-value", n)
        
        random_selection_df.to_csv(output_tsv_path, sep='\t', index=False)
        
        print(f"{n} random lines from {input_tsv_path} written to {output_tsv_path}")

    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_tsv_path}'")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"Error: Input file '{input_tsv_path}' is empty or has only a header.")
        sys.exit(1)
    except ValueError as ve:
        # Catch the custom ValueErrors for n <= 0 or n > total_rows
        print(f"{ve}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Randomly select 'n' unique lines from a TSV file and save to a new TSV.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '-i', '--input-file',
        type=str,
        required=True,
        help="Path to the input TSV file."
    )
    
    parser.add_argument(
        '-o', '--output-file',
        type=str,
        required=True,
        help="Path for the output TSV file."
    )
    
    parser.add_argument(
        '-n', '--num-lines',
        type=int,
        required=True,
        help="The number of random, non-repetitive lines to select."
    )

    parser.add_argument(
        '-p', '--pvals',
        type=str,
        required=False,
        help="where to sample p-values from."
    )

    args = parser.parse_args()
    select_random_lines(args.input_file, args.output_file, args.num_lines, args.pvals)