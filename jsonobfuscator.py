from jsonpath_rw import jsonpath, parse

import json
import re
import sys

def is_scalar(val):
    return isinstance(val, (int, float, basestring))

def obfuscate(obj, path_configs):
    clean_object = None
    # We need to keep track of previous paths because sometimes I think it tries to replace on 
    # its replacements, so sometimes we need to stop it.
    for path_config in path_configs:
        all_previous_paths = []
        jsonpath_expr = parse(path_config["path"])
        for match in jsonpath_expr.find(obj):
            match_path = str(match.full_path)
            for prev_path in all_previous_paths:
                if match_path.startswith(prev_path):
                    sys.exit("You seem to be replacing already replaced paths..."
                             "  Maybe tone down the jsonpath?")
            all_previous_paths.append(match_path)
            feature_value = match.value
            clean_object = change_value_at_path(match_path, path_config, obj)
    return clean_object


def change_value_at_path(path_string, path_config, obj):
    # Example path is 'sbcs.[0].scores.[0].customer.attributes.ssn'
    paths = path_string.split(".")
    if path_string == '':
        if "regex" in path_config:
            regex_pattern = path_config["regex"]
            replacement = path_config["replace"]
            if not obj:
                return obj
            else:
                as_string = json.dumps(obj)
                clean_string = re.sub(regex_pattern, replacement, as_string)
                try:
                    return json.loads(clean_string)
                except:
                    print "Tried to json load: %s" % clean_string
                    print "JSON pre cleaning was: %s" % as_string
                    raise
        else:
            return path_config["func"](obj)
    index = None
    path = paths[0]
    if path.startswith("[") and path.endswith("]"):
        index = int(path[1:-1])
    else:
        index = path
    new_path_string = ".".join(paths[1:])
    obj[index] = change_value_at_path(new_path_string, path_config, obj[index])
    return obj
