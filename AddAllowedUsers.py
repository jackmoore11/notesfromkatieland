import json
from notesfromkatieland import createApp, db
from notesfromkatieland.models import AllowedUser

app = createApp()
app.app_context().push()
db.create_all()

currentAllowedUsers = AllowedUser.query.all()
currentEmails = []
for allowedUser in currentAllowedUsers:
    currentEmails.append(allowedUser.email)

f = open('AllowedUsers.json')
userData = json.load(f)
f.close()

for name, info in userData.items():
    if str.lower(info[0]) not in currentEmails:
        allowedUser = AllowedUser(name=name, email=str.lower(info[0]), placeDefault=info[1])
        db.session.add(allowedUser)
        print(f'Added {name} to database.')
    else:
        allowedUser = AllowedUser.query.filter_by(email=str.lower(info[0])).first()
        allowedUser.placeDefault = info[1]
        print(f'{name} already in database. Updated location.')

db.session.commit()