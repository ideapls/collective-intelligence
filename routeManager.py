import threading
from threading import Thread
from time import sleep
import csv
from math import sqrt
from status import Status

board = open("data/map.csv")
file = csv.reader(board)
node_list = list(file)

HOME = (3, 3)
COL = int(node_list[0][0])
ROW = int(node_list[0][1])
matrix = node_list[1:]
threads = []
lock = threading.Lock()


class Drone:
    def __init__(self, id, availability=Status.AVAILABLE.name, localization=HOME):
        self.id = id
        self.availability = availability
        self.localization = localization

    def change_status_to_delivering(self):
        self.availability = Status.DELIVERING.name

    def change_status_to_backing(self):
        self.availability = Status.BACKING.name

    def report(self):
        print("=====================================\n")
        print("Status do drone:\n")
        print("Identificador: " + str(self.id))
        print("Status: " + str(self.availability))
        print("Localização: " + str(self.localization) + "\n")

    def flight(self, matrix, localization):
        navigate(self, matrix, localization)


drone1 = Drone(1)
drone2 = Drone(2)

for b in matrix:
    print(*b)


def find_positions(matrix, COL, ROW, value):
    positions = []
    for i in range(0, COL):
        for j in range(0, ROW):
            if matrix[i][j] == value:
                positions.append((i, j))
    return positions


def navigate(drone, matrix, localization):
    agent = ''
    i = localization[0]
    j = localization[1]
    if drone.id == 1:
        agent = '-'
    elif drone.id == 2:
        agent = '+'
    matrix[i][j] = agent
    lock.acquire()
    for m in matrix:
        print(*m)
    print("\n")
    lock.release()


def find_neighbors(matrix, COL, ROW, current_position):
    i = current_position[0]
    j = current_position[1]
    neighbors = []
    if i > 0 and matrix[i - 1][j] != '2':  # Cima
        neighbors.append((i - 1, j))
    if i + 1 < COL and matrix[i + 1][j] != '2':  # Baixo
        neighbors.append((i + 1, j))
    if j > 0 and matrix[i][j - 1] != '2':  # Esquerda
        neighbors.append((i, j - 1))
    if j + 1 < ROW and matrix[i][j + 1] != '2':  # Direita
        neighbors.append((i, j + 1))
    return neighbors


def find_better_state(fringe, state_heuristic):
    most_promising_value = 1000000000
    most_promising_index = 0
    index = 0
    for state in fringe:
        if state_heuristic[state] < most_promising_value:
            most_promising_state = state
            most_promising_value = state_heuristic[most_promising_state]
            most_promising_index = index
        index = index + 1
    return most_promising_index


def meta_heuristic(state, final_states):
    x = state[0]
    y = state[1]
    distancia_minima = 1000000000

    for final_state in final_states:
        x_final_state = final_state[0]
        y_final_state = final_state[1]
        diff1 = x_final_state - x
        diff2 = y_final_state - y
        soma_diffs = pow(diff1, 2) + pow(diff2, 2)
        distancia_atual = sqrt(soma_diffs)
        if distancia_atual < distancia_minima:
            distancia_minima = distancia_atual
    return distancia_minima


def presents_solution(state, predecessors, iteration, drone):
    path = [state]
    print("Entrega realizada com " + str(iteration) + " ações.")
    while predecessors[state] is not None:
        path.append(predecessors[state])
        state = predecessors[state]
    path = path[::-1]
    for p in path:
        drone.flight(matrix, p)
        sleep(3)
    print(path)


def a_star_pathfinding(matrix, COL, ROW, initial_state, final_states, drone):
    meta_distance = {}
    travelled_distance = {}
    heuristic = {}
    predecessors = {}
    expanded_states = []
    solution_found = False

    travelled_distance[initial_state] = 0
    meta_distance[initial_state] = meta_heuristic(initial_state, final_states)
    heuristic[initial_state] = travelled_distance[initial_state] + meta_distance[initial_state]
    predecessors[initial_state] = None
    print("Heuristica da Distancia no Estado Inicial: " + str(heuristic[initial_state]))
    fringe = []
    fringe.append(initial_state)
    iteration = 1
    if initial_state != HOME:
        drone.change_status_to_backing()
    elif initial_state == HOME:
        drone.change_status_to_delivering()
    while len(fringe) != 0:
        most_promising_index = find_better_state(fringe, heuristic)
        state = fringe.pop(most_promising_index)
        drone.localization = state
        drone.report()
        if state in final_states:
            solution_found = True
            break
        successor_states = find_neighbors(matrix, COL, ROW, state)
        expanded_states.append(state)
        for i in range(0, len(successor_states)):
            successor = successor_states[i]
            if successor not in expanded_states and successor not in fringe:
                fringe.append(successor)
                if successor not in heuristic.keys():
                    meta_distance[successor] = meta_heuristic(successor, final_states)
                    travelled_distance[successor] = travelled_distance[state] + 1
                    heuristic[successor] = meta_distance[successor] + travelled_distance[successor]
                    predecessors[successor] = state
        iteration = iteration + 1

    if solution_found:
        presents_solution(state, predecessors, iteration, drone)
    else:
        print("Rota não encontrada")


def d1(lock):
    initial_state = find_positions(matrix, COL, ROW, 'i')
    final_states = find_positions(matrix, COL, ROW, '0')
    a_star_pathfinding(matrix, COL, ROW, initial_state[0], final_states, drone1)
    lock.acquire()
    a_star_pathfinding(matrix, COL, ROW, final_states[0], initial_state, drone1)
    lock.release()
    sleep(3)


def d2(lock):
    initial_state = find_positions(matrix, COL, ROW, 'i')
    final_states = find_positions(matrix, COL, ROW, '4')
    a_star_pathfinding(matrix, COL, ROW, initial_state[0], final_states, drone2)
    lock.acquire()
    a_star_pathfinding(matrix, COL, ROW, final_states[0], initial_state, drone2)
    lock.release()
    sleep(3)


td1 = Thread(target=d1, args=(lock,))
td2 = Thread(target=d2, args=(lock,))

threads.append(td1)
threads.append(td2)


def thread_controller(threads):
    for thread in threads:
        if not thread.is_alive():
            thread.start()

    for thread in threads:
        thread.join()


thread_controller(threads)

print()

for m in matrix:
    print(*m)
