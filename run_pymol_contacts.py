from pymol import cmd

def main():
    # Fetch the structure 2IE4
    cmd.fetch("2IE4")
    
    # Save the fetched structure as a PDB file
    cmd.save("2IE4.pdb", "all")

if __name__ == "__main__":
    main()