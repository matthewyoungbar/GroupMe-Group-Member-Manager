import requests
import json
'''
Command line equivalent of add command:
curl -X POST -H "Content-Type: application/json" -d '{"members": [{"nickname": "Person","phone_number": "+1 9999999999","guid": "GUID-1"}]}' "https://api.groupme.com/v3/groups/69606616/members/add?token=<TOKEN>"
'''

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

def removeOldMembers():
    oldNames = getGroupData()
    # remove old members:
    for name in oldNames.keys():
        if name not in newNames:
            url = "https://api.groupme.com/v3/groups/" + groupCode + "/members/" + oldNames[name] + "/remove?token=" + token
            x = requests.post(url, headers = {"Content-Type": "application/json"})
            print("Removed", name)
            print(x.text)


userData = {"members": []}

newNames = set()

csv = open('simplified.csv', 'r').read()

for line in csv.split('\n'):
    data = line.split(',')
    if len(data) > 1:
        user = dict()
        name = data[1].strip().title() + " " + data[0].strip().title()
        user["nickname"] = name
        newNames.add(name)
        user["phone_number"] = data[3].replace(".", "").replace("-", "").replace("(", "").replace(")", "").strip()
        userData["members"].append(user)

url = "https://api.groupme.com/v3/groups/" + groupCode + "/members/add?token=" + token

x = requests.post(url, headers = {"Content-Type": "application/json"}, data=json.dumps(userData))
print(x.text)
