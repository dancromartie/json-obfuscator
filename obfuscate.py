from jsonpath_rw import jsonpath, parse

import sys


def obfuscate(obj, path_list):
    clean_object = None
    # We need to keep track of previous paths because sometimes I think it tries to replace on 
    # its replacements, so sometimes we need to stop it.
    all_previous_paths = []
    for path, replacement_value in path_list:
        jsonpath_expr = parse(path)
        for match in jsonpath_expr.find(obj):
            match_path = str(match.full_path)
            for prev_path in all_previous_paths:
                if match_path.startswith(prev_path):
                    sys.exit("You seem to be replacing already replaced paths..."
                             "  Maybe tone down the jsonpath?")
            all_previous_paths.append(match_path)
            feature_value = match.value
            clean_object = change_value_at_path(match_path, replacement_value, obj)
    return clean_object


def change_value_at_path(path_string, new_value, obj):
    # Example path is 'sbcs.[0].scores.[0].customer.attributes.ssn'
    paths = path_string.split(".")
    if path_string == '':
        return new_value
    index = None
    path = paths[0]
    if path.startswith("[") and path.endswith("]"):
        index = int(path[1:-1])
    else:
        index = path
    new_path_string = ".".join(paths[1:])
    obj[index] = change_value_at_path(new_path_string, new_value, obj[index])
    return obj


def read_configs(file_path):
    """
    Gets a list of (path, replacement_value) tuples.
    """
    path_lines = open(file_path, "rb").readlines()
    path_configs = []
    for line in path_lines:
        splitup = line.strip().split(" ")
        assert len(splitup) == 2
        assert splitup[1] in ["DONTREALLYCARE", "OBFUSCATE"]
        path_configs.append((splitup[0], splitup[1]))
    return path_configs
