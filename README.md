# Bridging The Context Gap: An LLM Fine-Tuning Framework for Context Parsing in Chinese Dialogues

This repository contains the data, code, and resources used in the thesis project "Bridging The Context Gap: An LLM Fine-Tuning Framework for Context Parsing in Chinese Dialogues". The project focuses on developing a novel approach to fine-tune Large Language Models (LLMs) for improved context understanding in Chinese dialogues as part of a PhD thesis dissertation.

## Repository Contents

1. **Training Data**
   - Movie scripts (primarily in Mandarin Chinese)
   - Metadata for the collected scripts
   - Annotation scheme used for data labeling

2. **Data Processing**
   - Preprocessed data with annotations and evaluation scores
   - Description of the data pipeline developed for annotation

3. **Model Training**
   - Python code used for model training
   - Configuration files and hyperparameters

4. **Evaluation**
   - Questionnaire developed for evaluation tasks
   - Evaluator demographics
   - R scripts for statistical analysis of model output and accuracy

5. **ContextBridge UI**
   - Demo picture of the ContextBridge user interface
   - Python scripts for the backend using Flask

## Data Collection and Annotation

The training data consists of movie scripts, predominantly in Mandarin Chinese. A custom data pipeline was developed to facilitate the annotation process. 100 evaluators were hired to ensure high-accuracy output for model training. The annotation scheme and metadata are provided to aid in understanding the data structure and labeling criteria.

The `training_data` directory contains preprocessed training data and metadata used for the model and statistical analysis. 

The Annotation Schemes are published here, following by the movie annotation outputs as well as individual evaluation scores: 
https://docs.google.com/spreadsheets/d/e/2PACX-1vSt3J_9BW7RtYn-Jnh5Ficc9udbZfm4Wq4Dn2fM0gEkmiLa8HLChNj_MJ08cx7oqdPaSia9gt4qL-jS/pubhtml

## Data Processing and Model Training

The `model_training` directory includes the python scripts used to train the model, along with any necessary configuration files.

The Data Training and Analysis Summaries are documented here: 
https://docs.google.com/spreadsheets/d/e/2PACX-1vS5Li6R9VDZmwwG8IvEriaiUVWVm06zfYEfswDaTmfLm7ozSFYuY09vCEtDII-IqpSm-jAXU0y2m-2x/pubhtml

## Evaluation

The `evaluation` directory contains a custom qualtrics questionnaire for the quality assurance and evaluation process. For transparency and reproducibility, R scripts used for statistical analysis of the model's output and accuracy metrics are included. Accuracy and loss data is collected through openai [Weights & Biases](https://docs.wandb.ai/guides/integrations/openai/) integration.
The model's highest validation accuracy reached 93.73%
![image](https://github.com/user-attachments/assets/3e8aa247-cdfb-47c1-8daf-38b2f29c3f94)

## ContextBridge UI

The `application` directory contains the source code for the ContextBridge UI, backend routing, and data feed configuration. 
The demo site is locally hosted and powered by the python package 'Flask'. 
Below are demo images showcasing the model's capabilities and the user interface design, including input and output views.

![ContextBridge UI Demo](application/ContextBRIDGE%20frontend.PNG)
![ContextBridge Process](application/ContextBRIDGE%20processed.png)

## Software
Data pipeline, finetuning and automation are scripted using Python 3.7 (Spyder) software.
Data analysis and statistical tests are completed using R 4.3.3 (Rstudio) software.

## Citation

If you use any of the resources from this project in your research, please cite using the following format:

```
@misc{Hong2024,
  author = {Hong, Alicia},
  title = {ContextBridge: A Corpus of Annotated Movie Scripts for Machine Learning},
  year = {2024},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/Alicia-Hong/AliciaJacksonPhD_ContextBridge_Corpus}}
}
```

## License

This project is made available under the MIT License, which permits commercial use, modification, distribution, and private use. This license does not provide any warranty.

## Contributing
Contributions to the dataset and scripts are welcome. Please fork the repository and submit pull requests for any enhancements.

## Contact

For any questions or inquiries about this project, please contact [Alicia Jackson] at [alicia.jnhong@gmail.com].

