#!/usr/bin/env python

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def init_matrix(n):
    return [[0 for i in range(n)] for i in range(n)]

def print_matrix(matrix):
    mat_len = len(matrix)
    for i in range(mat_len):
        print(bcolors.BOLD + bcolors.YELLOW + str(matrix[i]) + bcolors.ENDC)
    print("\n")

def rotate_matrix(matrix, time):
    print(bcolors.BOLD + bcolors.RED + "# Original matrix" + bcolors.ENDC)
    print_matrix(matrix)

    print(bcolors.BOLD + bcolors.RED + "# After rotate %d times" % time + bcolors.ENDC)
    mat_len = len(matrix)
    if time >= mat_len:
        # If number of rotate is equal to length of matrix,
        # the matrix is same.
        time = time % mat_len
        if time == 0:
            print_matrix(matrix)
            exit(0)

    for head in range(time):
        # Get column
        col = [matrix[i][head] for i in range(mat_len)]
        shift = [matrix[i][head+1] for i in range(mat_len)]
        for i in range(mat_len):
            matrix[i][head] = shift[i]
            matrix[i][head+1] = col[i]
    print_matrix(matrix)

# app test
# Test 1
N = 3
M = 3
K = 10

mat = init_matrix(3)

mat[0][0] = 12
mat[0][1] = 23
mat[0][2] = 34

mat[1][0] = 56
mat[1][1] = 67
mat[1][2] = 45

mat[2][0] = 78
mat[2][1] = 89
mat[2][2] = 91

rotate_matrix(mat, K)

n = 2
m = 2
k = 2

# Test 2
mat_ = init_matrix(2)
mat_[0][0] = 1
mat_[0][1] = 2
mat_[1][0] = 3
mat_[1][1] = 4

rotate_matrix(mat_, k)