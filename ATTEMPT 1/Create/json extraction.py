from dotenv import load_dotenv
import os
import openai
from openai import OpenAI
import json
import time
import re

load_dotenv("key.env")
openai.api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

file_path = 'super_prompt_test.txt'

def analyze_text(num, text_1, text_2):

    instruction = f"""
    You are a linguist experts. 
    OUTPUT: two sepatared json files written as string one after the other
    
    You have this sentence 
    Number of sentences: {num}
    Statement: {text_1}
    Justification: {text_2}
    
    1) Wtire JSON analysys of sentense
        
    1.1) Extract Rhetorical techniques (write several and explaination to each other), 
    1.2) Propaganda methods(write several and explaination to each other), 
    1.3) Polarity of the statement (positive, neutral or negative and explaination),
    1.4) Tonality of the statement (type of tonality and explaination), 
    1.5) Logical errors (Type of error and explaination)
    1.6) Contradictions within the statement (Yes or no and explainationwhy plus)
    1.7) Contradictions within the justification (Same as above)
    1.8) Contradictions when you consider statment and justification together
    
    Use justification only for extra comments and extra explaination in a convenient way(remember that the sub-paragraphs are interconnected and cannot be analyzed separately. The first subparagraph is the statement of the speaker, and the second subparagraph is extracted justification. Analyze them together. Use second subparagraph to better explanation of propaganda methods, rhetorical teqniques from first subparagraph). 
    ANSWER AS JSON STRUCTURE SEPARATE!!!
    DO NOT FORGET START WITH '```json' AND END WITH '```'
    DO NOT FORGET THE COMMAS INSIDE THE json FORMAT SO AS NOT TO VIOLATE THE INTEGRITY OF THE FILE

    
    2) Create JSON table with columns: 
    id = {num}, 
    Rhetorical Techniques = only names of this techniques (depends on what you wrote in analyses),  
    Propaganda Methods = only names of this methods, ethods (depends on what you wrote in analyses), 
    Polarity = positive, negative or neutral (depends on what you wrote in analyses), 
    Tonality = only name of type (depends on what you wrote in analyses),	
    Logical Errors = only name of type (depends on what you wrote in analyses),	
    Contradictions = yes or no (depends on what you wrote in analyses.
    1)  
    ). 
    ANSWER AS JSON STRUCTURE SEPARATE!!!
    DO NOT FORGET START WITH '```json' AND END WITH '```'
    DO NOT FORGET THE COMMAS INSIDE THE json FORMAT SO AS NOT TO VIOLATE THE INTEGRITY OF THE FILE
    """

    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": f"number: {num}\nstatement: {text_1}\njustification: {text_2}"}
        ]
    )
    input_text = chat_completion.choices[0].message.content

    # Folder for saving files
    output_folder = f"Test/{num}"

    # Creating a folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Saving the contents to a file num.txt
    with open(os.path.join(output_folder, f'{num}.txt'), 'w') as file:
        file.write(input_text)
        #json.dump(input_text, file, indent=4)


    # Clearing the string of newline characters
    сleaned_text = input_text.replace("\n", "")
    
    # Looking for JSON files between "`json' and "`'
    json_files = re.findall(r'```json(.*?)```', сleaned_text)

    # Converting JSON strings to Python objects
    json_data = [json.loads(file.strip()) for file in json_files]
    
    # Saving the extracted data to files
    with open(os.path.join(output_folder,'analysis.json'), 'w') as analysis_file:
        json.dump(json_data[0], analysis_file, indent=4)

    with open(os.path.join(output_folder,'table.json'), 'w') as table_file:
        json.dump(json_data[1], table_file, indent=4)

    print(f"{num}: Files 'analysis.json' and 'table.json' have been saved.")
    # Get the size of the files
    txt_size = os.path.getsize(os.path.join(output_folder, f'{num}.txt'))
    analysis_size = os.path.getsize(os.path.join(output_folder, 'analysis.json'))
    table_size = os.path.getsize(os.path.join(output_folder, 'table.json'))

    # Output the file size in bytes
    print(f"Size of {num}.txt: {txt_size} bytes")
    print(f"Size of analysis.json: {analysis_size} bytes")
    print(f"Size of table.json: {table_size} bytes\n\n")

    pass

# Debug example
#num = 1
#text_1 = """When did the decline of coal start? It started when natural gas took off that started to begin in (President George W.) Bushs administration."""
#text_2 = """Surovell said the decline of coal "started when natural gas took off  That started to begin in President (George W. ) Bushs administration. "No doubt, natural gas has been gaining ground on coal in generating electricity. The trend started in the 1990s but clearly gained speed during the Bush administration when the production of natural gas -- a competitor of coal -- picked up. But analysts give little credit or blame to Bush for that trend. They note that other factors, such as technological innovation, entrepreneurship and policies of previous administrations, had more to do with laying the groundwork for the natural gas boom."""
#analyze_text(num, text_1, text_2)

def analyze_with_retries(num, text_1, text_2, max_retries=10):
    attempts = 0
    while attempts < max_retries:
        try:
            analyze_text(num, text_1, text_2)
            return  # Successful completion, exit the function
        except Exception as e:
            attempts += 1
            print(f"Error in analyze_text for {num}: {e}. Retry {attempts}/{max_retries}...")
    print(f"Critical failure: analyze_text failed for {num} after {max_retries} retries.")
    raise RuntimeError(f"Failed to analyze text for {num}.")


def print_lines_in_sequence(file_path,start,end):
    with open(file_path, 'r') as file:
        lines = file.readlines()  # We read all the lines from the file
        # Iterate through every three lines and output them
        for i in range(3*start, 3*(end+1), 3):

            num = lines[i].strip()  # We read the number by removing extra spaces and newline characters
            text_1 = lines[i+1].strip()  # Read statement
            text_2 = lines[i+2].strip()  # Read justification

            analyze_with_retries(int(num), text_1, text_2)


# Specify the path to the file

print(print_lines_in_sequence(file_path,0,1266))