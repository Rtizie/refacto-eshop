import json

def getData():
    with open("./app/data/data.json", 'r') as f:
        data = json.load(f)
        print(type(data))
        return data