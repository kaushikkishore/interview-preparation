"""
Machine coding 


Requirement
Design and implement a program that can merge multiple JSON configuration files into a single consolidated output file. 
The program should take two or more JSON files as input and produce a merged JSON file as output. When merging, values from later files should override corresponding 
values from earlier files. 

For lists of items that have a 'name' field, items with the same name should be merged rather than replaced entirely. 

The program should handle nested structures and preserve all fields from input files unless explicitly overridden by later files.


// local.json
{
  "environment": "local",
  "deployments": [
    {
      "name": "hello-universe-d1",
      "image": "d1:v1.0.0",
      "tags": {
        "app": "hello-universe"
      }
    },
    {
      "name": "hello-universe-d2",
      "image": "d2:v3.2.1-beta",
      "tags": {
        "app": "hello-universe"
      }
    }
  ]
}


// production.json
{
  "environment": "production",
  "deployments": [
    {
      "name": "hello-universe-d1",
      "tags": {
        "env": "production"
      }
    },
    {
      "name": "hello-universe-d2",
      "image": "d2:v3.2.1"
    }
  ]
}


// final json
{
  "environment": "production",
  "deployments": [
    {
      "name": "hello-universe-d1",
      "image": "d1:v1.0.0",
      "tags": {
        "app": "hello-universe",
        "env": "production"
      }
    },
    {
      "name": "hello-universe-d2",
      "image": "d2:v3.2.1",
      "tags": {
        "app": "hello-universe"
      }
    }
  ]
}

{'environment': 'production', 'deployments': [{'name': 'hello-universe-d1', 'image': 'd1:v1.0.0', 'tags': {'app': 'hello-universe', 'env': 'production'}}, {'name': 'hello-universe-d2', 'image': 'd2:v3.2.1', 'tags': {'app': 'hello-universe'}}]}


"""


"""
Solution 

# deep_merge 
- recursively merge the items 
- build a dict - value are there - then overrride 
- Mkae a check if the name is key then merge 
- Override will take precedence 
- merged files - new file 
- local.json 
- production.json 
- empty new {}
- 

Error case 
- file not found one 
- Invalid json 
- memory limiting with large files. - small files. 

"""



def deep_merge(base, override):
    # print(f"base {base} override {override}")
    if not isinstance(base, dict) or not isinstance(override, dict):
        if isinstance(base, list) and isinstance(override, list):
            # Check the name fields 

            if (all ('name' in item for item in base if isinstance(item, dict)) 
            and all ('name' in item for item in override if isinstance(item, dict))):
                # merging 
                result_dict = { item['name']: item for item in base if isinstance(item, dict)}
                # { 'hello-universe-d1': {entire-obj} }
                for item in override:
                    if isinstance(item, dict) and 'name' in item:
                        name = item['name']
                        if name in result_dict:
                            result_dict[name]= deep_merge(result_dict[name], item)
                    else:
                        # new item add 
                        result_dict[name]= item
                return list(result_dict.values())
            else:
                return override
        else:
            return override

    result = base.copy()
    # overrides
    for key, value in override.items():
        if key in result:
            # merge recursively
            result[key] = deep_merge(result[key], value)
        else:
            # new keys 
            result[key] = value
    return result 

                    




if __name__ == "__main__":
    local = {
    "environment": "local",
    "deployments": [
        {
        "name": "hello-universe-d1",
        "image": "d1:v1.0.0",
        "tags": {
            "app": "hello-universe"
        }
        },
        {
        "name": "hello-universe-d2",
        "image": "d2:v3.2.1-beta",
        "tags": {
            "app": "hello-universe"
        }
        }
    ]
    }

    production = {
    "environment": "production",
    "deployments": [
        {
        "name": "hello-universe-d1",
        "tags": {
            "env": "production"
        }
        },
        {
        "name": "hello-universe-d2",
        "image": "d2:v3.2.1"
        }
    ]
    }
    production2 = {
    "environment": "production",
    "deployments": [
        {
        "name": "hello-universe-d1",
        "tags": {
            "env": "production"
        }
        },
        {
        "name": "hello-universe-d2",
        "image": "d2:v3.2.1"
        }
    ]
    }


    result = deep_merge(local, production)
    result2 = deep_merge(result, production2)

    print(result2)