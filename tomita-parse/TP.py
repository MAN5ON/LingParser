import re
import subprocess
import time
from pymongo import MongoClient

def write_sentence_db(setneces_person,sentences_place, news_id):
    if setneces_person or  sentences_place :
        collection_sentence.insert_one({"news_id": news_id, "sentence_person": setneces_person, "sentence_places": sentences_place})


def getSentencePerson(news_id):
    sentences = []
    sentences_suitable_person = []
    with open("facts.txt") as file:
        facts_text = file.read()
    s = re.sub(r'\s+', ' ', facts_text, flags=re.M)
    i = 0
    for s in re.split(r'(?<=[.!?…]) ', s):
        sentences.append(s)
        if (bool(re.search(r'Person { Name ', sentences[i])) == True):
            sentences_suitable_person.append(sentences[i - 1])
        i += 1

    file.close()
    return sentences_suitable_person

def getSentencePlace(news_id):
    sentences = []
    sentences_suitable_places = []
    with open("facts.txt") as file:
        facts_text = file.read()
    s = re.sub(r'\s+', ' ', facts_text, flags=re.M)
    i = 0
    for s in re.split(r'(?<=[.!?…]) ', s):
        sentences.append(s)
        if (bool(re.search(r'Place { Name ', sentences[i])) == True):
            sentences_suitable_places.append(sentences[i - 1])
        i += 1

    file.close()
    return sentences_suitable_places


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
        seteneces_person = getSentencePerson(news_id)
        if seteneces_person:
            deleteExcess(seteneces_person)
        sentences_place = getSentencePlace(news_id)
        if sentences_place:
            deleteExcess(sentences_place)
        write_sentence_db(seteneces_person, sentences_place, news_id)

def deleteExcess(sentence):
    k = -1
    for i in sentence:
        k+=1
        excess = re.findall("Person.*}|Place.*}", i)
        excess_toString = ''.join(excess)
        if excess_toString:
            sentence[k] = re.sub(excess_toString, '', sentence[k])



if __name__ == '__main__':
    client = MongoClient("mongodb+srv://admin:admin@cluster0-y2po7.mongodb.net/vpravda")
    db = client.vpravda
    collection = db.archive
    collection_sentence = db.sentence
    tparse()


