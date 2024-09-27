# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 15:03:54 2024

Thesis GPT Finetuning

@author: jjack
"""
##########################################################

#Newest Job: id='ftjob-aLvBJPCfKpUgoiAeuOJ1fIoF

#FIRST ADD THE API KEY IN EXTERNAL VARIABLE
#Open Anaconda Prompt
#cd C:\Users\pjack\Desktop\Training Python Script
#set OPENAI_API_KEY=xxxxx
#spyder


import pandas as pd
import json
import openai
from pathlib import Path
from openai import OpenAI
import requests
import os

os.environ['OPENAI_API_KEY'] = 'xxxxx'
openai_api_key = os.environ.get('OPENAI_API_KEY')

client = OpenAI()

def format_row(transcripts, context_parsings, background, focus, focus_cn):
    # Aggregate transcripts and context_parsings into single strings
    transcripts_combined = " ".join(transcripts)
    # Combine transcripts and context parsings side by side, followed by a line break
    context_parsings_combined = '\n'.join([f"Transcript: {transcript}\n Analysis: {parsing}"
                                  for transcript, parsing in zip(transcripts, context_parsings)])


    # Define the user's message (transcript segment)
    user_message = {
        "role": "user",
        "content": f"'{background}' \
        以上文作为对话背景，帮助我注释以下的对白，分析主要{focus_cn}, \
        以表格格式将这一个方面作为附加的单元格将它们放在每个话语对应的单独列中：{transcripts_combined}"
    }

    # Define the assistant's response (analysis of the segment)
    assistant_message = {
        "role": "assistant",
        "content": context_parsings_combined 
    }

    # Structure the conversation with the system message, user message, and assistant message
    conversation = {
        "messages": [
            {"role": "system",  
             "content": f"You are a helpful assistant. Your task is to analyze dialogue segments in its language for {focus}, based on the provided background."
            },
            user_message,
            assistant_message
        ]
        
        
    }

    return conversation

def process_file(file_path, focus, focus_cn):
    # Load the Excel file
    data = pd.read_excel(file_path)

    # Initialize the list to hold formatted data
    formatted_data = []

    # Group by 'index'
    grouped = data.groupby('index')

    # Process each group
    for index, group in grouped:
        # Get the 'background' from the first row of the group
        background = group.iloc[0]['background']
        
          # Chunk the group into segments of up to 5 rows
        for start in range(0, len(group), 6):
            segment = group.iloc[start:start+6]
            transcripts = segment['transcript'].tolist()
            context_parsings = segment['context_parsing'].tolist()
            
            formatted_segment = format_row(transcripts, context_parsings, background, focus, focus_cn)
            formatted_data.append(formatted_segment)
  
    return formatted_data


def main():
    os.chdir(r'C:\Users\pjack\Desktop\model training\training - supervised')
    # Set your OpenAI API key
    #openai.api_key = 'xxxxx'
    
    # Define file paths and their corresponding focuses
    file_info = [
        ('trainingdata_context.xlsx', 'context', '语境(一般背景)', 'trainingdata_context_val.xlsx'),
        ('trainingdata_emotion.xlsx', 'emotion', '情绪基调', 'trainingdata_emotion_val.xlsx'),
        ('trainingdata_culture.xlsx', 'culture', '文化标志以及与世界构建的微妙联系(文化线索)', 'trainingdata_culture_val.xlsx'),
    ]

    all_formatted_data = []
    all_formatted_val_data = []

    # Process each file for its specific focus and accumulate the data
    for file_path, focus, focus_cn, val_file_path in file_info:
        # Process training file
        formatted_data = process_file(file_path, focus, focus_cn)
        all_formatted_data.extend(formatted_data)
        # Process validation file
        formatted_val_data = process_file(val_file_path, focus, focus_cn)
        all_formatted_val_data.extend(formatted_val_data)

    # Save the combined formatted data to a JSON Lines file
    with open('combined_training_data.jsonl', 'w') as file:
        for entry in all_formatted_data:
            json.dump(entry, file)
            file.write('\n')

    # Save the combined validation file to a JSON Lines file
    with open('combined_validation_data.jsonl', 'w') as val_file:
        for entry in all_formatted_val_data:
            json.dump(entry, val_file)
            val_file.write('\n')
                
    # Upload the training data
    response = openai.files.create(file=Path("combined_training_data.jsonl"), purpose='fine-tune')
    print(response)
    file_id = response.id
    
    # Upload the validation data
    val_response = openai.files.create(file=Path("combined_validation_data.jsonl"), purpose='fine-tune')
    val_file_id = val_response.id

    # Start the fine-tuning process
    fine_tune_response = client.fine_tuning.jobs.create(
        training_file=file_id,
        validation_file=val_file_id,
        model="gpt-3.5-turbo",
        suffix = "supervise4_ep4",     
        hyperparameters = {"n_epochs": 4, "learning_rate_multiplier": 1, "batch_size":1}
        #batch_size=4,
      
        # Other parameters as needed
    )
    print(fine_tune_response)
    
    fine_tune_response_id = fine_tune_response.id
    return fine_tune_response_id

def check_fine_tuning_status(job_id):
    try:
        status = client.fine_tuning.jobs.retrieve(job_id)
        job_status = status.json()  # Assuming the relevant info is under 'data'
        # Convert the string into a Python dictionary
        job_status_data = json.loads(job_status)      
        # Use json_normalize to flatten the dictionary and handle nested structures
        job_status_df = pd.json_normalize(job_status_data)    
        job_status_df['created_at'] = pd.to_datetime(job_status_df['created_at'], unit='s', errors='coerce')
        job_status_df['finished_at'] = pd.to_datetime(job_status_df['finished_at'], unit='s', errors='coerce')
        # Transpose the DataFrame to have keys in one column and values in another
        job_status_df = job_status_df.transpose().reset_index()
        job_status_df.columns = ['Key', 'Value']
        
        # Set pandas display option
        pd.set_option('display.width', 1000)
        print(f"Fine-Tuning Job Status: {job_status_df}")
    except Exception as e:
        print(f"Error checking job status: {e}")
        
if __name__ == "__main__":
    job_id = main()
    check_fine_tuning_status('job_id')


'''
Fine-Tuning Job Status: FineTuningJob(id='ftjob-29zV45F0lH6VIajvQaHDWket', 
created_at=1704861190, error=None, fine_tuned_model='ft:gpt-3.5-turbo-0613:personal::8fKnv1sb', finished_at=1704862110, 
hyperparameters=Hyperparameters(n_epochs=3, batch_size=1, learning_rate_multiplier=2), m
odel='gpt-3.5-turbo-0613', object='fine_tuning.job', organization_id='org-xxxxx', 

result_files=['file-9feBGyZCX7m8LtXWLPi5RRkT'], status='succeeded', trained_tokens=36984, 
training_file='file-FVlLZwJi9XrCSoS8L02cFjm7', validation_file=None)
'''
#check_fine_tuning_status('ftjob-aLvBJPCfKpUgoiAeuOJ1fIoF')
#check_fine_tuning_status('ftjob-HMSYx7zeV33sJTnFq2v3McZs')
#check_fine_tuning_status('ftjob-TvCXNqOwZypApDAWk5KcO8WI')

# Define the URL for listing fine-tuning jobs
url = 'https://api.openai.com/v1/fine_tuning/jobs'

# Make the GET request to the OpenAI API
response = requests.get(url, headers={"Authorization": f"Bearer {openai_api_key}"})

# Check if the request was successful
if response.status_code == 200:
    # Convert the JSON response to a DataFrame
    jobs_data = response.json()['data']  # Assuming the relevant info is under 'data'
    df = pd.DataFrame(jobs_data)
    
    df['created_at'] = pd.to_datetime(df['created_at'], unit='s', errors='coerce')
    df['finished_at'] = pd.to_datetime(df['finished_at'], unit='s', errors='coerce')
    
    # Set pandas options to display all columns and rows
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_colwidth', None)
    
    # Print the DataFrame
    print(df)
    df.to_csv('C:\\Users\\pjack\\Desktop\\model training\\model_log.csv')
else:
    # Print an error message if the request was not successful
    print(f"Failed to retrieve fine-tuning jobs. Status code: {response.status_code}, Response: {response.text}")


'''
####Test model on a new prompt
new_prompt = "沉香 精诚所至 金石为开 这八个字 你要时时牢记"
fine_tuned_model='ft:gpt-3.5-turbo-0125:personal:cccb-full-auto:96W1FBW9'
answer = client.chat.completions.create(
  model=fine_tuned_model,
  messages=[{"role": "system", "content": "You are a helpful assistant.Your task is to analyze dialogue for context, emotion, and cultural cues."},
              {"role": "user", "content": new_prompt}],
  max_tokens=1000,
  temperature=0
)
print(answer)
'''


