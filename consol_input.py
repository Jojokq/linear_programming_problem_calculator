import numpy as np

def data_input():
    print('Введите через пробел число уравнений системы и' + '\n' +'число коэфффициентов в уравнении, включая ' + '\n' + 'свободный член')
    n = int(input()) #Число уравнений в системе
    m = int(input()) #Число чисел при переменных + свободная переменная eg: 14 *x1+ 5 *x2 = 350 -> 14 5 1350 -> 3 числа
    #print(n, m)

    system_eq = [[0]] * (n+1)
    #print(system_eq)

    E = np.eye(n)

    print('введите свободное слагаемое, затем коэффициенты'+ '\n' + ' для каждого уравнения по очереди')
    for i in range (n):
            a = map(int,input().split())
            a = list(a)
            for j in range(n):
                a.append(int(E[i][j]))
            system_eq[i] = [] + a

    print('Введите коэффициенты целевой функции в формате z-x1-x2=0')
    a = map(int,input().split())
    a = list(a)
    for j in range(n):
        a.append(0)
    system_eq[n] = [] + a

    return base_output(system_eq, n)

def base_output(eq_list, n):
    #system_eq = [[350,14, 5,  1, 0, 0], [392,14, 8,  0, 1, 0], [408,6, 12,  0, 0, 1], [0, -10, -5,  0, 0, 0]]
    basis_cols=[]

    for i in range(n):
        basis_cols.append(n+i)
    
    #print(basis_cols)
    #print(system_eq)
    eq_arr = np.array(eq_list, dtype=float)
    return eq_arr, basis_cols, n
