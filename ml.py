def stem_sentence(stemmer, sentence):
    sentence = ' '.join([stemmer.stem(word) for word in sentence.split(' ')])
    return sentence

def stem(sentence):
    from nltk.stem.snowball import SnowballStemmer
    stemmer = SnowballStemmer('english')
    stemmed_corpus = stem_sentence(stemmer, sentence)
    return stemmed_corpus

def predict(sentence):
    import pickle
    log_filename = 'log_model.sav'
    vector_filename = 'vector.sav'
    loaded_model = pickle.load(open(log_filename, 'rb'))
    loaded_vector = pickle.load(open(vector_filename, 'rb'))

    stemmed = stem(sentence)    
    X = loaded_vector.transform([stemmed])

    prediction = loaded_model.predict(X)
    print(f'{stemmed}\n{prediction[0]}')

    return prediction