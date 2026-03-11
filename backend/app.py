from flask import Flask, render_template, request, jsonify
from chatbot_Gemma3 import CustomerSupportBot as Gemma3
from chatbot_Llama3 import CustomerSupportBot as Llama3
from chatbot_Mistral import CustomerSupportBot as Mistral
from DataCleaner import clean_dataset  # Import the cleaning function
import pandas as pd

# Initialize Flask app with custom template folder
app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")

# Initialize models
models = {
    "1": Gemma3("../data/Cleaned_DataSet.csv", "../data/intents.json"),
    "2": Llama3("../data/Cleaned_DataSet.csv", "../data/intents.json"),
    "3": Mistral("../data/Cleaned_DataSet.csv", "../data/intents.json"),
}

# Serve the frontend
@app.route("/")
def index():
    return render_template("index.html")

# Handle chatbot interaction
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    model_choice = request.json.get("model")
    if not user_input or not model_choice:
        return jsonify({"error": "Invalid input"}), 400

    bot = models.get(model_choice)
    if not bot:
        return jsonify({"error": "Invalid model choice"}), 400

    response = bot.get_response(user_input)
    return jsonify({"response": response})

# Route to clean the dataset
@app.route("/clean-dataset", methods=["POST"])
def clean_dataset_route():
    input_file = "../data/DataSet.csv"
    output_file = "../data/Cleaned_DataSet.csv"

    # Clean the dataset
    clean_dataset(input_file, output_file)

    # Load the cleaned dataset and return a preview
    cleaned_df = pd.read_csv(output_file)
    preview = cleaned_df.head().to_dict(orient="records")
    return jsonify({"preview": preview})

if __name__ == "__main__":
    app.run(debug=True)