from flask import Flask, render_template, request, jsonify
import openai
import re

app = Flask(__name__)

# Load your OpenAI API key
openai.api_key = "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"

# Load custom data from file
def load_custom_data():
    with open("custom_data.txt", "r") as file:
        lines = file.readlines()
        data = {}
        for i in range(0, len(lines), 2):
            question = lines[i].strip().replace("Question: ", "")
            answer = lines[i + 1].strip().replace("Answer: ", "")
            data[question.lower()] = answer
        return data

custom_data = load_custom_data()

# Define the route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Define the route for the API call to ChatGPT
@app.route('/api/ask_chatgpt', methods=['POST'])
def ask_chatgpt():
    # Get the user input
    user_input = request.form['user_input'].lower()  # Convert to lowercase for case-insensitive matching
    
    # Check if the question exists in the custom data
    response = custom_data.get(user_input)
    if response:
        return jsonify({'response': response})
    else:
        # Check if any part of the user input matches a question
        for question, answer in custom_data.items():
            if re.search(user_input, question):
                return jsonify({'response': answer})
        
        # If no match found, call OpenAI's GPT-3 API with the user input
        response = call_gpt3(user_input)
        return jsonify({'response': response})

# Call GPT-3 API to generate response
def call_gpt3(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    app.run(debug=True)
