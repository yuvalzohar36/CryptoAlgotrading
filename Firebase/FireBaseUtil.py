import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import json

CONFIGURATION_FILE = "../Configurations/configuration.json"


def init_FB(credentials_full_path):
    cred = credentials.Certificate(credentials_full_path)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db


def write_to_db(doc_ref, data_set):
    doc_ref.set(data_set)


def process_firebase_writing():
    with open(CONFIGURATION_FILE) as config_file:
        config = json.load(config_file)
    db = init_FB(config["Paths"]["abs_path"] + config["Paths"]["FIREBASE_CREDENTIALS"])
    coins_db = pd.read_csv(config["Paths"]["abs_path"] + config["Paths"]["COINS_DB_PATH"])
    for index, row in coins_db.iterrows():
        doc_ref = db.collection(u'currencies').document(row['Coin'])
        data_set = {'Stability': row['Stability'], "Security": row['Security'], "Scalability": row['Scalability'],
                    "Supply": row['Supply'], "Decentralisation": row['Decentralisation'], "Demand": row['Demand'],
                    "Usefulness": row['Usefulness'], "Backup_Date": row['Backup_Date']}
        write_to_db(doc_ref, data_set)


process_firebase_writing()
