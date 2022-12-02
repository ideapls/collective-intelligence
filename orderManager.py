from dataManager import insert_order


class Order:
    def __init__(self, weights=[], items=[], total_weight=0):
        self.weights = weights
        self.items = items
        self.total_weight = total_weight


itemsDict = {'hamburger': 4, 'milkshake': 2, 'batata': 3}
digit_key = ""
count = 0
while digit_key != "sai":
    order = Order()
    digit_key = input("Digite o nome do item: ")
    if digit_key == "sai":
        count += 1
        break
    if digit_key in itemsDict.keys():
        order.items.append(digit_key)
        order.weights.append(itemsDict[digit_key])
        print(order.items)
        print(order.weights)
    else:
        print('Item inválido!')

order.total_weight = sum(order.weights)
print(f"Peso considerado: {order.total_weight}")
insert_order(order.total_weight, order.items)
