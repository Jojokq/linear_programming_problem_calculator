import csv
from pathlib import Path
import numpy as np
from consol_input import base_output
def import_table():
    FILENAME = Path('datatable/example_data.csv').resolve()

    dataset = []
    target_function = None

    with open(FILENAME, newline="", encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        
        for row in reader:
            if not row or not row[0]:  # Пропускаем пустые строки
                continue
                
            first_elem = row[0].strip()
            
            if first_elem == 'C':  # Заголовок - пропускаем
                continue
            elif first_elem == '':  # Пустая строка перед целевой функцией
                continue
            elif first_elem == '0':  # Целевая функция
                # Преобразуем коэффициенты обратно (умножаем на -1)
                target_coeffs = [float(val) * -1 for val in row[1:] if val]
                target_function = target_coeffs
            else:  # Ограничения (неравенства)
                dataset.append(row)
    print(dataset)
    return base_output(dataset, len(dataset))
