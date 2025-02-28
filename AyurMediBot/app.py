from flask import Flask, request, jsonify, render_template
import random
import json

app = Flask(__name__)

# Load dataset for medicine info
with open('medicine_dataset.json') as f:
    medicine_data = json.load(f)

@app.route('/')
def home():
    return render_template('index.html')

def get_medicine_response(user_input):
    user_input = user_input.lower()
    for medicine in medicine_data:
        if medicine["medicine_name"].lower() in user_input or any(condition.lower() in user_input for condition in medicine["conditions_treated"]):
            response = f"Medicine Name: {medicine['medicine_name']}\n"
            response += f"System: {medicine['system']}\n"
            response += f"Ingredients: {', '.join(medicine['ingredients'])}\n"
            response += f"Conditions Treated: {', '.join(medicine['conditions_treated'])}\n"
            response += f"Dosage (Adults): {medicine['dosage'].get('adult', 'Not available')}\n"
            response += f"Dosage (Children): {medicine['dosage'].get('children', 'Not available')}\n"
            response += f"Precautions: {', '.join(medicine['precautions'])}\n"
            response += f"Side Effects: {', '.join(medicine['side_effects'])}\n"
            return response
    # Default response if no match is found
    return "I'm sorry, I don't have information on that. Please try mentioning another medicine or symptom."

@app.route('/get_response', methods=['POST'])
def respond():
    user_input = request.json.get("message")
    response = get_medicine_response(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
