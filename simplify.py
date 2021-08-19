import json
import requests

tokenAndGroupCode = json.load(open("token.json"))
token = tokenAndGroupCode["token"]
groupCode = tokenAndGroupCode["groupCode"]

def getGroupData():
    names = dict()
    url = "https://api.groupme.com/v3/groups/" + groupCode + "?token=" + token
    response = requests.get(url)
    print(response.json())
    for person in response.json()['response']['members']:
        names[person['nickname']] = person['id']
    return names

newNames = set()

# members is currently set up to be a csv of ordering Last Name, First Name, <email (unused)>, phone number
csv = open('members.csv', 'r').read()

for line in csv.split('\n'):
    data = line.split(',')
    if len(data) > 1:
        name = data[1].strip().title() + " " + data[0].strip().title()
        newNames.add((name, data[3].replace(".", "").replace("-", "").replace("(", "").replace(")", "").strip()))

def compareMembers():
    outfile = open("simplified.csv", 'w')
    oldNames = getGroupData()
    # remove old members:
    for name, number in newNames:
        if name not in oldNames.keys():
            outfile.write(name.split(" ")[1] + "," + name.split(" ")[0] + "," + "," + number + "\n")

compareMembers()
