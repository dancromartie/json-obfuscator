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
