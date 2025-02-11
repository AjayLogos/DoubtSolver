#%%
from utils import format_prompt ,evaluate
from llms.agent_llm import AgentLlm
import logging
import os
from flask import Flask, request, jsonify
from langchain_core.output_parsers import JsonOutputParser
from database import store_question_output
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Without using agent
def get_llm_response(subject, grade, question, examples ):
        agent_llm = AgentLlm()
        llm = agent_llm.load_agent_llm()

        prompt = format_prompt(subject, grade, question, examples)
        parser = JsonOutputParser()
        agent = llm | parser

        result = agent.invoke(prompt)
        print(result)
        return result

#%%
@app.route('/doubt_solver', methods=['POST'])
def doubt_solver():
    if not request.is_json:
        return jsonify({"error": "Unsupported Input Type"}), 415
    try:
        data = request.get_json()
        doubt_id = data.get('doubt_id')
        grade_id = data.get('grade_id')    
        question = data.get('original_question')
        examples = data.get('rag_output_JSON')
        subject = data.get('subject')
    except Exception as e:
        return jsonify({"error": "Invalid JSON"}), 400
    
    if question is None:
        return jsonify({"error": "message is required"}), 400

    response = get_llm_response(subject,grade_id,question,examples)
    
    feedback = evaluate(question, response)
    
    store_question_output(doubt_id, grade_id,subject, question,response['hints'], response['steps'],response['final_answer'], feedback)

    return jsonify({"doubt_id": doubt_id,"hints": response['hints'],"steps": response['steps'],"final_answer": response['final_answer'],"evaluation_feedback": feedback})

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), debug=True)
    except Exception as e:
        logging.error(f"Error starting the Flask application: {e}")

# %%
# {

# "doubt_id":123,
# "grade_id":11,
# "subject":"Maths",
# "original_question":"A line makes an angle of $$ frac{pi }{4}$$with the positive directions of each of $$ y-$$and $$ z-$$axes. Then the angle that the line makes with the positive direction of $$ x-$$axis, is",

# "rag_output_JSON":[{"question": "A line makes an angle of $$ \\frac{\\pi }{4}$$with the positive directions of each of $$ y-$$and $$ z-$$axes. Then the angle that the line makes with the positive direction of $$ x-$$axis, is",
#   "solution": " If<math xmlns=http://www.w3.org/1998/Math/MathML><mi>α</mi><mo>,</mo><mi>β</mi><mo>,</mo><mi>γ</mi></math>are the angles made by a line ‘L’ with the coordinate axes in the positive direction then<math xmlns=http://www.w3.org/1998/Math/MathML><msup><mi>cos</mi><mn>2</mn></msup><mi>α</mi><mo>+</mo><msup><mi>cos</mi><mn>2</mn></msup><mi>β</mi><mo>+</mo><msup><mi>cos</mi><mn>2</mn></msup><mi>γ</mi><mo>=</mo><mn>1</mn></math>Given<math xmlns=http://www.w3.org/1998/Math/MathML><mi>β</mi><mo>=</mo><mfrac><mi>π</mi><mn>4</mn></mfrac><mo>,</mo><mi>γ</mi><mo>=</mo><mfrac><mi>π</mi><mn>4</mn></mfrac></math>Hence,<math xmlns=http://www.w3.org/1998/Math/MathML><msup><mi>cos</mi><mn>2</mn></msup><mi>α</mi><mo>+</mo><mfrac><mn>1</mn><mn>2</mn></mfrac><mo>+</mo><mfrac><mn>1</mn><mn>2</mn></mfrac><mo>=</mo><mn>1</mn><mo>⇒</mo><mi>cos</mi><mi>γ</mi><mo>=</mo><mn>0</mn></math>Therefore,<math xmlns=http://www.w3.org/1998/Math/MathML><mi>γ</mi><mo>=</mo><mfrac><mi>π</mi><mn>2</mn></mfrac></math> "}
#  ]

# }