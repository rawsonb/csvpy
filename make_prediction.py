import io
import os
import time
import uuid
from joblib import load
import pandas as pd

def make_prediction(csv_file, model_filename):
    # Load the trained model
    model_path = os.path.join('models', model_filename)
    model = load(model_path)
    
    # Load the input data into a pandas dataframe
    df = pd.read_csv(io.StringIO(csv_file.decode('utf-8')), header=0)
    
    # Make predictions on the input data
    predictions = model.predict(df)
    
    # Add the predictions as a new column to the input data
    df['predictions'] = predictions
    
    # Save the predictions to a new CSV file in the 'predictions' folder
    timestamp = str(int(time.time()))
    rand_str = str(uuid.uuid4().hex)
    filename = f"predictions_{rand_str}_{timestamp}.csv"
    df.to_csv(os.path.join('predictions', filename))

    results = [df.columns.tolist()] + df.values.tolist()
  
    # Return the filename of the new predictions file
    return filename, results