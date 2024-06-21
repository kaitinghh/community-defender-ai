import json

def text_to_json(text):
    lines = text.strip().split("\n")

    data = {"Name": "Unknown", "Address": "Unknown"}

    for line in lines:
        key, value = line.split(":", 1)
        data[key.strip().lower()] = value.strip()
    json_data = json.dumps(data, indent=4)
    
    return json_data