import os
import time
import random

def crc(data):
    h = 0
    for ki in data:
        highorder = h & 0xf8000000
        h = h << 5
        h = h ^ (highorder >> 27)
        h = h ^ ki
    return h

def pjw(data):
    h = 0
    for ki in data:
        h = (h << 4) + ki
        g = h & 0xf0000000
        if g != 0:
            h = h ^ (g >> 24)
            h = h ^ g
    return h

def buz(data):
    h = 0
    R = dict()
    for r, i in enumerate(data):
        R[i] = r
    for ki in data:
        highorder = h & 0x80000000
        h = h << 1
        h = h ^ (highorder >> 31)
        h = h ^ R[ki]
    return h

def find_duplicates(files: list[str], hash_function: callable):
    hash_dict = {}
    duplicates = []
    total_time = 0
    
    for file in files:
        with open(f"out/{file}", 'rb') as f:
            file_data = f.read()

            start_time = time.time()
            file_hash = hash_function(file_data)
            end_time = time.time()
            
            total_time += (end_time - start_time)
            if file_hash in hash_dict:
                duplicates.append(file)
            else:
                hash_dict[file_hash] = file
                
    return duplicates, total_time


files = []
for x in os.listdir("out"):
    if x.endswith(".txt"):
        files.append(x)

functions = [crc, pjw, buz, hash]

for i in functions:
    dup, time1 = find_duplicates(files, i)
    print(f"\t{i.__name__}")
    print(f"Number of duplicates: {len(dup)}")
    print(f"Execution time: {time1} sec")
    print()