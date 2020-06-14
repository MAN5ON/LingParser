from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
from pymongo import MongoClient

def classifier(messages = ['Это анализатор текста из пакета']):
    tokenizer = RegexTokenizer()
    tokens = tokenizer.split('всё очень плохо')  # [('всё', None), ('очень', None), ('плохо', None)]
    model = FastTextSocialNetworkModel(tokenizer=tokenizer)
    results = model.predict(messages, k=2)
    for message, sentiment in zip(messages, results):
        print(message, '->', sentiment)

if __name__ == "__main__":
    client = MongoClient("mongodb+srv://admin:admin@cluster0-y2po7.mongodb.net/vpravda")
    db = client.vpravda
    collection_sentence = db.sentence
    print("Отношения высказываний к персонам: ")
    for sentence in collection_sentence.find():
        classifier(sentence['sentence_person'])
    print("Отношения высказываний к местам и достопримечательностям: ")
    for sentence in collection_sentence.find():
        classifier(sentence['sentence_places'])