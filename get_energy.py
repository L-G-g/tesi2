import os
import re
import pandas as pd

# Define the root directory where the 'fs_res' folder is located
root_dir = '/home/gabi/fs_res'

# Initialize an empty DataFrame to store the results
df = pd.DataFrame(columns=['Ligand', 'PDB_Crystal', 'Run', 'Binding_Energy'])

# Iterate over each ligand folder
for ligand_folder in os.listdir(root_dir):
    if os.path.isdir(os.path.join(root_dir, ligand_folder)):
        # Check if the current item is a ligand folder (e.g., 'BZB')
        ligand_name = ligand_folder
        # Iterate over each PDB crystal folder within the ligand folder
        for pdb_crystal_folder in os.listdir(os.path.join(root_dir, ligand_folder)):
            if os.path.isdir(os.path.join(root_dir, ligand_folder, pdb_crystal_folder)):
                # Extract the PDB crystal name (e.g., 'BZB_2IE4')
                pdb_crystal_name = pdb_crystal_folder
                
                # Construct the path to the docking.dlg file
                docking_file_path = os.path.join(root_dir, ligand_folder, pdb_crystal_folder, 'docking.dlg')
                
                # Read the docking.dlg file and extract the Run and Binding Energy numbers
                with open(docking_file_path, 'r') as file:
                    content = file.read()
                    match_run = re.search(r"Run\s*:\s*(\d+)", content)
                    match_binding_energy = re.search(r"Binding Energy\s*:\s*(-?\d+\.\d+)", content)
                    print(match_run, match_binding_energy)

                    if match_run and match_binding_energy:
                        run = int(match_run.group(1))
                        binding_energy = float(match_binding_energy.group(1))
                        
                        # Append the extracted data to the DataFrame
                        df = df.append({'Ligand': ligand_name, 'PDB_Crystal': pdb_crystal_name, 'Run': run, 'Binding_Energy': binding_energy}, ignore_index=True)

# Display the final DataFrame
print(df)