Bridging The Context Gap: An LLM Fine-Tuning Framework for Context Parsing in Chinese Dialogues
This repository contains the data, code, and resources used in the thesis project "Bridging The Context Gap: An LLM Fine-Tuning Framework for Context Parsing in Chinese Dialogues". The project focuses on developing a novel approach to fine-tune Large Language Models (LLMs) for improved context understanding in Chinese dialogues.
Repository Contents

Training Data

Movie scripts (primarily in Mandarin Chinese)
Metadata for the collected scripts
Annotation scheme used for data labeling


Data Processing

Python scripts for data preprocessing
Description of the data pipeline developed for annotation


Model Training

Python code used for model training
Configuration files and hyperparameters


Evaluation

Questionnaire developed for evaluation tasks
R scripts for statistical analysis of model output and accuracy


ContextBridge UI

Demo picture of the ContextBridge user interface



Data Collection and Annotation
The training data consists of movie scripts, predominantly in Mandarin Chinese. A custom data pipeline was developed to facilitate the annotation process. 100 evaluators were hired to ensure high-accuracy output for model training. The annotation scheme and metadata are provided to aid in understanding the data structure and labeling criteria.
Data Processing and Model Training
The data_processing directory contains Python scripts used for preprocessing the raw data. The model_training directory includes the code used to train the model, along with any necessary configuration files.
Evaluation
The evaluation process involved a custom questionnaire, which can be found in the evaluation directory. For transparency and reproducibility, we've included R scripts used for statistical analysis of the model's output and accuracy metrics.
ContextBridge UI
While the source code for the ContextBridge UI is not included in this repository, we've provided a demo picture to showcase the model's capabilities and the user interface design.
Show Image
Usage
To use the resources in this repository:

Clone the repository
Install the required dependencies (list provided in requirements.txt)
Follow the instructions in each directory for specific usage guidelines

Citation
If you use any of the resources from this project in your research, please cite:
Copy[Citation information for your thesis]
License
[Include appropriate license information here]
Contact
For any questions or inquiries about this project, please contact [Your Name] at [Your Email].













# AliciaJacksonPhD_ContextBridge_Corpus
Sharing dataset curated for my PhD Thesis Work CCCCB "Context Bridge"

Dissertation Title: Bridging The Context Gap:
An LLM Fine-Tuning Framework for Emotional and Cultural Parsing in Chinese Movie Dialogues

Data will be added iteratively from April-June 2024



The Annotation Schemes are published here: 
https://docs.google.com/spreadsheets/d/e/2PACX-1vSt3J_9BW7RtYn-Jnh5Ficc9udbZfm4Wq4Dn2fM0gEkmiLa8HLChNj_MJ08cx7oqdPaSia9gt4qL-jS/pubhtml

The Data Training and Analysis Summaries are documented here: 
https://docs.google.com/spreadsheets/d/e/2PACX-1vS5Li6R9VDZmwwG8IvEriaiUVWVm06zfYEfswDaTmfLm7ozSFYuY09vCEtDII-IqpSm-jAXU0y2m-2x/pubhtml


Data pipeline, finetuning and automation are scripted using Python 3.7 (Spyder) software.
Data analysis and statistical tests are completed using R 4.3.3 (Rstudio) software.

Please email Alicia jjackson9@my.harrisburgu.edu for any questions.
