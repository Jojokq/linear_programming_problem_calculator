import numpy as np

from consol_input import data_input

def print_array(array):
    for i in range(len(array)):
        print(array[i], end="\n")

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
                


def find_allowing_element(array, basis_cols, n):
    min_el = 0
    min_el_col_index = 0
    for i in range(len(array[0])):
        if min_el > array[-1][i]:
            min_el = array[-1][i]
            min_el_col_index = i
    if min_el >= 0:
        return 0, -1
    min_el =  array[0][0] / array[0][min_el_col_index] #ДЕЛЕНИЕ НА НОЛЬ ПРОВЕРИТЬ
    min_el_row_index = 0
    for i in range(1, len(array)):
        if array[i][min_el_col_index] != 0:
            temp = array[i][0] / array[i][min_el_col_index]
        if temp > 0 and temp < min_el:
            min_el = temp
            min_el_row_index = i
    if min_el < 0:
        return -1, 0
    el = min_el_row_index + n
    it = basis_cols.index(el)
    basis_cols[it] = min_el_col_index
    return min_el_row_index, min_el_col_index


def happy_end(array, basis_cols, n):
    answer = []
    length = len(array[0])
    for i in range(len(basis_cols)):
        if not (basis_cols[i] >= length - n):
            answer.append(array[i][0])
        else:
            answer.append(0)
    print(f'''    x1 = {answer[0]}    x2 = {answer[1]}    Z = {array[-1][0]}    ''')
    return 0


def calc(array, basis_cols, n):
    row, col = find_allowing_element(array, basis_cols, n)
    while True:
        if row == 0 and col == -1:
            print_array(array)
            return happy_end(array, basis_cols, n)
        elif row == -1 and col == 0:
            print('Система несовместна. Решений нет.')
            return 0
        rectangle_method(array, row, col, basis_cols)
        change_basis(row, col, array)
        row, col = find_allowing_element(array, basis_cols, n)
        
def final_calc():
    #для теста
    #a = [[350, 14, 5, 1, 0, 0], [392, 14, 8, 0, 1, 0], [408, 6, 12, 0, 0, 1], [0, -10, -5, 0, 0, 0]]
    #a = [[12, 3, 1, 1, 0, 0], [12, 1, 3, 0, 1, 0], [7, 2, 0, 0, 0, 1], [0, -2, -3, 0, 0, -5]]
    #b = [3,4,5]
    #c=3
    #basis_cols = [3, 4, 5]
    #результат: 20, 14, 270
    a, b, c = data_input()
    calc(a,b,c)
final_calc()

'''
#-------------ОТЛАДКА
n, m = 3, 3

system_eq = [[350, 14, 5, 1, 0, 0], [392, 14, 8, 0, 1, 0], [408, 6, 12, 0, 0, 1], [0, -10, -5, 0, 0, 0]]
print('список')
print_array(system_eq)

eq_arr = np.array(system_eq, dtype=float)
print('массив')
print(eq_arr)
basis_cols = [3, 4, 5]

print_array(system_eq)
row, col = find_allowing_element(system_eq, basis_cols, n)
print(row)

print(basis_cols)

print('прямоугольник!!!!!!!!!!\n\n\n\n')

rectangle_method(system_eq, row, col, basis_cols)

print_array(change_basis(row, col, system_eq))
#--------------


#------------Вывод--------  
#print('на массиве')
#calc(eq_arr, basis_cols, n)
system_eq = [[350, 14, 5, 1, 0, 0], [392, 14, 8, 0, 1, 0], [408, 6, 12, 0, 0, 1], [0, -10, -5, 0, 0, 0]]
basis_cols = [3, 4, 5]
#print('На списке')
calc(system_eq, basis_cols, n=3)
'''

