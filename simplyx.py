import numpy as np
import csv
from consol_input import data_input
from table_import import import_table

EPSILON = 0.00005

def print_array(array):
    for i in range(len(array)):
        print(array[i], end="\n")
    print()

def change_basis(row, col, array):
    r_el = array[row][col]
    for i in range(len(array[0])):
        array[row][i] = array[row][i] / r_el
    for j in range(len(array)):
        if j == row:
            continue
        array[j][col] = 0
    return array


def rectangle_method(arr,  a_row, a_col, basis_cols):
    a_el = arr[a_row][a_col]
    for row in range(len(arr)):
        for col in range(len(arr[0])):
            if (not (col in basis_cols)) and row != a_row:
                arr[row][col] = arr[row][col] - arr[row][a_col] * arr[a_row][col] / a_el
                


def find_allowing_element(array, basis_cols, n, number_of_variables, target_function_row_number = -1):
    #seeking for col
    min_el = 0
    min_el_col_index = 1
    for i in range(1, number_of_variables + 1): 
        if min_el > array[target_function_row_number][i]:
            min_el = array[target_function_row_number][i]
            min_el_col_index = i
    if min_el >= 0:
        return 0, -1
    #seeking for row
    min_el =  array[0][0] / array[0][min_el_col_index] 
    min_el_row_index = 0
    for i in range(1, n):
        if array[i][min_el_col_index] != 0:
            temp = array[i][0] / array[i][min_el_col_index]
            if temp > 0 and temp < min_el:
                min_el = temp
                min_el_row_index = i
    if min_el < 0:
        return -1, 0
    #updating basis
    update_basis(basis_cols, min_el_row_index, min_el_col_index)
    rectangle_method(array, min_el_row_index, min_el_col_index, basis_cols)
    change_basis(min_el_row_index, min_el_col_index, array)
    '''print(basis_cols)
    el = min_el_row_index + number_of_variables + 1
    it = basis_cols.index(el)
    basis_cols[it] = min_el_col_index'''
    #returning row/col indexes of allowing element
    return min_el_row_index, min_el_col_index


def update_basis(basis_cols, new_row, new_col):
    basis_cols[new_row] = new_col

def answer_print(array, basis_cols, n): #REDO WITH ANY BASIS !!!!!!!!!!!!!!!!!!!!!!!!!!
    answer = []
    length = len(array[0])
    for i in range(len(basis_cols)):
        if not (basis_cols[i] >= length - n):
            answer.append(array[i][0])
        else:
            answer.append(0)
    print(f'''    x1 = {answer[0]}    x2 = {answer[1]}    Z = {array[-1][0]}    ''')
    return 0


def check_Mrow_target(array, n):
    for i in range(0, len(array)-n+1):
        if abs(array[-2][i]) > EPSILON:
            return 1
    return 0

def calc(array, basis_cols, n, m    ):
    if check_Mrow_target(array, n) == 0:
        row, col = find_allowing_element(array, basis_cols, n, m)
    else:
        row, col = find_allowing_element(array, basis_cols, n, m,  -2)
    while check_Mrow_target(array, n):
        print_array(array)
        if row == -1 and col == 0:
            print('Система несовместна. Решений нет.')
            return 0
        #rectangle_method(array, row, col, basis_cols)
        #change_basis(row, col, array)
        row, col = find_allowing_element(array, basis_cols, n, m,  -2)
    print(basis_cols)
    print_array(array)
    print('phase 2')
    #update_basis(basis_cols, row, col)
    while True:
        print_array(array)
        row, col = find_allowing_element(array, basis_cols, n, m)
        print(row, '   ',col,'\n')
        if row == 0 and col == -1:
            print(basis_cols)
            print_array(array)
            return answer_print(array, basis_cols, n)
        elif row == -1 and col == 0:
            print('Система несовместна. Решений нет.')
            return 0
        #rectangle_method(array, row, col, basis_cols)
        #change_basis(row, col, array)
        

def final_calc():
    
    arr = []
    a, b, c = import_table()
    calc(a,b,c, len(a[0] - 1 - len(b))) #ДОБАВИТЬ d=число переменных!!!!!!!!!
    '''
    #для теста
    #a = [[225, 5, 3, -1, 0, 0, 1, 0, 0], [150, 2.5, 3, 0, -1, 0, 0, 1, 0], [80, 1, 1.3, 0, 0, -1, 0, 0, 1],
    #      [-455, -8.5, -7.3, 1, 1, 1, 0, 0, 0], [0, 5, 2, 0, 0, 0, 0, 0, 0]] # Таблица для метода искусственного базиса
    a = [[225, 2, 2, 0, 1, 0, 1, 0, 0], [10, 1, 0, 1, 0, 0, 0, 1, 0],[5, 0, 6, -1, 0, -1, 0, 0, 1], 
         [-15, -1, -6, 0, 0, 1, 0, 0, 0], [0, 11, -6, 0, 0, 0, 0, 0, 0]]
    a = [[5, 2, 1, 1, 1, 3, 1, 0, 0 ], [7, 3, 2, 0, -1, 6, 0, 1, 0], [2, 1, 0, -1, 2, 1, 0, 0, 1], [-14, -6, -3, 0, -2, -10, 0, 0, 0], [0, 0, 0, 3, -2, -1, 0, 0, 0]]
    b = [6,7,8] #базисные столбцы
    c = 3 #число уравнений
    d = 5 #число переменных
    #basis_cols = [3, 4, 5]
    #результат: 20, 14, 270'''
