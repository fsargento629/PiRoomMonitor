import csv
file_name = 'data/test.csv'
row = ['28', '12', ' 2018',20,80]

with open(file_name, 'a') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(row)

csvFile.close()