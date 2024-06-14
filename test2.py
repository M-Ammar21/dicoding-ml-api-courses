from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tensorflow as tf

app = Flask(__name__)
CORS(app)

# Path to the directory containing the saved model
# saved_model_dir = os.path.join(os.getcwd(), 'model/')
saved_model_dir = './model/'

# Load the model
try:
    model = tf.saved_model.load(saved_model_dir)
    infer = model.signatures['serving_default']
except Exception as e:
    print(f"Error loading model: {e}")
    infer = None

@app.route('/predict', methods=['POST'])
def predict():
    if infer is None:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        data = request.json
        if 'input_data' not in data:
            return jsonify({"error": "No input data provided"}), 400

        input_data = tf.constant([data['input_data']], dtype=tf.string)
        predictions = infer(input_data)

        # Log available keys in predictions
        prediction_keys = list(predictions.keys())
        # print(f"Available prediction keys: {prediction_keys}")

        # Assuming the correct output key needs to be identified
        output_key = prediction_keys[0]  # Use the first key as an example

        # Convert prediction to a serializable format
        predictions_serializable = predictions[output_key].numpy().astype(str).tolist()

        return predictions_serializable
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)