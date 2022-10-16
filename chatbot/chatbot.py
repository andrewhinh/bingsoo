# Imports
import argparse
import json
import os
import openai
from dotenv import load_dotenv
from pathlib import Path


# Variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
question_file = Path(__file__).resolve().parents[0] / "context.json"


# Main classes
class Reply:
  """
  Main inference class
  """

  def __init__(self):
    self.start = "Marv is a chatbot that reluctantly answers questions with sarcastic responses:\n\n"
    self.context = []
    context_questions = json.load(open(question_file, "r"))
    for dic in context_questions['qapairs']:
      self.context.append(dic['question'] + dic['answer'])
    self.end = "\nMarv:"

  def process_answer(self, answer):
      to_be_removed = {""}
      answer_list = answer.split(" ")
      answer_list = [item for item in answer_list if item not in to_be_removed]
      return " ".join(answer_list)

  def predict(self, question):
    prompt = self.start + "".join(self.context) + question + self.end
    response = openai.Completion.create(
      model="text-davinci-002",
      prompt=prompt,
      temperature=0.5,
      max_tokens=60,
      top_p=0.3,
      frequency_penalty=0.5,
      presence_penalty=0.0
    )
    return self.process_answer(response["choices"][0]['text'])


def main():
  parser = argparse.ArgumentParser()

  # Inputs
  parser.add_argument("--question", type=str, required=True)
  args = parser.parse_args()

  # Answering question
  reply = Reply()
  answer = reply.predict(args.question)
  print(answer)
  return answer


if __name__ == "__main__":
  main()