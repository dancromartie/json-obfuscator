import json
import obfuscate

file_json = json.loads(open("to_obfuscate_example.json", "rb").read())
path_configs = obfuscate.read_configs("obfuscation_paths_example.txt")

print "Scrubbing this JSON: %s" % file_json
print "Scrubbing with paths: %s" % path_configs
print "Scrubbed JSON is: %s" % json.dumps(obfuscate.obfuscate(file_json, path_configs), indent=4)
