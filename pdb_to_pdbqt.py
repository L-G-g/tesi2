from openbabel import openbabel

def convert_pdb_to_pdbqt(input_pdb_file, output_pdbqt_file):
    obConversion = openbabel.OBConversion()
    obConversion.SetInAndOutFormats("pdb", "pdbqt")

    mol = openbabel.OBMol()
    obConversion.ReadFile(mol, input_pdb_file)
    mol.AddPolarHydrogens()
    print(f"Conversion completed. PDBQT file saved as '{output_pdbqt_file}'.")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python convert_pdb_to_pdbqt.py input.pdb output.pdbqt")
        sys.exit(1)

    input_pdb_file = sys.argv[1]
    output_pdbqt_file = sys.argv[2]

    convert_pdb_to_pdbqt(input_pdb_file, output_pdbqt_file)