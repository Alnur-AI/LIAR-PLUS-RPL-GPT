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

dataset_name = 'train'
file_path = f'super_prompt_{dataset_name}.txt'

'''
        "Meta Information": [
            {{
                "Dataset Name": {dataset_name},
                "Name of file": {num},
                "Statement:": {text_1}
            }}
        ],
'''

def analyze_text(num, text_1, text_2):

    instruction = f"""
    You are a linguist experts. You need to analyse statement on rhetorical techniques, propaganda methods and logical errors. Tonality, polarity and contradictions in statement, Justification use only to analyse more accurate only given sentence.
    OUTPUT: JSON file written as string.
    
    You have this sentence 
    Dataset Name {dataset_name}
    Name of file: {num}
    Statement: {text_1}
    Justification: {text_2}

    THIS IS TASK FOR YOU:

    1) Write JSON file like this:
    ```
    {{
        "Rhetorical Techniques": [
            {{
                "Classification": "Rhetorical Devices and Figures of Speech ",
                "Details": [
                    {{
                        "Type": "Rhetorical Techniques type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "Manipulation of Facts and Information ",
                "Details": [
                    {{
                        "Type": "Rhetorical Techniques type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "Emotional Appeals",
                "Details": [
                    {{
                        "Type": "Rhetorical Techniques type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "Logical Argumentation and Reasoning ",
                "Details": [
                    {{
                        "Type": "Rhetorical Techniques type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "Manipulative Techniques ",
                "Details": [
                    {{
                        "Type": "Rhetorical Techniques type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "Fact-Based Arguments ",
                "Details": [
                    {{
                        "Type": "Rhetorical Techniques type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "Criticism and Devaluation ",
                "Details": [
                    {{
                        "Type": "Rhetorical Techniques type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "Audience Engagement Techniques  ",
                "Details": [
                    {{
                        "Type": "Rhetorical Techniques type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }}
        ],
        "Propaganda Methods": [
            {{
                "Classification": "Emotional Manipulation ",
                "Details": [
                    {{
                        "Type": "Propaganda Methods type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "Simplification and Misrepresentation",
                "Details": [
                    {{
                        "Type": "Propaganda Methods type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "Misdirection and Distraction",
                "Details": [
                    {{
                        "Type": "Propaganda Methods type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "Cherry-Picking and Selectivity ",
                "Details": [
                    {{
                        "Type": "Propaganda Methods type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "Social Influence and Group Dynamics ",
                "Details": [
                    {{
                        "Type": "Propaganda Methods type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "Deceptive Framing ",
                "Details": [
                    {{
                        "Type": "Propaganda Methods type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }}
        ],
        "Polarity": [
            {{
                "Type": "Positive, Neutral or Negative",
                "Explanation": "Explanation why you choice this type to statement"
            }}
        ],
        "Tonality": [
            {{
                "Classification": "Formality",
                "Details": [
                    {{
                        "Type": "Tonality type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "Emotional Tone ",
                "Details": [
                    {{
                        "Type": "Tonality type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "Urgency and Focus  ",
                "Details": [
                    {{
                        "Type": "Tonality type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "Narrative Style  ",
                "Details": [
                    {{
                        "Type": "Tonality type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "Inspirational and Awe ",
                "Details": [
                    {{
                        "Type": "Tonality type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "Euphemism and Directness ",
                "Details": [
                    {{
                        "Type": "Tonality type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "Thematic Tones ",
                "Details": [
                    {{
                        "Type": "Tonality type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "Literary Aesthetic ",
                "Details": [
                    {{
                        "Type": "Tonality type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }}
        ],
        "Logical Errors": [
            {{
                "Classification": "Relevance Fallacies ",
                "Details": [
                    {{
                        "Type": "Logical Errors type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "Ambiguity and Vagueness ",
                "Details": [
                    {{
                        "Type": "Logical Errors type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "Causal Fallacies  ",
                "Details": [
                    {{
                        "Type": "Logical Errors type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "Formal Logical Errors   ",
                "Details": [
                    {{
                        "Type": "Logical Errors type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "False Comparisons   ",
                "Details": [
                    {{
                        "Type": "Logical Errors type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "Fallacies of Overgeneralization  ",
                "Details": [
                    {{
                        "Type": "Logical Errors type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "Contradictory Arguments ",
                "Details": [
                    {{
                        "Type": "Logical Errors type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
            {{
                "Classification": "Dichotomies and Binary Thinking ",
                "Details": [
                    {{
                        "Type": "Logical Errors type 1",
                        "Explanation": "Explanation why you choice this type to statement"
                    }}
                ]
            }},
        ],
        "Contradictions": [
            {{
                "Type": "Yes or No",
                "Explanation": "Explanation why you choice this type to statement, depends on logical errors classification, is it empty or not"
            }}
        ]
    }}
    ```
    1.1) For rhetorical techniques, choose more than three types in classification, but most reliable, commas separate names: 
        1.1.1) Rhetorical Devices and Figures of Speech:
            Hyperbole, 
            Anaphora or Epiphora,
            Epizeuxis or Anadiplosis,
            Sarcasm or Irony, 	 
            Metaphor and Paronomasia, 	 
            Ellipsis (Omission of Words), 	 
            Pleonasm, 	 
            Syntactic Parallelism, 	 
            Antithesis, 	 
            Aposiopesis, 	 
            Allegory, 	 
            Euphemism, 	 
        1.1.2) Manipulation of Facts and Information 	
            Defamation, 	 
            De-Contextualization, 	 
            Lying by Omission, 	 
            Substitution of Concepts  (Anachronism or Metonymy), 	 
            Ambiguity or Doublespeak, 	 
            Gaslighting, 	 
            Misleading Statements, 	 
        1.1.3) Emotional Appeals	
            Nostalgia, 	 
            Aspirational Appeal (Evocative Language), 	 
            Sense of Urgency,	 
            Glass-Half-Full Perspective,	 
            Inflammatory Language,	 
            Alarmism, 	 
        1.1.4) Logical Argumentation and Reasoning 	
            Syllogism or Inductive and Deductive Reasoning,	 
            Counter-Argument,	 
            Contrast (Stark or Dismissive or Incongruity),	 
            Analogy, 	 
            Cumulative Argument, 	 
            Conditional Argument, 	 
            Causal Analysis,	 
        1.1.5) Manipulative Techniques 	
            Skepticism, 	 
            Appeal to Authority, 	 
            Positional Shift (Anchoring), 	 
            Pseudoprofound Statements, 	 
            Feeding the Narrative, 	 
            Playing the Victim (Victimhood), 	 
            Accusation (Innuendo or Allegation or Hypocrisy), 	 
        1.1.6) Fact-Based Arguments 	
            Quotations, 	 
            Appeal to Costs, 	 
            Historical Facts, 	 
            Statistical Facts, 	 
            Comparative Analysis, 	 
            Case Studies 	 
        1.1.7) Criticism and Devaluation 	
            Criticism, 	 
            De-Emphasis (Diminishing Words), 	 
            Skepticism, 	 
            Understatement (Litotes), 	 
            Denial (Denialism), 	 
        1.1.8) Audience Engagement Techniques 	
            Rhetorical Questions (Hypophora), 	 
            Self-Deprecation, 	 
            Appeal to Principles (Patriotism), 	 
            Appeal to Identity, 	 
            Virtue Signaling, 

    1.2) For propaganda methods, choose more than three types in classification, but most reliable, commas separate names: 
        1.2.1) Emotional Manipulation 
            Flag-Waving, 
            Heroification, 
            Fear-Mongering, 
            Doomsaying, 
            Demonization, 
            Us vs Them, 
            In-Group Favoritism (Partisan Framing), 
        1.2.2) Simplification and Misrepresentation 
            Black-And-White Thinking, 
            Glittering Generality, 
            Sloganeering, 
            Big Lie, 
            Fallacy of Emphasis, 
        1.2.3) Misdirection and Distraction 
            Distraction Tactics, 
            Subliminal Message, 
            Whataboutism, 
            Spinning, 
            Throwing Stones, 
        1.2.4) Cherry-Picking and Selectivity 
            Card-Stacking (Cherry-Picking), 
            Selective Whistleblowing, 
            Unaccountable Attribution, 
        1.2.5) Social Influence and Group Dynamics 
            Bandwagon, 
            Tokenism, 
            Foot-In-The-Door, 
        1.2.6) Deceptive Framing 
            Weasel Words, 
            Backdoor Argument, 
            Presumption of Necessity, 

    1.3) Polarity can be only Positive, Neutral or Negative. Choose and write in explaination why you choose it.
    
    1.4) Tonality choose more than three types in classification, but most reliable, commas separate names: 
        1.4.1) Formality (ALWAYS ANALYSE SENTENCE ON IT)
            Formal, 
            Informal, 
            Pedantic, 
        1.4.2) Emotional Tone  (ALWAYS ANALYSE SENTENCE ON IT)
            Serious, 
            Humorous, 
            Sarcastic, 
            Optimistic, 
            Pessimistic, 
            Sympathetic, 
            Contemptuous, 
            Cynical, 
            Passionate, 
            Indifferent, 
            Melancholic, 
            Romantic, 
        1.4.3) Urgency and Focus 
            Urgent, 
            Objective, 
            Subjective, 
            Critical, 
            Respectful, 
            Irreverent, 
        1.4.4) Narrative Style 
            Narrative, 
            Conversational, 
            Suspenseful, 
            Dramatic, 
            Stream-of-Consciousness, 
            Descriptive, 
            Reflective, 
            Introspective, 
        1.4.5) Inspirational and Awe 
            Inspirational, 
            Awe-Filled 
        1.4.6) Euphemism and Directness 
            Euphemistic, 
            Direct, 
        1.4.7) Thematic Tones 
            Fantastical, 
            Philosophical, 
            Scholarly, 
            Didactic, 
            Cerebral,
            Analytical, 
            Minimalist, 
            Straightforward, 
        1.4.8) Literary Aesthetic 
            Romantic, 
            Reflective, 
            Philosophical, 


    1.5) For logical errors, choose more than three types in classification, but most reliable, commas separate names: 

        1.5.1) Relevance Fallacies 
            Red Herring, 
            Ad Hominem Abusive, 
            Ad Hominem Tu Quoque, 
            Ad Hominem Circumstantial, 
            Ad Misercordiam, 
            Flaw Appeal, 
        1.5.2) Ambiguity and Vagueness 
            Fallacy of Equivocation, 
            Solecism, 
        1.5.3) Causal Fallacies 
            Post Hoc Ergo Propter Hoc, 
            False Analogy, 
            Fallacy of Cause and Effect, 
            Slippery Slope, 
            Ergo Propter Hoc, 
        1.5.4) Formal Logical Errors 
            Circular Reasoning, 
            Non-Sequitur, 
            Affirming the Consequent, 
            Fallacy of Presumption, 
        1.5.5) False Comparisons 
            Weak Analogy, 
            Apples and Oranges, 
            Fallacy of Composition, 
            Aggregation Fallacy, 
        1.5.6) Fallacies of Overgeneralization 
            Hasty Generalization, 
            No-True-Scotsman,
            Wishful Thinking, 
            Fallacy of Accident,
        1.5.7) Contradictory Arguments 
            Self-Refutation, 
            Contradictory Argument, 
            Self-Contradiction, 
        1.5.8) Fallacies of Unfounded Assertions 
            Unsubstantiated Claims, 
            Ad Ignorantiam, 
        1.5.9) Dichotomies and Binary Thinking 
            False Dichotomy, 
            Conditional Fallacy, 

    1.6) Contradiction can be only Yes or No. Explain in explaination why you choice this type to statement, depends on logical errors classification, is it empty or not
    
    Analyse on Rhetorical Techniques, Propaganda Methods, Logical Errors, Contradictions, Polarity, Tonality only statement. Use justification only for extra comments  and extra explanation in a convenient way about statement (Use justification to better explanation of propaganda methods, rhetorical techniques in statement)
    """

    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": f"number: {num}\nstatement: {text_1}\njustification: {text_2}"}
        ]
    )
    input_text = chat_completion.choices[0].message.content
    #print(input_text)

    # Folder for saving files
    output_folder = dataset_name

    # Creating a folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Saving the contents to a file num.txt
    #with open(os.path.join(output_folder, f'{num}.txt'), 'w') as file:
        #file.write(input_text)
        #json.dump(input_text, file, indent=4)
    
    
    # Clearing the string of newline characters
    сleaned_text = input_text.replace("\n", "")
    
    # Looking for JSON files between "`json' and "`'
    json_files = re.findall(r'```json(.*?)```', сleaned_text)

    # Converting JSON strings to Python objects
    json_data = [json.loads(file.strip()) for file in json_files]
    
    # Saving the extracted data to files
    with open(os.path.join(output_folder,f'{num}.json'), 'w') as analysis_file:
        json.dump(json_data[0], analysis_file, indent=4)
    
    print(f"{num}: Files 'num.json' have been saved.")
    # Get the size of the files
    txt_size = os.path.getsize(os.path.join(output_folder, f'{num}.json'))

    # Output the file size in bytes
    print(f"Size of {num}.json: {txt_size} bytes")

    pass

def analyze_with_retries(num, text_1, text_2, max_retries=3):
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
###print(print_lines_in_sequence(file_path,0,1266)) #test
###print(print_lines_in_sequence(file_path,0,10239)) #train
###print(print_lines_in_sequence(file_path,0,1283)) #val