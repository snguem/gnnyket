import json

with open("gnnyket.bd.json", "r") as f:
    datas = json.load(f)
    
with open("entities.config.txt", "r") as fil:
    struct = fil.read()

print(struct)

all_entities_struc = """"""
for entitie in datas["tables"]:
    struct_entities = struct.replace("//ENTITY",entitie["name"].upper()).replace("//TABLE",f"'{entitie["name"].lower()}'")
    keys_ = "("+ ",".join([f"'{attr["name"]}'" for attr in entitie["attributs"]]) +")"
        
    struct_entities = struct_entities.replace("//KEYS",keys_)
    all_entities_struc += struct_entities + "\n\n"

print(all_entities_struc)

with open("entities.py", "r") as f:
    file_ = f.read().replace("# //OTHER", all_entities_struc)

with open("entities.py", "w") as f:
    f.write(file_)

