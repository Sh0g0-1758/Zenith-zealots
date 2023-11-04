# Import necessary libraries from Qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram
import numpy as np

# Import the necessary functions for visualizing quantum states
from qiskit.visualization import plot_bloch_multivector

# Import the State vector class from Qiskit's quantum information module
from qiskit.quantum_info import Statevector
import numpy as np
import random
# import helper functions
from HelperFunctions import *
import json

# Few instructions

# wall_gate = {
#     0: 'H',
#     1: 'X',
#     2: 'I',
#     3: 'Z'
# }

# For Direction
# 0 - Left
# 1 - Right
# 2 - Up
# 3 - Down

def process(qc_map, qc_loc, qc_matrix, dir, gates, state_vector):
    # first we will shift the matrix
    shift(qc_matrix, dir)

    # now we will operate the gates
    gate_op(dir, qc_map, qc_loc, qc_matrix, gates)

    # now we will merge the qubits
    merge(qc_map, qc_loc, qc_matrix, dir, state_vector)

    shift(qc_matrix, dir)


LevelInfo = json.load(open("levels.json", "r"))

# Designing Level 1

wall_gate = {
    0: 'H',
    1: 'X',
    2: 'I',
    3: 'Z'
}

Legend = {
    "shogo": "Statevector([0.70710678+0.j, 0.70710678+0.j],dims=(2,))",
    "Sam": "Statevector([0.70710678+0.j, -0.70710678+0.j],dims=(2,))",
    "Parv": "Statevector([1.+0.j, 0.+0.j],dims=(2,))",
    "Veet": "Statevector([0.+0.j, 1.+0.j],dims=(2,))",
    "TunTunMausi": "Statevector([0.+0.j, -1.+0.j],dims=(2,))"
}

q_circuts = {}
q_location = {}

number_of_q_circuits = LevelInfo["Levels"]["Info"][0]["Qubits"]["number"]

for _ in range(number_of_q_circuits):
    q = QuantumCircuit(1)
    gates = LevelInfo["Levels"]["Info"][0]["Qubits"]["Info"][_]["Gates"]
    q_location[_] = LevelInfo["Levels"]["Info"][0]["Qubits"]["Info"][_]["Location"]
    for n_ in gates:
        print(n_)
        if n_ == 'h':
            q.h(0)
        elif n_ == 'x':
            q.x(0)
        elif n_ == 'z':
            q.z(0)
    q_circuts[_] = q


# qc1 = QuantumCircuit(1)
# qc2 = QuantumCircuit(1)

# qc1.h(0)  # Hadamard Gate on qubit |+>
# qc1.z(0)  # Setting the initial state to |->
# qc2.x(0)  # Setting the initial state to |1>

# create a map of quantum circuits
# qc_map = {
#     0: qc1,
#     1: qc2
# }

# now set location of these qubits

# qc_location = {
#     0: [1, 1],
#     1: [1, 3]
# }

# valid_qc = [True, True]

# now generate the matrix
location_matrix = matrix_gen(q_location)

# let's see the matrix
print(location_matrix)
# the shift operation is ready

# creating a state-vector dictionary
state_vector_dict = {}
for _ in range(number_of_q_circuits):
    state_vector_dict[_] = Statevector(q_circuts[_])
# state_vector_dict[0] = Statevector(qc_map[0])
# state_vector_dict[1] = Statevector(qc_map[1])

print(state_vector_dict[0])
print(state_vector_dict[1])

qc_map = {}

for _ in range(number_of_q_circuits):
    qc_map[_] = q_circuts[_]

process(qc_map, q_location, location_matrix, 3, wall_gate, state_vector_dict)

# wall_gate = {
#     0: 'H',
#     1: 'X',
#     2: 'I',
#     3: 'Z'
# }

# qc1.h(0)  # Hadamard Gate on qubit |+>
# qc2.x(0)  # Setting the initial state to |1>

# qc1_test = qc_map[0]
# qc1_test.draw(output='mpl')

print(location_matrix)

print(state_vector_dict[0])
print(state_vector_dict[1])