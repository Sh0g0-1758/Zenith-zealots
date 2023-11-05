# Import necessary libraries from Qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram
import numpy as np

# Import the necessary functions for visualizing quantum states
from qiskit.visualization import plot_bloch_multivector

# Import the Statevector class from Qiskit's quantum information module
from qiskit.quantum_info import Statevector
import numpy as np


# def matrix_gen(qubit_location, valid_qubits):
#     # initialise the matrix with all -1
#     matrix = np.full((4, 4), -1)
#
#     # set the qubit locations
#     for qubit in qubit_location:
#         if valid_qubits[qubit]:
#             matrix[qubit_location[qubit][0]][qubit_location[qubit][1]] = qubit
#
#     return matrix

def print_matrix(matrix):
    for i in range(4):
        for j in range(4):
            print(matrix[i][j], end=" ")
        print()
    print()


def left_shift(matrix):
    n = len(matrix)
    # array of length n with 0
    last_loc = np.zeros(n)

    for i in range(n):
        for j in range(n):
            if matrix[i][j] != -1:
                val = matrix[i][j]
                matrix[i][j] = -1
                # shift it to last-loc in that row
                matrix[i][int(last_loc[i])] = val
                last_loc[i] += 1

    return matrix


def right_shift(matrix):
    n = len(matrix)
    # array of length n with (n-1)
    last_loc = np.full(n, n - 1)

    for i in range(n):
        for j in range(n - 1, -1, -1):
            if matrix[i][j] != -1:
                val = matrix[i][j]
                matrix[i][j] = -1
                # shift it to last-loc in that row
                matrix[i][int(last_loc[i])] = val
                last_loc[i] -= 1
    return matrix


def up_shift(matrix):
    n = len(matrix)
    # array of length n with 0
    last_loc = np.zeros(n)

    for i in range(n):
        for j in range(n):
            if matrix[j][i] != -1:
                val = matrix[j][i]
                matrix[j][i] = -1
                # shift it to last-loc in that row
                matrix[int(last_loc[i])][i] = val
                last_loc[i] += 1

    return matrix


def down_shift(matrix):
    n = len(matrix)
    # array of length n with n-1
    last_loc = np.full(n, n - 1)

    for i in range(n):
        for j in range(n - 1, -1, -1):
            print("row: ", j, "col: ", i)
            if matrix[j][i] != -1:
                val = matrix[j][i]
                matrix[j][i] = -1
                # shift it to last-loc in that row
                matrix[last_loc[i]][i] = val
                last_loc[i] -= 1

    return matrix


def shift(matrix, direction):
    if direction == 0:
        return left_shift(matrix)
    elif direction == 1:
        return right_shift(matrix)
    elif direction == 2:
        return up_shift(matrix)
    elif direction == 3:
        return down_shift(matrix)
    else:
        print("Invalid direction")
        return matrix


# def operate_gate(qc_map,qc_loc,qc_matrix, direction, gates):

def merge_left_wall(qc_loc, qc_matrix, state_vector_dict):
    j = 0
    k = 1
    for i in range(len(qc_matrix)):
        if qc_matrix[i][j] == -1 or qc_matrix[i][k] == -1:
            continue
        s1 = state_vector_dict[qc_matrix[i][j]]
        s2 = state_vector_dict[qc_matrix[i][k]]
        if s1 == s2:
            # we will non-wall qubit
            del qc_loc[qc_matrix[i][k]]
            qc_matrix[i][k] = -1

def merge_right_wall(qc_loc, qc_matrix, state_vector_dict):
    j = len(qc_matrix) - 1
    k = len(qc_matrix) - 2
    for i in range(len(qc_matrix)):
        if qc_matrix[i][j] == -1 or qc_matrix[i][k] == -1:
            continue
        s1 = state_vector_dict[qc_matrix[i][j]]
        s2 = state_vector_dict[qc_matrix[i][k]]
        if s1 == s2:
            # we will non-wall qubit
            del qc_loc[qc_matrix[i][k]]
            qc_matrix[i][k] = -1

def merge_up_wall(qc_loc, qc_matrix, state_vector_dict):
    j = 0
    k = 1
    for i in range(len(qc_matrix)):
        if qc_matrix[j][i] == -1 or qc_matrix[k][i] == -1:
            continue
        s1 = state_vector_dict[qc_matrix[j][i]]
        s2 = state_vector_dict[qc_matrix[k][i]]
        if s1 == s2:
            # we will non-wall qubit
            del qc_loc[qc_matrix[k][i]]
            qc_matrix[k][i] = -1

def merge_down_wall(qc_loc, qc_matrix, state_vector_dict):
    j = len(qc_matrix) - 1
    k = len(qc_matrix) - 2
    for i in range(len(qc_matrix)):
        if qc_matrix[j][i] == -1 or qc_matrix[k][i] == -1:
            continue
        s1 = state_vector_dict[qc_matrix[j][i]]
        s2 = state_vector_dict[qc_matrix[k][i]]
        if s1 == s2:
            # we will non-wall qubit
            del qc_loc[qc_matrix[k][i]]
            qc_matrix[k][i] = -1


def merge(qc_map, qc_loc, qc_matrix, curr_dir, state_vector_dict):
    # first we update the state vector
    for i in range(len(qc_map)):
        state_vector_dict[i] = Statevector(qc_map[i])

    # now depending on the direction we will iterate the wall and compare their state vectors and if same we will
    # destroy the non-wall qubit
    if curr_dir == 0:
        merge_left_wall(qc_loc, qc_matrix, state_vector_dict)
    elif curr_dir == 1:
        merge_right_wall(qc_loc, qc_matrix, state_vector_dict)
    elif curr_dir == 2:
        merge_up_wall(qc_loc, qc_matrix, state_vector_dict)
    elif curr_dir == 3:
        merge_down_wall(qc_loc, qc_matrix, state_vector_dict)
    else:
        print("Invalid direction")

def matrix_gen(qubit_location):
    # initialise the matrix with all -1
    matrix = np.full((4, 4), -1)

    # set the qubit locations
    for qubit in qubit_location:
        matrix[qubit_location[qubit][0]][qubit_location[qubit][1]] = qubit

    return matrix

def operate_gate(qc_map, qc_i,dir,gate):
    gate = gate[dir]
    if gate == 'H':
        qc_map[qc_i].h(0)
    elif gate == 'X':
        qc_map[qc_i].x(0)
    elif gate == 'I':
        qc_map[qc_i].i(0)
    elif gate == 'Z':
        qc_map[qc_i].z(0)
    else:
        print("Invalid gate")


def gate_op(curr_dir, qc_map, qc_location, qc_matrix, wall_gate):

    # now we will operate the gates
    for i in range(len(qc_map)):
        if curr_dir == 0:
            # left
            if qc_matrix[i][0] != -1:
                operate_gate(qc_map, qc_matrix[i][0], curr_dir, wall_gate)
        elif curr_dir == 1:
            # right
            if qc_matrix[i][len(qc_matrix) - 1] != -1:
                operate_gate(qc_map, qc_matrix[i][len(qc_matrix) - 1], curr_dir, wall_gate)
        elif curr_dir == 2:
            # up
            if qc_matrix[0][i] != -1:
                operate_gate(qc_map, qc_matrix[0][i], curr_dir, wall_gate)
        elif curr_dir == 3:
            # down
            if qc_matrix[len(qc_matrix) - 1][i] != -1:
                operate_gate(qc_map, qc_matrix[len(qc_matrix) - 1][i], curr_dir, wall_gate)
        else:
            print("Invalid direction")

    qc_matrix = matrix_gen(qc_location)