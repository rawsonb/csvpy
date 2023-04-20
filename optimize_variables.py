from scipy.optimize import differential_evolution
from joblib import load
import pandas as pd


def optimize_variables(bounds_filename, model_filename):
    # Load the bounds from the specified CSV file
    bounds_df = pd.read_csv(f'models/{bounds_filename}')
    bounds = bounds_df.values.tolist()

    # Load the scikit learn model
    model = load(f'models/{model_filename}')

    n_params = model.n_features_in_

    # Define the objective function to optimize
    def objective_function(x):
        x = x.reshape(-1, n_params) #should match the shape expected by the model
        prediction = model.predict(x)
        return -prediction

    result = differential_evolution(objective_function, bounds=bounds)

    good_result = []

    for i in result.x:
        good_result.append(format(i, ".4f"))
    # Return the optimized variables and the corresponding target value
    return good_result, -result.fun