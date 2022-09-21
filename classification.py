from enum import Enum
from queue import Queue


class Order:
    def __init__(self, weight=0, number=0, items=[]):
        self.weight = weight
        self.number = number
        self.items = items


weights = [1, 2, 3, 5, 8]
itemsDict = {'hamburger': weights[4], 'milkshake': weights[2], 'batata': weights[3]}
digit_key = ""
count = 0
while digit_key != "sai":
    order = Order()
    digit_key = input("Digite o nome do item: ")
    if digit_key == "sai":
        count += 1
        break
    if digit_key in itemsDict:
        order.items.append(itemsDict.get(digit_key))
        print(order.items)
    else:
        print('Item inválido!')


def weight_sums(items_list):
    summation = sum(items_list)
    order.weight = summation
    return summation


print("Resultado: " + str(weight_sums(order.items)))
