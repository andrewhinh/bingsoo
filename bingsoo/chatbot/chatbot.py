# Imports
import argparse
import json
import numpy as np
import os
import openai
import random
import requests

from dotenv import load_dotenv
from pathlib import Path
from PIL import Image
from transformers import CLIPProcessor, CLIPModel


# Variables
# HF Token / OpenAI API Key
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# OpenAI GPT-3 config
context_id = 100  # Random
question_id = 1005  # Random
n_shot = 16
n_ensemble = 1
gpt_max_tokens = 4097

# Computing similarity config
encoder = "openai/clip-vit-base-patch16"

# Context files
parent_dir = Path(__file__).resolve().parents[0] / "context"
random_img_for_clip = parent_dir / "img.jpg"
chatbot_dir = "chatbot"
training_idx_file = parent_dir / chatbot_dir / "train_idx.json"
training_context_file = parent_dir / chatbot_dir / "context.json"
training_question_features = parent_dir / chatbot_dir / "question_feature.npy"
training_context_features = parent_dir / chatbot_dir / "context_feature.npy"
training_question_file = parent_dir / chatbot_dir / "question.json"
training_answer_file = parent_dir / chatbot_dir / "answer.json"


# Main functions/classes
def process_answer(answer):
    to_be_removed = {""}
    answer_list = answer.split(" ")
    answer_list = [item for item in answer_list if item not in to_be_removed]
    return " ".join(answer_list)


class Reply:
  """
  Main question_answering class
  """

  def __init__(self, question_info, context_info, context_idx, question_text_embed, context_text_embed):
    self.question = question_info
    self.inputtext_dict = self.load_cachetext(context_info)
    (
        self.traincontext_context_dict,
        self.traincontext_answer_dict,
        self.traincontext_question_dict,
    ) = self.load_anno(
        training_context_file,
        training_answer_file,
        training_question_file,
        None,
    )
    self.train_keys = list(self.traincontext_answer_dict.keys())
    self.load_similarity(context_idx, question_text_embed, context_text_embed)
    
  def predict(self):
    _, _, question_dict = self.load_anno(None, None, None, self.question)

    key = list(question_dict.keys())[0]
    context_key = int(key.split("<->")[0])
    question, context = (
        question_dict[key],
        self.inputtext_dict[context_key],
    )

    context_key_list = self.get_context_keys(
        key,
        n_shot * n_ensemble,
    )

    # prompt format following GPT-3 QA API
    prompt = "Marv is a chatbot that reluctantly answers questions with sarcastic responses:\n\n"
    for ni in range(n_shot):
        if context_key_list is None:
            context_key = self.train_keys[random.randint(0, len(self.train_keys) - 1)]
        else:
            context_key = context_key_list[ni]
        context_id_key = int(context_key.split("<->")[0])

        while True:  # make sure get context with valid question and answer
            if (
                len(self.traincontext_question_dict[context_key]) != 0
                and len(self.traincontext_answer_dict[context_key][0]) != 0
            ):
                break
            context_key = self.train_keys[random.randint(0, len(self.train_keys) - 1)]
        prompt += (
            "Context: %s\n"
            % self.traincontext_context_dict[context_id_key][
                random.randint(
                    0,
                    len(self.traincontext_context_dict[context_id_key]) - 1,
                )]
        )
        prompt += "You: %s\nMarv: %s\n" % (
            self.traincontext_question_dict[context_key],
            self.traincontext_answer_dict[context_key],
        )

    prompt += "Context: %s\n" % context
    prompt += "You: %s\nMarv:" % question
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=60,
        top_p=0.3,
        frequency_penalty=0.5,
        presence_penalty=0.0
    )
    return process_answer(response["choices"][0]["text"])

  def get_context_keys(self, key, n):
      # combined with Q-similairty
      lineid = self.valkey2idx[key]
      question_similarity = np.matmul(self.train_feature, self.val_feature.detach().numpy()[lineid, :])
      # end of Q-similairty
      similarity = question_similarity + np.matmul(
          self.context_train_feature, self.context_val_feature.detach().numpy()[lineid, :]
      )
      index = similarity.argsort()[-n:][::-1]
      return [self.train_idx[str(x)] for x in index]

  def load_similarity(self, context_idx, question_feature, context_feature):
      val_idx = context_idx
      self.valkey2idx = {}
      for ii in val_idx:
            self.valkey2idx[val_idx[ii]] = int(ii)
      self.train_feature = np.load(training_question_features)
      self.val_feature = question_feature
      self.train_idx = json.load(
          open(
              training_idx_file,
              "r",
          )
      )
      self.context_train_feature = np.load(
          training_context_features
      )
      self.context_val_feature = context_feature
    
  def load_cachetext(self, context_info):
    idx = context_info["context_examples"][0]["context_id"]
    context = context_info["context_examples"][0]["context"]
    context_dict = {idx: context}
    return context_dict

  def load_anno(self, context_file, answer_anno_file, question_anno_file, questions):
    if context_file is not None:
        context = json.load(open(context_file, "r"))
        if isinstance(context, dict):
            context = context["context_examples"]
    if answer_anno_file is not None:
        answer_anno = json.load(open(answer_anno_file, "r"))
    if question_anno_file is not None:
        question_anno = json.load(open(question_anno_file, "r"))
    else:
        question_anno = questions

    context_dict = {}
    if context_file is not None:
        for sample in context:
            if sample["context_id"] not in context_dict:
                context_dict[sample["context_id"]] = [sample["context"]]
            else:
                context_dict[sample["context_id"]].append(sample["context"])
    answer_dict = {}
    if answer_anno_file is not None:
        for sample in answer_anno["answers"]:
            if str(sample["context_id"]) + "<->" + str(sample["question_id"]) not in answer_dict:
                answer_dict[str(sample["context_id"]) + "<->" + str(sample["question_id"])] = sample["answer"]
    question_dict = {}
    for sample in question_anno["questions"]:
        if str(sample["context_id"]) + "<->" + str(sample["question_id"]) not in question_dict:
            question_dict[str(sample["context_id"]) + "<->" + str(sample["question_id"])] = sample["question"]
    return context_dict, answer_dict, question_dict


