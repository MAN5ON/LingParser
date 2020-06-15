from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
from pymongo import MongoClient

def classifier(messages = ['ds']):
    tokenizer = RegexTokenizer()
    tokens = tokenizer.split('всё очень плохо')
    model = FastTextSocialNetworkModel(tokenizer=tokenizer)
    results = model.predict(messages, k=2)
    for message, sentiment in zip(messages, results):
        print(message, '->', sentiment)
        return {
            'sentence': message,
            'sentiment': sentiment
        }

if __name__ == "__main__":
    client = MongoClient("mongodb+srv://admin:admin@cluster0-y2po7.mongodb.net/vpravda")
    db = client.vpravda
    collection_sentence = db.sentence
    collection_classify = db.classify
    print("Отношения высказываний к персонам: ")
    for sentence in collection_sentence.find():
        if (sentence['sentence_person']):
            persObj  = classifier(sentence['sentence_person'])
            persObj['link'] = sentence['link']
            collection_classify.insert_one(persObj)
    print("Отношения высказываний к местам и достопримечательностям: ")
    for sentence in collection_sentence.find():
        if (sentence['sentence_places']):
            placeObj  = classifier(sentence['sentence_places'])
            placeObj['link'] = sentence['link']
            collection_classify.insert_one(placeObj)