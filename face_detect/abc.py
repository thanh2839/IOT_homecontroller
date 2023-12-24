import firebase_admin
from firebase_admin import db, credentials

cred = credentials.Certificate('credentials.json')
firebase_admin.initialize_app(cred, {"databaseURL":"https://btl-iot-27a9c-default-rtdb.asia-southeast1.firebasedatabase.app/"})
ref = db.reference('/btl-iot/face-detect').get()
db.reference('/btl-iot').update({"face-detect": True})
print(ref)