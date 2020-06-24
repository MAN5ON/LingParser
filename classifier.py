from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
from pymongo import MongoClient

def classifier(messages = ['ds']):
    tokenizer = RegexTokenizer()
    tokens = tokenizer.split('всё очень плохо')
    model = FastTextSocialNetworkModel(tokenizer=tokenizer)
    results = model.predict(messages, k=2)
    resSents = []
    for message, sentiment in zip(messages, results):
        print(message, '->', sentiment)
        resSents.append({
            'sentence': message,
            'sentiment': sentiment
        })
    return resSents

if __name__ == "__main__":
    client = MongoClient("mongodb+srv://admin:admin@cluster0-y2po7.mongodb.net/vpravda")
    db = client.vpravda
    collection_sentence = db.sentence
    collection_classify = db.classify
    print("Отношения высказываний: ")
    for sentence in collection_sentence.find():
        mySentMass = []
        link = sentence['link']
        nameCell = ''
        if ('sentence_person' in sentence.keys()):
            nameCell = 'sentence_person'
        elif ('sentence_places' in sentence.keys()):
            nameCell = 'sentence_places'
        mySentMass = classifier(sentence[nameCell])
        for oneSent in mySentMass:
            myObj = oneSent
            oneSent['link'] = link
            collection_classify.insert_one(myObj)