# ASi17BRrdpweUuMR
from pymongo import MongoClient


def get_database():
    CONNECTION_STRING = "mongodb+srv://igaozasso:ASi17BRrdpweUuMR@swarm.m6anj2k.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING, connect=False)
    return client['CollectiveIntelligence']


dbname = get_database()
