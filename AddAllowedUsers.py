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

for name, email in userData.items():
    if email not in currentEmails:
        allowedUser = AllowedUser(name=name, email=email)
        db.session.add(allowedUser)
        print(f'Added {name} to database')
    else:
        print(f'{name} already in database')

db.session.commit()