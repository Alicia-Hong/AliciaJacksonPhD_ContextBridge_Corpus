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

os.chdir(r'C:\Users\alici\OneDrive\Desktop\Python UI\UI')

# Set up basic configuration for logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

print("Before running app...")
app = Flask(__name__)

# Set OpenAI API Key securely
os.environ['OPENAI_API_KEY'] = 'xxxxxxxxxxxxxxxxxxxxxxxxx'#set up and insert your key
openai_api_key = os.environ.get('OPENAI_API_KEY')
app.secret_key = 'xxxxxxxxxxxxxxxxxxxxxxxxx'#set up and insert your key
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
    context_data=analysis_results[0].get('general context', [])
    emotion_data=analysis_results[1].get('emotional tone', [])
    culture_data=analysis_results[2].get('cultural cue', [])

    return render_template('result.html', context_data=context_data,emotion_data=emotion_data,culture_data=culture_data)

dialogue = str("秋菊: 村长，你这是啥意思 \n \
村长: 啥意思? 别人的钱不是那么好拿的 \n \
秋菊: 我今天来就不是图个钱的, 我是要个理 \n \
村长: 理? 你以为我软了 \n \
村长: 地下的钱一共二十张, 你拾一张给我低一回头 \n ")

background = str("农村妇女秋菊为了向踢伤丈夫的村长讨说法，不屈不挠逐级上告。")

def analyze_dialogue(dialogue, background):
    focus = [
        ('general context', '语境(一般背景)'),
        ('emotional tone', '情绪基调'),
        ('cultural cue', '文化标志以及与世界构建的微妙联系(文化线索)'),
    ]
    analysis_results = []
    for english_focus, chinese_focus in focus:
        result, result_json = ask_ChatGPT(dialogue, background, english_focus, chinese_focus)
        analysis_results.append(result_json)
       # logging.info(f'Focus: {english_focus}, Result: {result}')
       
    print(analysis_results)
    return analysis_results

def ask_ChatGPT(background, transcript, english_focus, chinese_focus):
    prompt = f"{background} 以上文作为对话背景，帮助我注释以下的对白，分析主要{english_focus}, \
   将这一个方面简练的英文注释放入json nested list object中 (当有特定文化词时引述中文词。 除所需输出之外不需要任何过渡性/结论性句子。): {transcript} "
    print("routing to GPT ...")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a helpful assistant. Your task is to analyze dialogue segments in its language for {english_focus}, based on the provided background.Output each utterance analysis in its own JSON object"},
                {"role": "user", "content": prompt}
            ],
            functions= [{"name":"set_response_format","parameters":{
                "type":"object",
                "properties":{
                f"{english_focus}":{
                    "type":"array",
                    "items":{
                        "type":"object",
                     "properties":{
                     "utterance":{"type":"string","description":"the original transcript sentence"},
                     "analysis":{"type":"string","description":"brief English analysis of the utterance"}
                    }}}}}}],
            temperature=0.3,
            top_p=0.2
            #max_tokens=4096
        )
        output_response = response.choices[0].message.function_call.arguments
        output_load = json.loads(output_response)
     #   logging.debug(f'Received response: {output_response}')
        return output_response, output_load
    except Exception as e:
      #  logging.error(f'Error processing OpenAI API request: {e}')
        return str(e)

if __name__ == '__main__':
    try:
        print("right before running app...")
        app.run(debug=True)
    except Exception as e:
        print("An exception occurred: ", e)
        print(traceback.format_exc())
        sys.exit(1)

print("After running app...")
