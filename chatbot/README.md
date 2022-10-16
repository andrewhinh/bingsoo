# Marv
A helpful (but sarcastic) chat bot to answer all of your course questions.

## Running Marv
1. Add the following imports:
- `from context_type import FindType`
- `from utils.get_context import getSyllabuses, getAssignments`
- `from chatbot import Answer`
2. Given a `QUESTION`, interface with the model with the following:
- `CONTEXT_TYPE = FindType().predict(QUESTION)`
- `CONTEXT = getSyllabuses() if CONTEXT_TYPE=="syllabus" else getAssignments()`
- `ANSWER = Answer().predict(QUESTION, CONTEXT, CONTEXT_TYPE)`

## Improving Marv
1. Add more examples to files in 
- context/chatbot: `answer.json`, `context.json`, `question.json`, and `train_idx.json`
- context/class: `answer.json`, `question.json`, and `train_idx.json`
2. Generate CLIP embeddings (`*.npy` files) with `python3 chatbot/feature_gen.py`.