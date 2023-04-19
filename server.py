from flask import Flask, request, jsonify
from train import create_model, process_csv
from flask_cors import CORS

#MAIN TODO

# * Style predict page
# * Setup communication between client and ML-Server
# * Setup firebase auth
# * Setup firebase storage
# * Next steps?

app = Flask(__name__)
CORS(app)

# Returns model when given a CSV and target column
@app.route('/train', methods=['POST'])
def train():
    print(request.form)
    file = request.form['file']
    target_col = int(request.form["targetcol"])
    model_data = create_model(file, target_col)
    return jsonify({"model": model_data[0], "bounds": model_data[1]})

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "I farded :D"})

# Returns CSV when given a model and CSV
@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']
    model = request.files['model']
    prediction = process_csv(file, model)
    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    app.run(debug=True)