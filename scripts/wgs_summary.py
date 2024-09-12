# -*- coding: utf-8 -*-

# @author: miquelsanchezosuna, msanchezo@tauli.cat

# Load the necessary modules
import csv, json


def mlst_data(filename):
    # Open the file with the specified filename and read all lines
    with open(filename) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    lineage = "Unknown"
    # Iterate over each line in the file
    for line in lines:
        # Check if the line contains the string "Sequence Type: "
        if "Sequence Type: " in line:
            # If "unknown" is not in the line, extract the sequence type
            if not "known" in line:
                lineage = "ST"+line.split(" ")[-1]
    # Return the determined lineage
    return (lineage)


def spa_data(filename):
    spa_types = []
    # Open the file with the specified filename and read all lines
    with open(filename, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter = "\t")
        for row in csvreader:
            # Append the value of the "Type" column from each row to the spa_types list
            spa_types.append(row["Type"])
    # Return the list of spa types
    return (spa_types)


def agr_data(filename):
    # Open the file with the specified filename and read all lines
    with open(filename) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    agr_type = "Unknown"
    # Iterate over each line in the file
    for line in lines:
        # Check if the line contains the string "agr typing "
        if "agr typing " in line:
            agr_type = "agr"+line.split(" ")[-1].replace("gp", "")
    # Return the determined agr_type
    return (agr_type)


def abricate_data(filename, value):
    genes = []
    # Open the file with the specified filename and read all lines
    with open(filename) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    # Iterate over each line in the file
    for line in lines:
        if not line.startswith("#"):
            # Append the value of the predicted ARG/VF column from each row to the genes list
            if value == "ARG":
                genes.append(line.split("\t")[5]+"__"+line.split("\t")[-1])
            else:
                genes.append(line.split("\t")[5])
    # Remove possible redundancies and sort the list
    genes = list(set(genes))
    genes.sort()
    # Return predicted genes
    return (genes)


def resfinder_data(filename):   
    resist = []
    # Open the file with the specified filename and read all lines
    with open(filename, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter = "\t")
        for row in csvreader:
            name = row["Mutation"].replace(" p.", "__")+"__"+row["Resistance"]
            resist.append(name)
    # Remove possible redundancies and sort the list
    resist = list(set(resist))
    resist.sort()
    # Return predicted genes
    return (resist)        


def plasmid_data(filename):
    plasmids = []
    # Open the file with the specified filename and read all lines
    with open(filename, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter = "\t")
        for row in csvreader:
            name = "Plasmid_"+row["sample_id"].split(":")[-1]
            if row["relaxase_type(s)"] != "-":
                name += "__"+row["relaxase_type(s)"]
            if row["orit_type(s)"] != "-":
                name += "__"+row["orit_type(s)"]
            plasmids.append(name)
    # Remove possible redundancies and sort the list
    plasmids = list(set(plasmids))
    plasmids.sort()
    # Return predicted plasmids
    return (plasmids)


def prophage_data(filename):
    prophages = []
    # Open the file with the specified filename and read all lines
    with open(filename) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    for line in lines:
        name = "Prophage_region_"+line.split("\t")[0]+"__"+line.split("\t")[1]+"__"+line.split("\t")[2]+"__"+line.split("\t")[3]
        prophages.append(name)
    # Remove possible redundancies and sort the list
    prophages = list(set(prophages))
    prophages.sort()
    # Return predicted plasmids
    return (prophages)
        
            
###############################################################################

# Load the configuration file
with open("wgs_summary.json") as json_conf: 
    conf = json.load(json_conf)
    
# Strains names
strains = conf["strains"]

# "Molecular Typing" output files
mlst_file = conf["mlst_file"]
spa_file = conf["spa_file"]
agrvate_file = conf["agrvate_file"]

# "Prediction of ARGs, VFs, Plasmids, and Prophages" output files
args_file = conf["args_file"]
resfinder_file = conf["resfinder_file"]
vfs_file = conf["vfs_file"]
plasmid_file = conf["plasmid_file"]
prophage_file = conf["prophage_file"]

# Construct the dictionary and access all files for getting the data
d = {}
for i in range(0,len(strains)):
    d[strains[i]] = {
                        "MLST": mlst_data(mlst_file[i]),
                         "spa_type": spa_data(spa_file[i]),
                         "agr_type": agr_data(agrvate_file[i]),
                         "ARGs": abricate_data(args_file[i], "ARG")+resfinder_data(resfinder_file[i]),
                         "VFs": abricate_data(vfs_file[i], "VF"),
                         "plasmids": plasmid_data(plasmid_file[i]),
                         "propages": prophage_data(prophage_file[i])
                     }

# Save the results in an output file
with open(conf["output_file"], "w") as f:
    json.dump(d, f, indent = 2)
    
    
