import nltk


def extract_named_entity(entity, text):
    #Identifying and return the named entity of the specified type in the text
    text = text.lower().title()
    tagged_words = nltk.pos_tag(nltk.word_tokenize(text))
    tree = nltk.ne_chunk(tagged_words)

    for subtree in tree.subtrees():
        if subtree.label() == entity:
            return subtree.leaves()[0][0]

    return text.split()[0].capitalize()


def getName(entity, text):
    # Returning the specific entity name 
    named_entity = extract_named_entity(entity, text)
    if named_entity:
        return named_entity
    else:
        return text.split()[0].capitalize()

   
    
def current_names():
    return {"chatbot_name": "Bot","user_name": "User"}


