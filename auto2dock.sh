#!/bin/bash




# Check if Open Babel is installed
if ! command -v obabel &> /dev/null; then
    echo "Error: Open Babel is not installed. Please install it before running this script."
    exit 1
fi

# Check if the correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <docking_ligand_SMILES> <docking_ligand_ID> <PDB_ID>"
    exit 1
fi


# Assign arguments to variables
smiles="$1"
docking_ligand_ID="$2"
smiles_smi="${docking_ligand_ID}.smi"
smiles_mol2="${docking_ligand_ID}.mol2"
docking_ligand="${docking_ligand_ID}.pdb"
docking_ligand_pdbqt="${docking_ligand_ID}.pdbqt"
pdb_ID="$3"
receptor="${pdb_ID}.pdb"
receptor_pdbqt="${receptor}qt"
r_maps_fld="${pdb_ID}.maps.fld"

# Creates the directory and smi file
mkdir -p ""$docking_ligand_ID"_"$pdb_ID""
cd ""$docking_ligand_ID"_"$pdb_ID""
echo "$smiles" > "$smiles_smi"

# Downloading the PDB file
wget -O "./$receptor" "https://files.rcsb.org/download/$receptor"

# Checking if download was successful
if [ $? -eq 0 ]; then
    echo "Download successful: $receptor is saved in the current working directory"
else
    echo "Download failed. Please verify the PDB code and try again."
fi


# Create directory if it doesn't exist
#output_dir="$r"
#mkdir -p "$output_dir"
output_dir=$(pwd)

# Run ligand extraction script
python3 ../ligand_extraction.py $output_dir --pdb $receptor 

# Move ligand files to output directory
#mv lig_*.pdb "$output_dir"

