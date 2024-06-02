import pandas as pd
import re
import requests
import sys
def load_and_process_csv(file_path):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    # Function to extract the 6-digit UniProt ID from the protein column
    def extract_uniprot_id(protein_str):
        # Assuming the UniProt ID is always 6 digits and might be surrounded by other characters
        uniprot_pattern = r'\b[A-Z0-9]{6}\b'
        match = re.search(uniprot_pattern, protein_str)
        return match.group(0) if match else None
    
    # Apply the function to each value in the protein column
    df['Protein'] = df['Protein'].apply(extract_uniprot_id)
    
    return df

def fetch_fasta_sequence(uniprot_id):
    url = f"https://www.uniprot.org/uniprot/{uniprot_id}.fasta"
    response = requests.get(url)
    if response.status_code == 200:
        fasta_content = response.text
        return fasta_content
    else:
        return None
    
def main(csv_file_path, fasta_output_filename):
    # Process the CSV file
    df_processed = load_and_process_csv(csv_file_path)

    # Open a file to write all FASTA sequences
    with open(fasta_output_filename, "w") as outfile:
        # Fetch and write FASTA sequences for each UniProt ID
        for uniprot_id in df_processed['Protein']:
            fasta_sequence = fetch_fasta_sequence(uniprot_id)
            if fasta_sequence:
                outfile.write(fasta_sequence + "\n\n")
            else:
                print(f"No FASTA sequence found for {uniprot_id}")

    print(f"All FASTA sequences have been saved to {fasta_output_filename}.")

if __name__ == "__main__":
    if len(sys.argv)!= 3:
        print("Usage: python script_name.py csv_file_path fasta_output_filename")
    else:
        csv_file_path = sys.argv[1]
        fasta_output_filename = sys.argv[2]
        main(csv_file_path, fasta_output_filename)