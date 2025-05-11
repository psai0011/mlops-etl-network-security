import os 
import sys
import json
import pandas as pd
import numpy as np
import pymongo
import certifi
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print("MongoDB URL:", MONGO_DB_URL)

ca = certifi.where()

class NetworkDataExtract:
    def __init__(self):
        try:
            pass  # You can initialize anything if needed later
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def cv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        try:
            self.database = database  # Fix: no comma
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)

            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    FILE_PATH = "Network_Data\phisingData.csv"
    DATABASE = "SAIKIRAN"
    COLLECTION = "NetworkData"

    try:
        networkobj = NetworkDataExtract()
        records = networkobj.cv_to_json_converter(file_path=FILE_PATH)
        print("Sample record:", records[0] if records else "No records found")
        no_of_records = networkobj.insert_data_mongodb(records, DATABASE, COLLECTION)
        print(f"{no_of_records} records inserted into MongoDB.")
    except NetworkSecurityException as ne:
        logging.error(str(ne))
