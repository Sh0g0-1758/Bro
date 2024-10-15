import csv

input_file = 'data.txt'
output_file = 'netflow.csv'

with open(input_file, 'r') as txt_file, open(output_file, 'w', newline='') as csv_file:
    reader = txt_file.readlines()
    writer = csv.writer(csv_file)

    for line in reader:
        row = line.split()
        writer.writerow(row)

print("Conversion complete! CSV saved as", output_file)
