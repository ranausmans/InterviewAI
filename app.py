import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import logging
import re
import traceback

# Configure Google Generative AI
GENAI_API_KEY = "Gemini API key here"
genai.configure(api_key=GENAI_API_KEY)

# Configure Flask app
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://usman.today", "http://-----------:5006"]}})

app.secret_key = 'anything here'  # Make sure this is a strong, random key

# Set up the Generative AI model configuration
generation_config = {
    "temperature": 0.1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1000,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Add these global variables at the top of the file, after the imports
total_runs = 0
total_questions = 0

def process_generated_content(content, difficulty):
    questions = []
    current_question = {}
    
    for line in content.split('\n'):
        if line.startswith('question:'):
            if current_question:
                questions.append(current_question)
                current_question = {}
            current_question['question'] = line.replace('question:', '').strip()
        elif line.startswith('evaluation:'):
            current_question['evaluation'] = line.replace('evaluation:', '').strip()
        elif line.startswith('sampleAnswer:'):
            current_question['sampleAnswer'] = line.replace('sampleAnswer:', '').strip()
    
    if current_question:
        questions.append(current_question)
    
    return questions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_questions', methods=['POST'])
def generate_questions():
    global total_runs, total_questions
    try:
        total_runs += 1
        job_description = request.json['job_description']
        all_questions = {"normal": [], "medium": [], "advanced": []}

        for difficulty in ["normal", "medium", "advanced"]:
            prompt = f"""
Based on the following job description, generate EXACTLY 3 {difficulty} difficulty interview questions with their answers:
{job_description}

For each question, you MUST include:
1. The question itself
2. Evaluation criteria (what the question assesses and what constitutes a good answer)
3. A sample answer that would be considered excellent

Format the output EXACTLY as follows:

question: [Question 1]
evaluation: [Evaluation criteria for Question 1]
sampleAnswer: [Sample excellent answer for Question 1]

question: [Question 2]
evaluation: [Evaluation criteria for Question 2]
sampleAnswer: [Sample excellent answer for Question 2]

question: [Question 3]
evaluation: [Evaluation criteria for Question 3]
sampleAnswer: [Sample excellent answer for Question 3]

It is CRUCIAL that you provide EXACTLY 3 questions. Do not include any additional text or explanations outside of this structure.
"""
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = model.generate_content(prompt)
                    questions = response.text
                    app.logger.info(f"Generated content for {difficulty}: {questions}")
                    
                    processed = process_generated_content(questions, difficulty)
                    if len(processed) == 3:
                        all_questions[difficulty] = processed
                        break
                    else:
                        app.logger.warning(f"Attempt {attempt + 1}: Generated {len(processed)} questions for {difficulty} instead of 3")
                except Exception as e:
                    app.logger.error(f"Error in attempt {attempt + 1} for {difficulty}: {str(e)}")
                    if attempt == max_retries - 1:
                        raise

            while len(all_questions[difficulty]) < 3:
                all_questions[difficulty].append({
                    "question": f"Additional {difficulty} question",
                    "evaluation": "Evaluation criteria not available",
                    "sampleAnswer": "Sample answer not available"
                })

        # Count total questions generated
        total_questions += sum(len(questions) for questions in all_questions.values())

        app.logger.info(f"Final processed questions: {all_questions}")
        return jsonify({
            "questions": all_questions,
            "stats": {
                "total_runs": total_runs,
                "total_questions": total_questions
            }
        })

    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    return jsonify({
        "total_runs": total_runs,
        "total_questions": total_questions
    })

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5006, debug=False)
