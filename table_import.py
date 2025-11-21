import csv
from pathlib import Path
import numpy as np
from consol_input import base_output

def import_table():
    FILENAME = Path('datatable/inequality_system.csv').resolve()

    constraints = []
    target_function = None

    with open(FILENAME, newline="", encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        
        for row in reader:
            if not row or not row[0]:  # Пропускаем пустые строки
                continue
                
            first_elem = row[0].strip()
            
            if first_elem == 'C':  # Заголовок - пропускаем
                continue
            elif first_elem == '':  # Пустая строка
                continue
            elif first_elem == '0':  # Целевая функция
                # Преобразуем коэффициенты в float
                target_coeffs = [float(val.strip()) for val in row[1:] if val.strip()]
                target_function = target_coeffs
            else:  # Ограничения
                # Преобразуем все элементы строки в float
                try:
                    constraint_row = [float(val.strip()) for val in row if val.strip()]
                    constraints.append(constraint_row)
                except ValueError:
                    continue
    
    print(f"Found {len(constraints)} constraints")
    print(f"Constraints: {constraints}")
    print(f"Target function: {target_function}")
    
    # Определяем максимальное количество переменных в ограничениях
    max_vars = max(len(constraint) for constraint in constraints) if constraints else 0
    num_constraints = len(constraints)
    
    # Создаем полную систему для симплекс-метода
    system_eq = []
    
    # Добавляем ограничения с slack-переменными
    for i, constraint in enumerate(constraints):
        # Дополняем ограничение до нужной длины
        current_vars = len(constraint)
        if current_vars < max_vars:
            # Добавляем нули для недостающих переменных
            constraint = constraint + [0.0] * (max_vars - current_vars)
        
        # Добавляем slack-переменные
        slack_vars = [0.0] * num_constraints
        slack_vars[i] = 1.0  # Единица для соответствующей slack-переменной
        
        system_row = constraint + slack_vars
        system_eq.append(system_row)
    
    # Добавляем целевую функцию
    if target_function is not None:
        # Дополняем целевую функцию до нужной длины
        current_target_vars = len(target_function)
        if current_target_vars < max_vars:
            target_function = target_function + [0.0] * (max_vars - current_target_vars)
        
        # Добавляем нули для slack-переменных
        target_slack = [0.0] * num_constraints
        full_target = target_function + target_slack
        
        # Умножаем на -1 для симплекс-таблицы
        full_target_negative = [-coeff for coeff in full_target]
        system_eq.append(full_target_negative)
    
    print("Final system for simplex method:")
    for i, eq in enumerate(system_eq):
        print(f"Eq {i}: {eq}")
    
    # Проверяем, что все строки имеют одинаковую длину
    if system_eq:
        expected_length = len(system_eq[0])
        for i, eq in enumerate(system_eq):
            if len(eq) != expected_length:
                print(f"Warning: Equation {i} has length {len(eq)}, expected {expected_length}")
                # Дополняем нулями до нужной длины
                system_eq[i] = eq + [0.0] * (expected_length - len(eq))
    
    return base_output(system_eq, num_constraints)

import_table()