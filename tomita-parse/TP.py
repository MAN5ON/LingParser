import re
import subprocess
import time

from pymongo import MongoClient

def write_sentence_db(setneces_person,sentences_place, link):
    if setneces_person or  sentences_place :
        collection_sentence.insert_one({"link": link, "sentence_person": setneces_person, "sentence_places": sentences_place})


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

def getPlaces():
    places = []
    place = ""
    with open("facts.txt") as file:
        facts_text = file.read()
    s = re.sub(r'\s+', ' ', facts_text, flags=re.M)
    for s in re.split(r'(?<=[.!?…]) ', s):
        tmp = re.findall(r'Place {.*?}',s)
        for k in tmp:
            place = re.sub(r'[a-z]|[A-z]|=|{|}', "", k)
            k = ''
        if(place):
            places.append(place)
    places = deleteDuplicate(places)
    file.close()
    return places

def getPersons():
    persons = []
    person = ""
    with open("facts.txt") as file:
        facts_text = file.read()
    s = re.sub(r'\s+', ' ', facts_text, flags=re.M)
    for s in re.split(r'(?<=[.!?…]) ', s):
        tmp = re.findall(r'Person {.*?}',s)
        for k in tmp:
            person = re.sub(r'[a-z]|[A-z]|=|{|}', "", k)
            k = ''
        if(person):
            persons.append(person)
    persons = deleteDuplicate(persons)
    file.close()
    return persons

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

def insert_persons_on_db(persons):
    if persons:
        collection_persons.insert_one(
        {"persons": persons})

def insert_places_on_db(places):
    if places:
        collection_places.insert_one(
        {"places": places})


def finalyiDeleteDuplicate(list):
    res = ''
    list2 = []
    for i in list:
        if len(i) > 1:
            i = ",".join(i)
        res += ''.join(i) + ','
    res = res.title()
    res2 = res.split(',')
    clear_list = deleteDuplicate(res2)
    clear_list = clear_list[:-1]
    n = -1
    for i in clear_list:
        n += 1
        list2.append([])
        list2[n].append(i)
    return list2 #Двумерный список с очищенными дубликатами

def deleteDuplicate(l):
    n = []
    for i in l:
        if i not in n:
            n.append(i)
    return n

def tparse():
    persons=[]
    places = []
    n =1
    for t in collection.find():
        n+=1
        print(n)
        print(collection.find())
        link = t['link']
        try:
            text = t['text_stat']
        except KeyError:
            continue
        f = open('test.txt', 'w')
        f.write(text)
        f.close()
        subprocess.Popen(["/home/skellet/tomita-parser/build/bin/tomita-parser config.proto"], shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Вместо /home/skelllet/tomita-parser/build/bin/tomita-parser должно быть tomita-parser, но у меня не сработало
        time.sleep(0.7)#Без этого данные в бд отображаются неверно

        seteneces_person = getSentencePerson(link)
        if seteneces_person:
            persons.append(getPersons())
            persons=deleteDuplicate(persons)
            deleteExcess(seteneces_person)
        sentences_place = getSentencePlace(link)
        if sentences_place:
            places.append(getPlaces())
            places = deleteDuplicate(places)
            deleteExcess(sentences_place)
        write_sentence_db(seteneces_person, sentences_place, link)
    persons = finalyiDeleteDuplicate(persons)
    places = finalyiDeleteDuplicate(places)
    insert_persons_on_db(persons)
    insert_places_on_db(places)



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
    collection_persons = db.persons
    collection_places = db.places
    tparse()


