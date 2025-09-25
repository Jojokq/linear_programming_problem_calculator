import csv
from pathlib import Path
import numpy as np
from consol_input import base_output

FILENAME = Path('Datatable/data.csv').resolve()

dataset = []

with open(FILENAME, newline="") as csvfile:
    reader = csv.reader(csvfile, )
    n=-1
    for _ in reader: 
        list_read = _
        elem = list_read[0][:1]
        if elem != 'C' and elem != ';':
            dataset.append(list_read)
            n+=1



#base_output(dataset, n)
print(dataset)
