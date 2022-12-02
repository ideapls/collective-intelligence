from connection import get_database


dbname = get_database()
collection_name = dbname["Order"]

"""order = {
    "weight": 14,
    "number": 0,
    "items": ["hamburger", "milkshake"]
}"""

#collection_name.insert_one(order)


def insert_order(weight, items):
    order = {
        "weight": weight,
        "items": items
    }

    collection_name.insert_one(order)
