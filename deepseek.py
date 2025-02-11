#%%
from prompts import get_prefix
from dotenv import load_dotenv
import os
import requests
import time
import json
load_dotenv(r'D:\DoubtSolver\.env')  # Load environment variables from a .env file
#%%
###
ec2_ip = "10.233.4.138"
port = 11434

def deepseek(question):

    # Construct the URL with the endpoint 
    url = f"http://{ec2_ip}:{port}/api/generate"
    
    # Prepare the data to send (dictionary with "model" and "prompt" keys)
    message = {"model": "deepseek-r1:14b", "prompt": question}


    try:
        # Send the POST request with the data
        response = requests.post(url, data=json.dumps(message))

        if response.status_code == 200:
            parsed_response = [json.loads(line) for line in response.text.split("\n") if line]
            complete_response = [line["response"] for line in parsed_response]
            outcome = "".join(complete_response)
            print(f"response: {outcome}") 
           
            return outcome  # Return the outcome
        else:
            print(f"Error: {response.status_code}, {response.text}")  # Print error details
            return None
    except Exception as e:
        print(f"Exception occurred: {str(e)}")  # Print exception details
        return None

# %%
# deepseek("what is an atom")
# %%
def format_prompt(subject, grade, question, examples):

    prefix_text = get_prefix(subject,grade)
    
    # examples = format_examples(examples)  #getting only the required fields in examples json

    # Format examples
    formatted_examples = []

    if not examples:
        print("No examples")
    else:
        # examples = format_examples(examples)
        # Example template definition
        example_template ='''Example: {question_text} \n Answer: {solution}'''
        
        for example in examples:
            try:
                formatted_example = example_template.format(
                    question_text=example['question'],  
                    solution=example['solution']
                )
                formatted_examples.append(formatted_example)
            except KeyError as e:
                print(f"KeyError: Missing key {e} in example {example}")
                continue
    
    if not formatted_examples:
        try:
            # Define few-shot prompt template
            few_shot_prompt = f"{prefix_text}\n" + f"\n\nQuestion:(Question to be answered.):\n {question}"   
        except KeyError as e:
            print(f"Error: {e} in formatting the final prompt.")
            return None
    else:
        # Format the final prompt
        try:
            # Define few-shot prompt template
            few_shot_prompt = f"{prefix_text}\n" + f"\n\n".join(formatted_examples) + f"\n\nQuestion:(Question to be answered.):\n {question}"   
        except KeyError as e:
            print(f"Error: {e} in formatting the final prompt.")
            return None

    return few_shot_prompt

question = "A line makes an angle of $$ frac{pi }{4}$$with the positive directions of each of $$ y-$$and $$ z-$$axes. Then the angle that the line makes with the positive direction of $$ x-$$axis, is",

examples= [{"question": "A line makes an angle of $$ \\frac{\\pi }{4}$$with the positive directions of each of $$ y-$$and $$ z-$$axes. Then the angle that the line makes with the positive direction of $$ x-$$axis, is",
  "solution": " If<math xmlns=http://www.w3.org/1998/Math/MathML><mi>α</mi><mo>,</mo><mi>β</mi><mo>,</mo><mi>γ</mi></math>are the angles made by a line ‘L’ with the coordinate axes in the positive direction then<math xmlns=http://www.w3.org/1998/Math/MathML><msup><mi>cos</mi><mn>2</mn></msup><mi>α</mi><mo>+</mo><msup><mi>cos</mi><mn>2</mn></msup><mi>β</mi><mo>+</mo><msup><mi>cos</mi><mn>2</mn></msup><mi>γ</mi><mo>=</mo><mn>1</mn></math>Given<math xmlns=http://www.w3.org/1998/Math/MathML><mi>β</mi><mo>=</mo><mfrac><mi>π</mi><mn>4</mn></mfrac><mo>,</mo><mi>γ</mi><mo>=</mo><mfrac><mi>π</mi><mn>4</mn></mfrac></math>Hence,<math xmlns=http://www.w3.org/1998/Math/MathML><msup><mi>cos</mi><mn>2</mn></msup><mi>α</mi><mo>+</mo><mfrac><mn>1</mn><mn>2</mn></mfrac><mo>+</mo><mfrac><mn>1</mn><mn>2</mn></mfrac><mo>=</mo><mn>1</mn><mo>⇒</mo><mi>cos</mi><mi>γ</mi><mo>=</mo><mn>0</mn></math>Therefore,<math xmlns=http://www.w3.org/1998/Math/MathML><mi>γ</mi><mo>=</mo><mfrac><mi>π</mi><mn>2</mn></mfrac></math> "}
 ]


prompt = format_prompt("Maths",11, question, examples)
# %%
prompt
# %%
deepseek(prompt)
# %%