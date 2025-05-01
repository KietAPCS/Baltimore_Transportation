import csv

with open("2025_Problem_D_Data/edges_all.csv", 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['u'] == '49548197' and row['v'] == '49523066':
            print(row)
            break
