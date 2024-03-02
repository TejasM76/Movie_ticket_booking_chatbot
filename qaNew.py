import pandas as pd
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.snowball import SnowballStemmer

# Loading the dataset
data = pd.read_csv('dataset/QA.csv')

# Extracting questions and answers
questions = data['Question'].tolist()
answers = data['Answer'].tolist()

# Preprocessing the texts
def preprocess(text):
    text = text.lower()
    stemmer = SnowballStemmer('english')
    tokens = nltk.word_tokenize(text)
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return ' '.join(stemmed_tokens)

# Creating TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(tokenizer=preprocess)
# Transforming questions into TF-IDF vectors
question_vectors = tfidf_vectorizer.fit_transform(questions)

# Function to find matching answer
def find_answer(user_question):
    user_question = preprocess(user_question)
    user_question_vector = tfidf_vectorizer.transform([user_question])

    # Calculating cosine similarity between user question vector and all question vectors
    cosine_similarities = cosine_similarity(user_question_vector, question_vectors)
    highest_similarity_index = np.argmax(cosine_similarities)

    # Checking if the similarity is above the threshold
    if cosine_similarities[0, highest_similarity_index] >= 0.9:
        return answers[highest_similarity_index]
    else:
        return 'NO RECORD FOUND'

'''# user input
user_question = input("Enter your question: ")

# Finding matching answer
answer = find_answer(user_question)

# Printing the answer
print(answer)'''






