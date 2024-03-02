from json import load
import json
import nltk
import random
from nltk.stem.wordnet import WordNetLemmatizer

filepath = "./dataset/small_talk.json"

import json
import nltk

# Loading intents from JSON file
with open(filepath) as f:
  intents_data = json.load(f)


lemmatizer = WordNetLemmatizer()

def process_user_input(user_input):
  # Tokenizing the user input
  user_input = user_input.lower()
  user_input_tokens = nltk.word_tokenize(user_input)

  # Lemmatizing each token
  lemmatized_tokens = [lemmatizer.lemmatize(token) for token in user_input_tokens]
  user_input_processed = ' '.join(lemmatized_tokens)

  return user_input_processed

def find_matching_intent(user_input_processed):
  for intent in intents_data['intents']:
    for pattern in intent['patterns']:
      pattern = pattern.lower()
      pattern_tokens = nltk.word_tokenize(pattern)
      lemmatized_pattern_tokens = [lemmatizer.lemmatize(token) for token in pattern_tokens]
      pattern_processed = ' '.join(lemmatized_pattern_tokens)

      if user_input_processed == pattern_processed:
        return intent

  return None

def generate_response(intent):
  if intent is None:
    return "Sorry, I couldn't find a matching intent."

  response_index = random.randint(0, len(intent['responses']) - 1)
  response = intent['responses'][response_index]

  return response
