import time
from datetime import datetime, timedelta
from flask import Flask, render_template, request, session
from create_model import create_model
from delete_old_files import delete_old_files
from make_prediction import make_prediction

app = Flask(__name__)
app.secret_key = 'mysecretkey'

class PredictRequest():
    def __init__(self, target_column):
        self.target_column = target_column

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    target_column = int(request.form['target_column'])
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file'
    
    file_contents = file.read()
    
    model_filename, bounds_filename = create_model(file_contents, target_column)
    
    session['model_filename'] = model_filename  # Save the filenames to the user's session
    session['bounds_filename'] = bounds_filename
    
    return render_template('predict.html')
    
@app.route('/results', methods=['POST'])
def results():
    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    file_contents = file.read()

    model_filename = session['model_filename']

    prediction_filename, results = make_prediction(file_contents, model_filename)

    session['prediction_filename'] = prediction_filename

    return render_template('results.html', results = results, numbers = range(len(results[0])))

def run_daily_cleanup():
    file_age_days = 2

    now = datetime.now()

    cleanup_time = datetime(now.year, now.month, now.day, 1, 0, 0)

    if now > cleanup_time:
        cleanup_time += timedelta(days=1)

    time_to_wait = (cleanup_time - now).total_seconds()

    time.sleep(time_to_wait)

    delete_old_files('./models', file_age_days)

if __name__ == '__main__':
    app.run(debug=True)

    import threading
    cleanup_thread = threading.Thread(target=run_daily_cleanup)
    cleanup_thread.start()