class Answer:
    """
  Main inference class
  """

    def __init__(self):
        self.clip_model = CLIPModel.from_pretrained(encoder)
        self.clip_processor = CLIPProcessor.from_pretrained(encoder)

    def query(self, payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    def shorten_context(self, context, context_type):
        summarized_context = self.query({
            "inputs": context,
        })
        summarized_context = summarized_context[0]['summary_text']
        max_tokens = 128
        prompt = "Extract the exam dates, keywords, and names from this :"
        prompt += context_type + "\n\n"
        prompt += context[:gpt_max_tokens - max_tokens]
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=prompt,
            temperature=0,
            max_tokens=max_tokens,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return summarized_context, summarized_context + process_answer(response["choices"][0]["text"])
    
    def predict(self, question, context, context_type):
        basic_summary, enhanced_summary = self.shorten_context(context, context_type)

        # Generating features
        question_clip_input = self.clip_processor(text=[question], images=Image.open(random_img_for_clip), return_tensors="pt", padding=True)
        question_clip_output = self.clip_model(**question_clip_input)

        context_clip_input = self.clip_processor(text=[basic_summary[:77]], images=Image.open(random_img_for_clip), return_tensors="pt", padding=True)
        context_clip_output = self.clip_model(**context_clip_input)

        # Generating context idxs
        context_idx = {"0": str(context_id) + "<->" + str(question_id)}

        # Answering question
        question_info = {"questions": [{"context_id": context_id, "question": question, "question_id": question_id}]}
        context_info = {"context_examples": [{"context_id": context_id, "context": enhanced_summary}]}

        reply = Reply(
            question_info, context_info, context_idx, question_clip_output.text_embeds, context_clip_output.text_embeds,
        )  # Have to initialize here because necessary objects need to be generated

        return reply.predict()
  

def main():
    parser = argparse.ArgumentParser()

    # Inputs
    parser.add_argument("--question", type=str, required=True)
    parser.add_argument("--context", type=str, required=True)
    parser.add_argument("--context_type", type=str, required=True)
    args = parser.parse_args()

    # Answering question
    answer = Answer()
    return answer.predict(args.question, args.context, args.context_type)


if __name__ == "__main__":
    main()