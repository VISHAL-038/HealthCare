from flask import Flask, request, jsonify
import pickle
import numpy as np
import statistics

# Load trained models and data dictionary
try:
    rf_model = pickle.load(open("rf_model.pkl", "rb"))
    nb_model = pickle.load(open("nb_model.pkl", "rb"))
    svm_model = pickle.load(open("svm_model.pkl", "rb"))
    data_dict = pickle.load(open("data_dict.pkl", "rb"))
    print("✅ Models and Data Dictionary Loaded Successfully!")
except Exception as e:
    print(f"❌ Error loading models: {e}")

app = Flask(__name__)

@app.route('/')
def home():
    return "Disease Prediction API is Running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get symptoms from request
        data = request.get_json()
        print("📌 Received Data:", data)  # Debugging

        if not data or "symptoms" not in data:
            return jsonify({"error": "Missing 'symptoms' in request"}), 400

        symptoms = [symptom.strip() for symptom in data["symptoms"].split(",")]

        # Create input data with all 0s
        input_data = [0] * len(data_dict["symptom_index"])
        for symptom in symptoms:
            index = data_dict["symptom_index"].get(symptom)  # Safely get index
            if index is not None:
                input_data[index] = 1
            else:
                print(f"⚠️ Warning: '{symptom}' not found in symptom index!")

        # Convert input to array
        input_data = np.array(input_data).reshape(1, -1)

        # Generate predictions
        rf_prediction = data_dict["predictions_classes"][rf_model.predict(input_data)[0]]
        nb_prediction = data_dict["predictions_classes"][nb_model.predict(input_data)[0]]
        svm_prediction = data_dict["predictions_classes"][svm_model.predict(input_data)[0]]

        # Final prediction using mode
        final_prediction = statistics.mode([rf_prediction, nb_prediction, svm_prediction])

        predictions = {
            "rf_model_prediction": rf_prediction,
            "naive_bayes_prediction": nb_prediction,
            "svm_model_prediction": svm_prediction,
            "final_prediction": final_prediction
        }

        print("📌 Prediction Response:", predictions)  # Debugging
        return jsonify(predictions)

    except Exception as e:
        print("❌ Error in Prediction:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
