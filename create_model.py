import io
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.model_selection import RandomizedSearchCV
from joblib import dump
import os
import time
import uuid

def create_model(csv_file, target_column):
    # Load the data into a pandas dataframe
    df = pd.read_csv(io.StringIO(csv_file.decode('utf-8')))
    
    # Extract the target column
    target = df.columns[target_column] 
    
    # Determine whether to use a classifier or a regressor
    unique_targets = df[target].nunique()
    total_targets = df.shape[0]
    if unique_targets / total_targets <= 0.5:
        model = GradientBoostingClassifier()
    else:
        model = GradientBoostingRegressor()
    
    # Define the bounds of the input data
    non_target_cols = df.columns[df.columns != target]
    bounds = np.array([[df[col].min(), df[col].max()] for col in non_target_cols])
    
    # Perform a randomized search over hyperparameters to find the best combination
    params = {
        "max_depth": [3, 5, 7, 9],
        "learning_rate": [0.01, 0.05, 0.1, 0.3],
        "n_estimators": [100, 200, 300, 500]
    }
    search = RandomizedSearchCV(model, param_distributions=params, n_jobs=-1)
    search.fit(df[non_target_cols], df[target])
    
    # Fit the model with the best hyperparameters to the data
    model.set_params(**search.best_params_)
    model.fit(df[non_target_cols], df[target])
    
    # Create unique file names for the trained model and the bounds of the input data
    timestamp = str(int(time.time()))
    rand_str = str(uuid.uuid4().hex)
    model_filename = f"model_{rand_str}_{timestamp}.joblib"
    bounds_filename = f"bounds_{rand_str}_{timestamp}.csv"
    
    # Save the trained model and the bounds of the input data
    dump(model, os.path.join('models', model_filename))
    pd.DataFrame(bounds).to_csv(os.path.join('models', bounds_filename), index=False)
    
    # Return the trained model and bounds
    return model_filename, bounds_filename