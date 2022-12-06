from connection import get_database


dbname = get_database()
collection_name = dbname["Order"]


def insert_order(weight, items):
    order = {
        "weight": weight,
        "items": items
    }

    collection_name.insert_one(order)


def get_orders():
    documents = collection_name.find()
    return list(documents)
