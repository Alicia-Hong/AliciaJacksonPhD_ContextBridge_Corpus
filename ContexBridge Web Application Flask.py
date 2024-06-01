# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 09:55:17 2024

@author: jjack
"""
import logging
from flask import Flask, render_template, request, flash, redirect, url_for
from openai import OpenAI
import os
import json
import sys
import traceback

os.chdir(r'C:\Users\pjack\Desktop\Training Python Script\UI')

# Set up basic configuration for logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

print("Before running app...")
app = Flask(__name__)1

# Set OpenAI API Key securely
os.environ['OPENAI_API_KEY'] = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'#set up and insert your key
openai_api_key = os.environ.get('OPENAI_API_KEY')
app.secret_key = 'xxxxxxxxxxxxxxxxxxxxx'#set up and insert your key
client = OpenAI()

@app.route('/')
def index():
    logging.info('Rendering index page')
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    dialogue = request.form.get('dialogue', '')
    background = request.form.get('background', '')
    logging.info(f'Processing dialogue with background: {background}')
   # if not dialogue or not background:  # Check if dialogue or background is empty
     #  flash('Dialogue and background are required!', 'error')
      # return redirect(url_for('index'))  # Redirect back to the form page

    analysis_results = analyze_dialogue(dialogue, background)
    # Extract context, culture, and emotion data from the analysis_results
    context_data = analysis_results.get('context', [])
    context_data = json.loads(context_data)
    emotion_data = analysis_results.get('emotion', [])
    emotion_data = json.loads(emotion_data)
    culture_data = analysis_results.get('culture', [])
    culture_data = json.loads(culture_data)
    utterance_data = [{"utterance": line} for line in dialogue.split('\n')]
    return render_template('result.html', context_data=context_data, culture_data=culture_data, emotion_data=emotion_data)

dialogue = str("秋菊: 村长，你这是啥意思 \n \
村长: 啥意思? 别人的钱不是那么好拿的 \n \
秋菊: 我今天来就不是图个钱的, 我是要个理 \n \
村长: 理? 你以为我软了 \n \
村长: 地下的钱一共二十张, 你拾一张给我低一回头 \n ")

background = str("农村妇女秋菊为了向踢伤丈夫的村长讨说法，不屈不挠逐级上告。")

def analyze_dialogue(dialogue, background):
    focus = [
        ('context', '语境(一般背景)'),
        ('emotion', '情绪基调'),
        ('culture', '文化标志以及与世界构建的微妙联系(文化线索)'),
    ]
    analysis_results = {}
    for english_focus, chinese_focus in focus:
        result = ask_ChatGPT(dialogue, background, english_focus, chinese_focus)
        analysis_results[english_focus] = result
       # logging.info(f'Focus: {english_focus}, Result: {result}')
       
    print(analysis_results)
    return analysis_results

# Function to reformat data for template rendering
def reformat_data_for_template(analysis_results):
    formatted_data = {
        'context': [],
        'culture': {},
        'emotion': {}
    }

    # Reformat context data
    for item in analysis_results['context']:
        formatted_data['context'].append({
            'utterance': item[0],
            'context': item[0][0]
        })

    # Reformat culture data
    for item in analysis_results['culture']:
        formatted_data['culture'][item['utterance']] = item['analysis']

    # Reformat emotion data
    for item in analysis_results['emotion']:
        formatted_data['emotion'][item['character']] = item['emotion']

    return formatted_data

# Reformat the data
formatted_data = reformat_data_for_template(analysis_results)

# Sample usage with a string that contains all the keywords
sample_data = """
{
  "utterance": "秋菊: 村长，你这是啥意思",
  "context": "秋菊向村长询问其意图或用意",
  "culture": {"markers": ["marker1", "marker2"]},
  "emotion": "determined"
}
"""

# Call the function and print the result
data = extract_data_from_string(sample_data)
print(json.dumps(data, indent=2, ensure_ascii=False))


def ask_ChatGPT(background, transcript, english_focus, chinese_focus):
    prompt = f"{background} 以上文作为对话背景，帮助我注释以下的对白，分析主要{english_focus}, \
   将这一个方面将它们放在单独列中 (无需添加对白, 除所需输出之外的任何过渡性/结论性句子。): {transcript}"
    print("routing to GPT ...")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a helpful assistant. Your task is to analyze dialogue segments in its language for {english_focus}, based on the provided background.Output each utterance analysis in its own JSON object"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            top_p=0.2
           # max_tokens=4096
        )
        output_response = response.choices[0].message.content
     #   logging.debug(f'Received response: {output_response}')
        return output_response
    except Exception as e:
      #  logging.error(f'Error processing OpenAI API request: {e}')
        return str(e)

if __name__ == '__main__':
    try:
        print("right before running app...")
        app.run(debug=True)
    except Exception as e:
        print("An exception occurred:")
        print(traceback.format_exc())
        sys.exit(1)

print("After running app...")
