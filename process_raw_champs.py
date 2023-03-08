import json

champs_json = open("processed/champs.jsonl", "w")
with open("raw/champs.txt", "r") as champs:
    for champ_id, line in enumerate(champs):
        words = line.split(" ") # Will produce bad results for Lee Sin, Master Yi, Dr. Mundo etc. Manually edit names in processed/champs.jsonl
        name = words[0]
        title = " ".join(words[1:])[0].upper() + " ".join(words[1:])[1:]
        champ_detail = {"id": champ_id, "name": name, "title": title.rstrip("\n")}
        champs_json.write(json.dumps(champ_detail) + "\n")
