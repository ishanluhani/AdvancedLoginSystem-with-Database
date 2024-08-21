import json
import os


def addUser(email, password):
    email = email.lower()
    dataDict = {'Email': email, 'Password': password,
                'Subjects': {'English': {'Introduction': {'Questions': ['Welcome'], 'Status': 'Pending'} },
                            'Science': {'Introduction': {'Work': ['Welcome'], 'Status': 'Pending'}} }
                }

    with open(f"RegisteredEmails/{email}.json", "w") as outfile:
        json.dump(dataDict, outfile, indent=4)

    return dataDict

def checkUserExists(email):
    data = os.listdir('RegisteredEmails')
    data = list(map(lambda x: x.strip('.json'), data))
    return email in data

def loginUser(email, password):
    database = os.listdir('RegisteredEmails')
    personData = None
    for file in database:
        filePath = os.path.join('RegisteredEmails', file)
        fileData = json.load(open(filePath))
        if fileData['Email'] == email and fileData['Password'] == password:
            personData = fileData
    return personData
