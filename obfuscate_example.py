import json
import obfuscate
import re

file_json = json.loads(open("to_obfuscate_example.json", "rb").read())

path_configs = []
path_configs.append({"path": "$..keep_part_of_me", "regex": "\d\d\d\d\dxxxx", "replace": "0000xxxx"})
path_configs.append({"path": "$..some_dict.stuff", "regex": "\d\d\d-?\d\d-?\d\d\d\d", "replace": "999999999"})
path_configs.append({"path": "$..byooroughReport", "func": lambda x: "I_DONT_CARE"})
path_configs.append({"path": "$..ssn", "func": lambda x: re.sub('[0-4]', '5', x)})


print "\nScrubbing this JSON: %s" % file_json
print "\nScrubbing with paths: %s" % path_configs
print "\nScrubbed JSON is: %s" % json.dumps(obfuscate.obfuscate(file_json, path_configs), indent=4)
