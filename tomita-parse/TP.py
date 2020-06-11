import re
import subprocess
import time
from pymongo import MongoClient

def write_sentence_db(sentences_suitable, news_id):
    if sentences_suitable:
        collection_sentence.insert_one({"news_id": news_id, "sentence": sentences_suitable})


def getSentence(news_id):
    sentences = []
    sentences_suitable = []
    with open("facts.txt") as file:
        facts_text = file.read()
    s = re.sub(r'\s+', ' ', facts_text, flags=re.M)
    i = 0
    for s in re.split(r'(?<=[.!?…]) ', s):
        sentences.append(s)
        if (bool(re.search(r'Person { Name ', sentences[i])) == True):
            sentences_suitable.append(sentences[i - 1])
        i += 1

    write_sentence_db(sentences_suitable, news_id)
    file.close()


def tparse():
    for t in collection.find():
        print(collection.find())
        news_id = t['_id']
        try:
            text = t['text_stat']
        except KeyError:
            continue
        f = open('test.txt', 'w')
        f.write(text)
        f.close()
        subprocess.Popen(["/home/skelllet/tomita-parser/build/bin/tomita-parser config.proto"], shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Вместо /home/skelllet/tomita-parser/build/bin/tomita-parser должно быть tomita-parser, но у меня не сработало
        time.sleep(0.7)#Без этого данные в бд отображаются неверно
        getSentence(news_id)


if __name__ == '__main__':
    client = MongoClient("mongodb+srv://admin:admin@cluster0-y2po7.mongodb.net/vpravda")
    db = client.vpravda
    collection = db.archive
    collection_sentence = db.sentence
    tparse()


