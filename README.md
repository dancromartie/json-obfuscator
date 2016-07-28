# json-obfuscator

## Dependencies

pip install jsonpath-rw, see https://github.com/kennknowles/python-jsonpath-rw

## Example input

```
{
    "something": [{
        "scores": [{
            "customer": {"attributes": {"ssn": "494949494"}}
        }] 
    }],
    "big_report": {
        "im": {
            "over": ["here", "im", "hard", "to", "get", {"to": ["111-22-4444"]}]
        }
    },
    "some_dict": {
        "stuff": {
            "over": ["here", 111223333, "hard", "to", "get", {"personalIdent": ["111-22-4444"]}]
        },
        "keep_part_of_me": "12345xxxx"
    }
}
```

## Example python usage

```
import json
import jsonobfuscator
import re

file_json = json.loads(open("to_obfuscate_example.json", "rb").read())

path_configs = []
path_configs.append({"path": "$..keep_part_of_me", "regex": "\d\d\d\d\dxxxx", "replace": "0000xxxx"})
path_configs.append({"path": "$..some_dict.stuff", "regex": "\d\d\d-?\d\d-?\d\d\d\d", "replace": "999999999"})
path_configs.append({"path": "$..big_report", "func": lambda x, y: "i_dont_care"})
path_configs.append({"path": "$..ssn", "func": lambda x, y: re.sub('[0-4]', '5', y)})


print "\nScrubbing this JSON: %s" % file_json
print "\nScrubbing with paths: %s" % path_configs
print "\nScrubbed JSON is: %s" % json.dumps(jsonobfuscator.obfuscate(file_json, path_configs), indent=4)
```

The lambda functions are functions that take a first argument of the original json object that you 
are obfuscating.  The second argument is the value found at the path.  This can be useful if you 
need to obfuscate depending on the details of the entire json object.

## Output

```
{
    "some_dict": {
        "keep_part_of_me": "0000xxxx",
        "stuff": {
            "over": [
                "here",
                999999999,
                "hard",
                "to",
                "get",
                {
                    "personalIdent": [
                        "999999999"
                    ]
                }
            ]
        }
    },
    "something": [
        {
            "scores": [
                {
                    "customer": {
                        "attributes": {
                            "ssn": "595959595"
                        }
                    }
                }
            ]
        }
    ],
    "big_report": "i_dont_care"
}
```

