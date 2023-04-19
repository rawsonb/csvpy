import numpy as np
from scipy.optimize import differential_evolution
from joblib import load
import json

model = load("trained_model.joblib")

n_params = model.n_features_in_

#gets bounds
with open("bounds.json", "r") as f:
    bounds = json.load(f)

def objective_function(x):
    x = x.reshape(-1, n_params) #should match the shape expected by the model
    prediction = model.predict(x)
    return -prediction

result = differential_evolution(objective_function, bounds=bounds)

good_result = []

for i in result.x:
    good_result.append(format(i, ".4f"))

print("Optimal solution: ", good_result)
print("Maximum prediction: ", -result.fun)