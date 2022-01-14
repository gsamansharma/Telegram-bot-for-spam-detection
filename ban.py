import json


def decreWarnings(user_id, value):
    with open('data.json', 'r+') as file:
        objecct = json.load(file)
        i = objecct[user_id]
        objecct[user_id] = i + value
        file.seek(0)
        json.dump(objecct, file, indent=4)


def getWarnings(user_id):
    file = open('data.json')
    objecct = json.load(file)
    try:
        i = objecct[user_id]

    except:
        with open('data.json', 'r+') as file:
            objecct = json.load(file)
            objecct[user_id] = 3
            print(objecct)
            i = objecct[user_id]
            file.seek(0)
            json.dump(objecct, file, indent=4)

    decreWarnings(user_id, -1)
    return i
