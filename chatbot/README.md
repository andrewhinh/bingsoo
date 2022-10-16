# Marv
A helpful (but sarcastic) chat bot to answer all of your course questions.

## Running Marv
1. Run `python3 chatbot.py --question QUESTION --context CONTEXT --context_type CONTEXT_TYPE`, replacing `QUESTION`, `CONTEXT`, and `CONTEXT_TYPE` OR
2. Add `from chatbot import Pipeline` to your imports, and interface with the model through `Pipeline.predict(QUESTION, CONTEXT, CONTEXT_TYPE)`.

## Improving Marv
1. Add more examples to files in context/: `answer.json`, `context.json`, `question.json`, and `train_idx.json`.
2. Generate CLIP embeddings (`*.npy` files) with `python3 feature_gen.py`.