# Prompt user to choose from estructural ligands
ligand_files=("$output_dir"/lig_*.pdb)
if [ ${#ligand_files[@]} -eq 0 ]; then
    echo "No ligand files found."
    exit 1
fi

echo "Choose a ligand file:"
select ligand_file in "${ligand_files[@]}"; do
    if [ -n "$ligand_file" ]; then
        echo "You selected: $ligand_file"
        break
    else
        echo "Invalid selection."
    fi
done

# Assign output name to variable
structural_ligand_pdbqt_full="${ligand_file%.*}.pdbqt"
# Extract filename with extension
structural_ligand_pdbqt=$(basename "$structural_ligand_pdbqt_full")

# Run the pdbqt transformation for the estructural ligand
output_estructural_pdbqt=$(pythonsh /home/gabi/tools/mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_ligand4.py -A hidrogens -l "$ligand_file" -o "$structural_ligand_pdbqt" 2>&1)

# Check if the conversion was successful
if [ $? -eq 0 ]; then
    echo "Estructural ligand conversion successful. Output saved to $structural_ligand_pdbqt."
else
    warning_message=$(echo "$output_estructural_pdbqt" | grep "WARNING:")
    echo "$warning_message"
fi
# Run the Open Babel smi -> mol2 -> pdbqt transformation.
obabel -ismi "./$smiles_smi" -omol2 -O "./$smiles_mol2" --gen3d --minimize --steps 1500 --sd -h --ff UFF 

# Check if the conversion was successful
if [ $? -eq 0 ]; then
    echo "New ligand smi -> mol2 conversion successful. Output saved to $smiles_mol2"
else
    echo "Error during docking ligand pdbqt transformation. Please check and try again."
fi

obabel "./$smiles_mol2" -O "./$docking_ligand_pdbqt" -h 
# Check if the conversion was successful
if [ $? -eq 0 ]; then
    echo "New ligand pdbqt conversion successful. Output saved to $docking_ligand_pdbqt"
else
    echo "Error during docking ligand pdbqt transformation. Please check and try again."
fi

# Ron the random state transformation for the docking ligand
pythonsh /home/gabi/tools/mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs/AutoDockTools/Utilities24/write_random_state_ligand.py -l "$docking_ligand_pdbqt" -o ligando_dock.pdbqt &> /dev/null

# Check if the conversion was successful
if [ $? -eq 0 ]; then
    echo "Succesful random state transformation. Output saved to ligando_dock.pdqbt" 
else
    echo "Unsuccesful random state transformation"
fi

# Delete waters and ligands from the receptor.

pdb_delhetatm $receptor > temp.pdb && rm $receptor && mv temp.pdb $receptor 

# Check if the conversion was successful
if [ $? -eq 0 ]; then
    echo "Succesful heteroatoms substracctions. Output saved to ligando_dock.pdqbt" 
else
    echo "Unsuccesful random state transformation"
fi


# Run the receptor transformation, if needed it takes the first conformation.
output_prepare_receptor=$(pythonsh /home/gabi/tools/mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_receptor4.py -A hydrogens -r "$receptor" -o "$receptor_pdbqt" 2>&1)

if [[ "$output_prepare_receptor" == *"WARNING!"* ]]; then
        echo "Multiple conformations found. Will proceed with the first one"
        pythonsh /home/gabi/tools/mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_pdb_split_alt_confs.py -r "$receptor" &> /dev/null
        r_maps_fld="${pdb_ID}_A.maps.fld"
        receptor_A="${pdb_ID}_A.pdb"
        receptor_A_pdbqt="${receptor_A}qt"
        pythonsh /home/gabi/tools/mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_receptor4.py -A hydrogens -r "$receptor_A" -o "$receptor_A_pdbqt" &> /dev/null
        receptor_pdbqt=$receptor_A_pdbqt

        if [ $? -eq 0 ]; then
            echo "Conformational receptor spliting conversion successful. Output saved to $receptor_A_pdbqt."
        else
            echo "Error during conversion. Please check your input and try again."
        fi
else
    echo "Initial receptor pdbqt conversion successful. Output saved to $receptor_pdbqt."
fi
# Prepare a gfp with the estructural ligand to extract the gridcenter
output_gpf=$(pythonsh /home/gabi/tools/mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_gpf4.py -y -l $structural_ligand_pdbqt -r $receptor_pdbqt -o receptor_coordenadas.gpf 2>&1)

# Check if the conversion was successful
if [ $? -eq 0 ]; then
    echo "Gridcenter setting successful. Output saved to receptor_coordenadas.gpf"
else
    warning_message=$(echo "$output_gpf")
    echo "$warning_message"
fi

# Run grep command to find the line containing "gridcenter"
output=$(grep "gridcenter" receptor_coordenadas.gpf)

# Extract coordinates using awk
coordinates=$(echo "$output" | awk '{print $2,$3,$4}')

# Replace spaces with commas
coordinates=${coordinates// /,}

# Format the output string
gridcenter="gridcenter='$coordinates'"

# Print the formatted output
pythonsh /home/gabi/tools/mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_gpf4.py -l $docking_ligand_pdbqt -r $receptor_pdbqt -p gridcenter=$coordinates -o receptor.gpf &> /dev/null

if [ $? -eq 0 ]; then
    echo "Final gpf generation successful, output save to receptor.gpf"
else
    echo "Error during final gpf generation. Please check your input and try again."
fi
# Append parameter_file AD4_parameters.dat at the start of receptor.gpf
sed -i '1i\
parameter_file AD4_parameters.dat\
' receptor.gpf
# Make the map
cp ../AD4_parameters.dat .
autogrid4 -p receptor.gpf -l receptor.glg # no genera el mapa de nitrogeno

if [ $? -eq 0 ]; then
    echo "Maps generation successfull"
else
    echo "Error during final gpf generation. Please check your input and try again."
fi

# Run the
autodock_gpu_64wi -ffile $r_maps_fld -lfile ligando_dock.pdbqt -nrun 100 -gfpop 1 -npdb -clustering
