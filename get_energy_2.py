import os
import pandas as pd

# Define the root directory where the 'fs_res' folder is located
root_dir = '/home/gabi/fs_res'

# Initialize an empty DataFrame to store the results
df = pd.DataFrame(columns=['Ligand', 'PDB_Crystal', 'Run', 'Binding_Energy'])

# Function to parse the docking.dlg file and extract the Run and Binding Energy values
def parse_docking_file(file_path, df):
    with open(file_path, 'r') as file:
        content = file.readlines()

        # Find the start of the RMSD TABLE section
        start_table_line = next(i for i, line in enumerate(content) if "RMSD TABLE" in line)
        
        # Initialize variables to hold the last run and binding energy found
        last_run = None
        last_binding_energy = None
        header = None
        # Iterate over the lines after the start of the table
        for line in content[start_table_line:]:

            # Skip empty lines and lines that don't contain relevant data
            if len(line) != 69:
                continue
            
            # Split the line by spaces and strip leading/trailing whitespaces
            split_line = [field.strip() for field in line.split()]

            if not header:
                header = split_line
                continue

            # Assuming the second column contains the Run value and the fourth column contains the Binding Energy
            try:

                run = int(split_line[2])
                binding_energy = float(split_line[3])
                print(run, binding_energy)
                new_row_df = pd.DataFrame({'Ligand': [ligand_name], 'PDB_Crystal': [pdb_crystal_name], 'Run': [run], 'Binding_Energy': [binding_energy]})
                
                # Concatenate the new row DataFrame with the existing DataFrame
                df = pd.concat([df, new_row_df])
                # Return the last run and binding energy found
            except ValueError:
                # Handle cases where the conversion fails due to unexpected data types
                pass
    return df


# Iterate over each ligand folder
for ligand_folder in os.listdir(root_dir):
    if os.path.isdir(os.path.join(root_dir, ligand_folder)):
        ligand_name = ligand_folder
        
        for pdb_crystal_folder in os.listdir(os.path.join(root_dir, ligand_folder)):
            if os.path.isdir(os.path.join(root_dir, ligand_folder, pdb_crystal_folder)):
                pdb_crystal_name = pdb_crystal_folder
                
                docking_file_path = os.path.join(root_dir, ligand_folder, pdb_crystal_folder, 'docking.dlg')
                
                df = parse_docking_file(docking_file_path, df)

# Display the final DataFrame
print(df)
df.to_csv('fs_res_ubiased.csv')
