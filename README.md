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
    "byooroughReport": {
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
import jsonobfuscate
import re

file_json = json.loads(open("to_obfuscate_example.json", "rb").read())

path_configs = []
path_configs.append({"path": "$..keep_part_of_me", "regex": "\d\d\d\d\dxxxx", "replace": "0000xxxx"})
path_configs.append({"path": "$..some_dict.stuff", "regex": "\d\d\d-?\d\d-?\d\d\d\d", "replace": "999999999"})
path_configs.append({"path": "$..byooroughReport", "func": lambda x: "I_DONT_CARE"})
path_configs.append({"path": "$..ssn", "func": lambda x: re.sub('[0-4]', '5', x)})


print "\nScrubbing this JSON: %s" % file_json
print "\nScrubbing with paths: %s" % path_configs
print "\nScrubbed JSON is: %s" % json.dumps(jsonobfuscate.obfuscate(file_json, path_configs), indent=4)
```

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
    "byooroughReport": "I_DONT_CARE"
}
```

