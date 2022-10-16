# Libraries
import json
import numpy as np
import requests
import openai
import os

from dotenv import load_dotenv
from pathlib import Path
from PIL import Image
from transformers import CLIPProcessor, CLIPModel


# Variables
# Keys
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

# Summarization
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Input paths
parent_dir = Path(__file__).resolve().parents[0] / "context"
training_question_file = parent_dir / "question.json"
training_context_file = parent_dir / "context.json"
random_img_for_clip = parent_dir / "img.jpg"

# Output paths
training_question_features = parent_dir / "question_feature.npy"
training_context_features = parent_dir / "context_feature.npy"

# CLIP config
encoder = "openai/clip-vit-base-patch16"
clip_model = CLIPModel.from_pretrained(encoder)
clip_processor = CLIPProcessor.from_pretrained(encoder)


# Main function
def main():
    question = json.load(open(training_question_file, "r"))
    if isinstance(question, dict):
        question = question["questions"][0]['question']

    context = json.load(open(training_context_file, "r"))
    if isinstance(context, dict):
        context = context["context_examples"][0]['context']

    summarized_context = query({"inputs": context})
    summarized_context = summarized_context[0]['summary_text']
    
    question_clip_input = clip_processor(text=[question], images=Image.open(random_img_for_clip), return_tensors="pt", padding=True)
    question_clip_output = clip_model(**question_clip_input)

    context_clip_input = clip_processor(text=[summarized_context], images=Image.open(random_img_for_clip), return_tensors="pt", padding=True)
    context_clip_output = clip_model(**context_clip_input)

    np.save(training_question_features, question_clip_output.text_embeds.detach().numpy())
    np.save(training_context_features, context_clip_output.text_embeds.detach().numpy())
    
    
if __name__ == "__main__":
  main()