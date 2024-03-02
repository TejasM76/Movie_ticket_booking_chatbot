import nltk
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def get_feedback(user_input):
    
    user_input_tokens = word_tokenize(user_input)

    # Analyzing the sentiment of the user feedback
    sentiment_analyzer = SentimentIntensityAnalyzer()
    sentiment = sentiment_analyzer.polarity_scores(user_input)

    # Extracting sentiment scores from analyzer
    compound_score = sentiment['compound']
    positive_score = sentiment['pos']
    negative_score = sentiment['neg']

    # Generate feedback response
    if compound_score > 0:
        feedback_response = "Thank you for your positive feedback! We're glad you're enjoying our chatbot."
    elif compound_score < 0:
        feedback_response = "We appreciate your feedback. We'll work on improving the chatbot to better meet your needs."
    else:
        feedback_response = "Thank you for your feedback. We'll continue to enhance the chatbot's capabilities."

    return feedback_response


    
def store_feedback(username, feedback):
    # Formatting the feedback data with username and feedback
    formatted_feedback = f"Username: {username}\nFeedback: {feedback}\n\n"

    # Opening the feedback file in append mode to write the feedback in file
    with open('feedback.txt', 'a') as f:
        # storing the feedback to the file
        f.write(formatted_feedback)









