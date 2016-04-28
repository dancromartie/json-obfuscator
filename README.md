# json-obfuscator

## Dependencies

pip install jsonpath-rw, see https://github.com/kennknowles/python-jsonpath-rw

## Example input

```
{
    "something": [{
        "scores": [{
            "customer": {"attributes": {"ssn": 111223333} }
        }] 
    }],
    "byooroughReport": {
        "im": {
            "over": ["here", "im", "hard", "to", "get", {"to": ["111-22-4444"]}]
        }
    }
}
```

## Example config file

Paths are jsonpaths, which get plugged into jsonpath_rw.  The value to the right of the first space 
will replace the stuff at the path.

```
$..something..ssn OBFUSCATE
$..byooroughReport DONTREALLYCARE
```

## Example python usage

```
import json
import obfuscate
file_json = json.loads(open("to_obfuscate.json", "rb").read())
path_configs = obfuscate.read_configs("obfuscation_paths.txt")
clean = obfuscate.obfuscate(file_json, path_configs)
```

## Output

```
{
    "something": [
        {
            "scores": [
                {
                    "customer": {
                        "attributes": {
                            "ssn": "OBFUSCATE"
                        }
                    }
                }
            ]
        }
    ],
    "byooroughReport": "DONTREALLYCARE"
}
```

# The 'nuclear option'

A path config with replacement value of the form:

```
regex___<regex here>___<replacement here> 
```

will do a json.dumps on the stuff at that path (if possible), and then do a regex substitution, and then 
json.loads it back up.

For example, if we use the following config row:

```
$..some_dict.stuff regex___\d\d\d-?\d\d-?\d\d\d\d___SCARYNUMBERS
```

Then this json:

```
{
    "some_dict": {
        "stuff": {
            "over": ["here", "111223333", "hard", "to", "get", {"personalIdent": ["111-22-4444"]}]
        }
    }
}
```

Turns into:

```
{
    "some_dict": {
        "stuff": {
            "over": [
                "here",
                "SCARYNUMBERS",
                "hard",
                "to",
                "get",
                {
                    "personalIdent": [
                        "SCARYNUMBERS"
                    ]
                }
            ]
        }
    }
}
```
