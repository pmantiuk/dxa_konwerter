import subprocess
import os
import time
import re

def trim():
    er_pos = file.find('.')
    new_name = file[:er_pos-1] + file[er_pos:]
    os.renames(path + '\\' + file, path + "\\" + new_name)
        
def find_excluded():
    ends = re.split(r'[,|.|-]',string = file)
    module_pattern = re.compile(r'[\d\w]{1,2}-([\d]{3}|KL)(\d|X|Y|Z|/|-)(\d|X|Y|Z)*',re.I)
    wall_pattern = re.compile(r'[A-Z]{2,3}',re.I)
    number_pattern = re.compile(r'[0-9]{2}')
    match = module_pattern.finditer(file)
    for mat in match:
        mat = mat.group()            
    for i in range(1,len(ends)-1):
        test = re.match(wall_pattern, ends[i])
        if bool(test):
            wall = test.group()
            for j in range(i+1,len(ends)-1):
                numb_test = re.match(number_pattern,ends[j])
                if bool(numb_test) and j>i:
                    wall_number = ends[j]
                    excluded.append(mat + '-' + wall.upper() + '-' + wall_number)
                else:
                    break
            
excluded = []
bvn_list = ''
dxa_list = []
path = str(input('Podaj ścieżkę do folderu, którego pliki chcesz przeobić na BVNy: '))

for file in os.listdir(path):
    if file.endswith(".DXM") and file[file.find('.')-3:file.find('.')].isdigit():
        trim()
        
for file in os.listdir(path):
    if file.endswith(".DXM"):
        find_excluded()        
        
for file in os.listdir(path):        
    if (file.rstrip('.dxa') not in excluded) and (not file.endswith(('.bvn','.wup'))):
        plik = os.path.join(path, file)
        p = subprocess.Popen([r"C:\Users\Pawka\Desktop\weinmanwin3.exe", plik]) 

input('\nZaczekaj aż program przetworzy wszystkie pliki. \nDla sprawdzenia poprawności działania programu, \nnaciśnij klawisz Enter')

for file in os.listdir(path):
    if file.endswith('.bvn'):
        bvn_list += os.path.join(file) + ','
        
processed_walls = re.split(r'[,|.|-]',string = bvn_list)
processed_walls = '\n'.join(processed_walls)
number_pattern = re.compile(r'\b[0-9]{2}\b')
bvn_amount  = re.findall(number_pattern, processed_walls)
bvn_amount = len(bvn_amount)

for file in os.listdir(path):
    if file.endswith('.dxa'):
        dxa_list.append(os.path.join(file))
dxa_amount = len(dxa_list)

if dxa_amount == bvn_amount:
    print('\nLiczba plików DXA, BVN i WUP się zgadza :)\nPrzetworzonych plików: ' + str(bvn_amount))  
else:
    print('\nUWAGA!!! Ilość plików DXA, BVN i WUP niezgodna.\nSprawdź co się stało! :(')
         
input('\nJeśli chcesz automatycznie zamknąć okienka bez przeglądania, \nnaciśnij klawisz Enter')
subprocess.call(["taskkill","/F","/IM","weinmanwin3.exe"])