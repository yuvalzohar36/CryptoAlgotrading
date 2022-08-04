import pandas as pd
import json

CONFIGURATION_FILE = "../Configurations/configuration.json"


def write_to_db(doc_ref, data_set):
    doc_ref.set(data_set)


def process_firebase_writing(data_util):
    data_util.lock("process_firebase_writing_sem")
    config = data_util.config
    db = data_util.get_fb_db()
    coins_db = pd.read_csv(config["Paths"]["abs_path"] + config["Paths"]["COINS_DB_PATH"])
    for index, row in coins_db.iterrows():
        doc_ref = db.collection(u'currencies').document(row['Coin'])
        data_set = {'Price': data_util.currency_price(row['Coin']), 'Stability': row['Stability'],
                    "Security": row['Security'], "Scalability": row['Scalability'],
                    "Supply": row['Supply'], "Decentralisation": row['Decentralisation'], "Demand": row['Demand'],
                    "Usefulness": row['Usefulness'], "Backup_Date": row['Backup_Date']}
        write_to_db(doc_ref, data_set)
    data_util.unlock("process_firebase_writing_sem")
