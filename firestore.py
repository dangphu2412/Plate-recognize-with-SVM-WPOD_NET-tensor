import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('./serviceAccount.json')
default_app = firebase_admin.initialize_app(cred)

def addToDB(cmnd, name, money, plate):
    try:
        db = firestore.client()

        doc_ref = db.collection(u'users').document(plate)

        doc_ref.set({
            u'cmnd': cmnd,
            u'name': name,
            u'money': money
        })
    except Exception:
        raise Exception('There was an error in adding to database')

def updateDB(plate, moneyBack, status):
    try:
        db = firestore.client()

        doc_ref = db.collection(u'users').document(plate)

        doc_ref.update({
            u'money': moneyBack,
            u'status': not status
        })
    except Exception:
        raise Exception('There was an error in adding to database')

def getInfoByPlate(plate):
    db = firestore.client()
    doc_ref = db.collection(u'users').document(plate)

    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return False

def getAllInfoPlate():
    try:
        results = []
        db = firestore.client()
        docs = db.collection(u'users').stream()

        for doc in docs:
            results.append(doc.to_dict())
        return results
    except Exception:
        return ''