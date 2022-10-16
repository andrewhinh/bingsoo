# Running Marv
1. Run `python3 chatbot.py --question QUESTION --context CONTEXT`, replacing `QUESTION` and `CONTEXT`, OR
2. Add `from chatbot import Pipeline` to your imports, and interface with the model through `Pipeline.predict(QUESTION, CONTEXT)`.


# Improving Marv
1. Add more examples to `answer.json`, `context.json`, `question.json`, and `train_idx.json`.
2. Generate CLIP embeddings with `python3 feature_gen.py`.