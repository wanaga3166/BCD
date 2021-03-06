#!/usr/bin/python3

import sys, os, re
from massTable import AMINOACIDS

pyScriptName = sys.argv[0]
fastaFileName = sys.argv[1]
outputFileName = sys.argv[2]
maxMissedCleavage = sys.argv[3]

# Read fasta file
fasta_dict = {}

# Variables
peptide_list = {}

#open(outputFileName, "w") as output_peptides,

with open(fastaFileName, "r") as fasta_file, open(outputFileName,"w") as output_peptides:
    sequence_id = ""
    for line in fasta_file:
        if line.startswith(">"):
            sequence_id = line.strip()
            fasta_dict[sequence_id] = ""
        else:
            fasta_dict[sequence_id] += line.strip()
            
    # Cleave a protein in different peptide with trypsin
    for id in fasta_dict.keys():
        print(id)
        seq = fasta_dict[id]
        site = [0]
        peptide = []
        print("\n")
        print("This protein has {} amino acids. \n".format(len(seq)))
        print("Trypsin digestion start. \n")
        for aa in range(0,len(seq)-1): # This line is necessary to avoid 
            if seq[aa] in 'KR' and seq[aa+1] != 'P':
                site.append(aa+1)
            #if seq[aa] == 'K' and seq[aa+1] != 'P':
            #    site.append(aa+1)

        if site[-1] != len(seq):
            site.append(len(seq))

        print("Trypsin digestion done. \n")

        print("Below, you will find the position list of cleavage site : \n")
        print(site, "\n")
            
        # Missed cleavage and print the different peptides
        print("Missed cleavage: {}".format(maxMissedCleavage))

        if int(maxMissedCleavage) == 0:
            for pep in range(0, len(site)-1):
                peptide.append(seq[site[pep]:site[pep+1]])
        elif int(maxMissedCleavage) == 1:
            for pep in range(0, len(site)-2):
                peptide.append(seq[site[pep]:site[pep+1]])
                peptide.append(seq[site[pep]:site[pep+2]])
            peptide.append(seq[site[-2]:site[-1]])
        elif int(maxMissedCleavage) == 2:
            for pep in range(0, len(site)-3):
                peptide.append(seq[site[pep]:site[pep+1]])
                peptide.append(seq[site[pep]:site[pep+2]])
                peptide.append(seq[site[pep]:site[pep+3]])
            peptide.append(seq[site[-3]:site[-1]])
        elif int(maxMissedCleavage) == 3:
            for pep in range(0, len(site)-4):
                peptide.append(seq[site[pep]:site[pep+1]])
                peptide.append(seq[site[pep]:site[pep+2]])
                peptide.append(seq[site[pep]:site[pep+3]])
                peptide.append(seq[site[pep]:site[pep+4]])
            peptide.append(seq[site[-4]:site[-1]])
                
        # Peptide mass calculus
        output_peptides.write(id + "\n")
        for pe in peptide:
            pepMass = 0
            for aa in pe:
                mass = AMINOACIDS[aa]
                pepMass += mass   
            print(pe, pepMass)
            output_peptides.write(pe + "\t" + str(pepMass) + "\n")

        output_peptides.write("\n")
            
        # Protein mass calculus
        mass = 0
        for AA in range(0, len(seq)-1):
            aaMass = AMINOACIDS[seq[AA]]
            mass += aaMass
        print("\n")
        print("Cette proteine a une masse de {:.3f} Da. \n".format(mass))
        
fasta_file.close()
output_peptides.close()
 
