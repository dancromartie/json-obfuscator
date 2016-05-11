from jsonpath_rw import jsonpath, parse

import copy
import json
import re
import sys


def is_scalar(val):
    return isinstance(val, (int, float, basestring))


def get_matches(obj, path_configs):
    all_paths = []
    for path_config in path_configs:
        these_paths = {"path_config": path_config, "matches": []}
        jsonpath_expr = parse(path_config["path"])
        for match in jsonpath_expr.find(obj):
            match_path = str(match.full_path)
            these_paths["matches"].append({
                "value": match.value,
                "path": match_path
            })
        all_paths.append(these_paths)
    return all_paths


def obfuscate(obj, path_configs):
    if not path_configs:
        sys.exit("You need at least one path config")
    clean_object = obj
    # We need to keep track of previous paths because sometimes I think it tries to replace on 
    # its replacements, so we need to stop it.
    all_previous_paths = set()
    matches_by_config = get_matches(obj, path_configs)
    for mbc in matches_by_config:
        for match in mbc["matches"]:
            for prev_path in all_previous_paths:
                if match["path"].startswith(prev_path):
                    sys.exit("You seem to be replacing already replaced paths..."
                             "  Maybe tone down the jsonpath?")
            if match["path"] in all_previous_paths:
                pass
            else:
                all_previous_paths.add(match["path"])
                feature_value = match["value"]
                orig_obj = copy.deepcopy(obj)
                clean_object = change_value_at_path(
                    match["path"], mbc["path_config"], obj, orig_obj)
    return clean_object


def change_value_at_path(path_string, path_config, obj, orig_obj):
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
            return path_config["func"](orig_obj, obj)
    index = None
    path = paths[0]
    if path.startswith("[") and path.endswith("]"):
        index = int(path[1:-1])
    else:
        index = path
    new_path_string = ".".join(paths[1:])
    obj[index] = change_value_at_path(new_path_string, path_config, obj[index], orig_obj)
    return obj
