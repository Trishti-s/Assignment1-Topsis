import pandas as pd
import numpy as np
import sys

def topsis():
    if len(sys.argv) != 5:
        print("Usage: topsis input.csv weights impacts output.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    weights = list(map(float, sys.argv[2].split(',')))
    impacts = sys.argv[3].split(',')
    output_file = sys.argv[4]

    data = pd.read_csv(input_file)
    decision = data.iloc[:, 1:].values.astype(float)

    norm = np.sqrt((decision ** 2).sum(axis=0))
    normalized = decision / norm
    weighted = normalized * weights

    ideal_best = np.max(weighted, axis=0)
    ideal_worst = np.min(weighted, axis=0)

    for i in range(len(impacts)):
        if impacts[i] == '-':
            ideal_best[i], ideal_worst[i] = ideal_worst[i], ideal_best[i]

    dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    score = dist_worst / (dist_best + dist_worst)

    data['Topsis Score'] = score
    data['Rank'] = data['Topsis Score'].rank(ascending=False)

    data.to_csv(output_file, index=False)
