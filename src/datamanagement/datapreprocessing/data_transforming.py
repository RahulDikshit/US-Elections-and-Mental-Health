# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline(
    "text-classification",
    model="SamLowe/roberta-base-go_emotions",
    device=0
    )
result = pipe("Happy for life!")
print(result)


model_configuration = {
                        "emotions":
                        {
                            "task": "text-classification", 
                            "model": "SamLowe/roberta-base-go_emotions",
                            "device": 0,
                        },
                        "fake-real":  {
                                 "task": "text-classification", 
                                 "model":"openai-community/roberta-base-openai-detector",
                                 "device": 0,
                            
                        },
                        "hate-no_hate":{
                                 "task": "text-classification",
                                 "model":"facebook/roberta-hate-speech-dynabench-r4-target",
                                 "device": 0,
                            },

                        "spam-ham": {
                                 "task": "text-classification",
                                 "model":"mshenoda/roberta-spam",
                                 "device": 0,
                            },
                        "sarcasm": 
                            {
                                 "task": "text-classification",
                                 "model":"helinivan/multilingual-sarcasm-detector",
                                 "device": 0,
                            },
                        "fake_news": {
                                 "task": "text-classification",
                                 "model":"mrm8488/bert-tiny-finetuned-fake-news-detection",
                                 "device": 0,
                        },
                        "toxicity": {

                                 "task": "text-classification",
                                 "model":"unitary/toxic-bert",
                                 "device": 0,
                        },
                        "offensive_detection": {
                                 "task": "text-classification",
                                 "model":"Hate-speech-CNERG/dehatebert-mono-English",
                                 "device": 0,
                        },
                        "argument": {
                                 "task": "text-classification",
                                 "model":"UKPLab/bert-base-argument-unit-classification",
                                 "device": 0,
                        },
                        "irony": {
                                 "task": "text-classification",
                                 "model":"SkolkovoInstitute/roberta-ironydetection",
                                 "device": 0,
                        },
                        "profanity": {
                                 "task": "text-classification",
                                 "model":"s-nlp/profanity-checker",
                                 "device": 0,
                        },
                        "subjectivity-objectivity ": {
                                 "task": "text-classification",
                                 "model":"modelsubjectivity/bart-large-mnli-subjectivity",
                                 "device": 0,
                        },
                        "intent": {
                                 "task": "text-classification",
                                 "model":"mrm8488/t5-base-finetuned-e2m-intent-detection",
                                 "device": 0,
                        },
                        "political_bias": {
                                 "task": "text-classification",
                                 "model":"evanmiller/political-bias-classifier",
                                 "device": 0,
                        },
                    }
                    