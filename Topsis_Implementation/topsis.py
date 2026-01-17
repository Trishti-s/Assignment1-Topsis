import sys
import pandas as pd
import numpy as np

if len(sys.argv) != 5:
    print("Usage: python topsis.py <InputFile> <Weights> <Impacts> <OutputFile>")
    sys.exit(1)

input_file = sys.argv[1]
weights = sys.argv[2].split(',')
impacts = sys.argv[3].split(',')
output_file = sys.argv[4]

try:
    data = pd.read_csv(input_file)
except FileNotFoundError:
    print("Error: Input file not found")
    sys.exit(1)

if data.shape[1] < 3:
    print("Error: File must contain at least 3 columns")
    sys.exit(1)

criteria = data[['Manf_year', 'Exp_date', 'Quantity_in_stock', 'Sales']]

try:
    matrix = criteria.astype(float).values
except:
    print("Error: Criteria columns must be numeric")
    sys.exit(1)

if len(weights) != matrix.shape[1] or len(impacts) != matrix.shape[1]:
    print("Error: Number of weights and impacts must match criteria")
    sys.exit(1)

weights = np.array(weights, dtype=float)

for i in impacts:
    if i not in ['+', '-']:
        print("Error: Impacts must be + or -")
        sys.exit(1)

norm = matrix / np.sqrt((matrix ** 2).sum(axis=0))
weighted = norm * weights

ideal_best = []
ideal_worst = []

for i in range(len(impacts)):
    if impacts[i] == '+':
        ideal_best.append(weighted[:, i].max())
        ideal_worst.append(weighted[:, i].min())
    else:
        ideal_best.append(weighted[:, i].min())
        ideal_worst.append(weighted[:, i].max())

ideal_best = np.array(ideal_best)
ideal_worst = np.array(ideal_worst)

dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

score = dist_worst / (dist_best + dist_worst)

data['Topsis Score'] = score
data['Rank'] = data['Topsis Score'].rank(ascending=False)

data.to_csv(output_file, index=False)
print("TOPSIS analysis completed successfully")
