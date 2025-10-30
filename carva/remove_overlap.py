import pandas as pd
import sys
import os

def filter_tsv_by_entrez(file_path: str, entrez_list_str: str):
    """
    Reads a TSV file, removes rows where the 'Entrez' column value is in
    the provided list, and saves the filtered data to a new file path.
    """
    # 1. Parse the Entrez list from the string argument
    # Remove curly braces, split by comma, and strip whitespace from each item
    entrez_values_to_remove = [
        item.strip()
        for item in entrez_list_str.strip('{}').split(',')
        if item.strip()
    ]
    
    # 2. Construct the new output file path
    
    # Split the base name by '_' to find the insertion point
    parts = file_path.rsplit('_', 1)
    
    if len(parts) > 1:
        # Insert 'no-overlap' before the last '_'
        new_file_path = f"{parts[0]}_no-overlap_{parts[1]}"
    else:
        exit(13)

    df = pd.read_csv(file_path, sep='\t')
    
    print(f"Reading file: {file_path}")
    print(f"Input rows: {len(df)}")

    if not entrez_values_to_remove:
        print("Exclusion list was empty. No filtering performed.")
        df_filtered = df
    else:
        print(f"Excluding rows where 'Entrez' is in: {entrez_values_to_remove}")
        
        # Check for 'Entrez' column
        if 'Entrez' not in df.columns:
            print("Error: Column 'Entrez' not found in the file.")
            sys.exit(1)
            
        # Boolean mask for rows to KEEP (where 'Entrez' value is NOT in the exclusion list)
        # .astype(str) ensures comparison works even if Entrez column is numeric but list has strings
        df_filtered = df[~df['Entrez'].astype(str).isin(entrez_values_to_remove)]
        
        rows_removed = len(df) - len(df_filtered)
        print(f"Removed {rows_removed} rows.")
        print(f"Remaining rows: {len(df_filtered)}")
        
    print(f"Saving filtered data to: {new_file_path}")

    df_filtered.to_csv(new_file_path, sep='\t', index=False)
    print("Successfully completed.")


if __name__ == "__main__":
    # Check for the correct number of command-line arguments
    if len(sys.argv) != 3:
        print(sys.argv)
        print("Usage: python script_name.py <file_path.tsv> \"{a,b,...}\"")
        sys.exit(1)

    # Get the arguments
    input_file_path = sys.argv[1]
    exclusion_list_str = sys.argv[2]
    
    # Run the main function
    filter_tsv_by_entrez(input_file_path, exclusion_list_str)