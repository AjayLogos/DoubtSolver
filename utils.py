#%%
from MathML2LATEX.mathml2latex import convert_string_to_latex
from html_css_tag_removal import remove_html_css_tag
# from sentence_transformers import SentenceTransformer
from prompts import get_prefix , get_eval_prompt
import json
import re
import time
import requests

#Credentials to use llama
ec2_ip = "10.233.4.138"
port = 11434

#Model to encode incoming question
# model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

#converting question to latex form
def Question_conversion(input_text):
    """
    Processes the input text. If the input contains MathML tags;
    """
    # Regular expression pattern to detect MathML tags
    mathml_pattern = re.compile(r'<math[^>]*>.*?</math>', re.DOTALL)

    # Check if the input contains MathML tags
    if mathml_pattern.search(input_text):
        input_text = input_text.replace("&nbsp;", " ")
        response = convert_string_to_latex(input_text)
        response = remove_html_css_tag(response)
        return response
    else:
        response = remove_html_css_tag(input_text)
        return response

#%%
#formatting examples
def format_examples(examples):
    examples_list=[]
    # Check if examples is empty or doesn't contain 'matches'
    if not examples:
        return examples_list 
    
    for i in range(0,5):
        try:
            if "solution" in examples['matches'][i]['metadata'].keys():
                if examples['matches'][i]['score']>0.65:
                    try: 
                        examples_list.append({
                        "question":examples['matches'][i]['metadata']["question"],
                        "solution":examples['matches'][i]['metadata']["solution"],
                        "correct_answer":examples['matches'][i]['metadata']["correct_answer"]
                        })
                    except:
                        pass
        except:
            pass
    return examples_list


#creating a few shot prompt
def format_prompt(subject, grade, question, examples):

    question = Question_conversion(question)
    # Fetch the prefix text for the subject
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


def evaluate(question,llm_response):

    prompt = get_eval_prompt(question,llm_response)

    # Construct the URL with the endpoint 
    url = f"http://{ec2_ip}:{port}/api/generate"
    
    # Prepare the data to send (dictionary with "model" and "prompt" keys)
    message = {"model": "llama3.2:latest", "prompt": prompt}
    
    # print(f"Sending request for value: {value}")  # Indicate request is being sent
    start_time = time.time()  # Start timing

    try:
        # Send the POST request with the data
        response = requests.post(url, data=json.dumps(message))

        elapsed_time = time.time() - start_time  # Measure elapsed time
        print(f"Received response in {elapsed_time:.2f} seconds")  # Indicate response received

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
# %%

# %%
