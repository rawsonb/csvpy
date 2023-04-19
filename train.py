import pandas as pd
from io import StringIO
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
import pickle

def create_model(file, target_col):
    csv_file = StringIO(file)
    data = pd.read_csv(csv_file)
    target_column = data.columns[target_col]
    X = data.drop(target_column, axis=1)
    y = data[target_column]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Detect whether the target variable is continuous or categorical
    unique_targets = len(set(y))
    total_targets = len(y)
    ratio = unique_targets / total_targets
    threshold = 0.05

    if ratio < threshold:
        print("Training classifier...")
        model = GradientBoostingClassifier()
        scoring_metric = 'Accuracy'
        metric_function = accuracy_score
        param_dist = {
            'n_estimators': [50, 100, 200, 300],
            'learning_rate': [0.01, 0.1, 0.2],
            'max_depth': [1, 2, 3, 4],
            'min_samples_split': [2, 3, 4],
            'min_samples_leaf': [1, 2, 3]
        }
    else:
        print("Training regressor...")
        model = GradientBoostingRegressor()
        scoring_metric = 'R2 Score'
        metric_function = r2_score
        param_dist = {
            'n_estimators': [50, 100, 200, 300],
            'learning_rate': [0.01, 0.1, 0.2],
            'max_depth': [1, 2, 3, 4],
            'min_samples_split': [2, 3, 4],
            'min_samples_leaf': [1, 2, 3],
            'alpha': [0.1, 0.5, 0.9]
        }

    # Hyperparameter tuning with RandomizedSearchCV
    search = RandomizedSearchCV(model, param_dist, n_iter=50, cv=5, random_state=42, n_jobs=-1)
    search.fit(X_train, y_train)

    # Get the best model from the search
    best_model = search.best_estimator_

    # Test the best model on the testing set
    y_pred = best_model.predict(X_test)

    # Calculate and print the performance metric
    performance = metric_function(y_test, y_pred)

    #pickle model
    model_data = str(pickle.dumps(best_model, 0), encoding="latin1")

    # Save the minmax json
    min_values = X.min(axis=0)
    max_values = X.max(axis=0)
    num_params = X.shape[1]
    bounds = [(min_values[i], max_values[i]) for i in range(num_params)]

    return [model_data, bounds]

def process_csv(file, model_string):
    data = pd.read_csv(file)
    model = pickle.loads(bytes(model_string, "latin1"))
    predicted = model.predict(data)
    data["Prediction"] = predicted
    return data


