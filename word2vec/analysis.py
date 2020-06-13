import os
from pyspark.sql import SparkSession
from pyspark.ml.feature import Word2VecModel
from pprint import pprint

import word2vec
from pymongo import MongoClient

def save_text_on_txt(collection):
    f = open('text.txt', 'a')
    for i in collection.find():
        try:
            text = i['text_stat']
        except KeyError:
            continue
        f.write(text)
    f.close()
    print("Данные из бд добавлены в text.txt")


def get_synonyms(elements, count, model, spark_session):
    result = []
    for element in elements:
        try:
            elementDF = spark_session.createDataFrame([
                (element[0].lower().split(" "),)], ["words"])
            transform_elem = model.transform(elementDF)
            synonyms = model.findSynonyms(transform_elem.collect()[0][1], count).collect()
            result.append(synonyms)
        except Exception:
            result.append("Синонимы не найдены")

    return result

def getPerson():
    for i in collection.find():
        try:
            persons = i['sentence_person']
        except KeyError:
            continue
    return persons


def getPlace():
    for i in collection.find():
        try:
            place = i['sentence_places']
        except KeyError:
            continue
    return  place

def print_elem(elements, elements_synonyms):
    for i in range(len(elements_synonyms)):
        pprint("-" * 30)
        pprint(elements[i][0])
        for el in elements_synonyms[i]:
            print(el[0])

PATH = 'model/data/'


def createModel():
    if (not os.path.exists('model')):
        os.mkdir('model')
        if (os.stat("text.txt").st_size == 0):
            save_text_on_txt(collection)

        word2vec.create_w2v_model()

    # persons = getPerson()
    # places = getPlace()
    #
    # spark = SparkSession \
    #     .builder \
    #     .appName("SimpleApplication") \
    #     .getOrCreate()
    #
    #
    # model = Word2VecModel.load(PATH)
    #
    # pprint("Поиск контекстных синонимов персон:")
    # persons_synonyms = get_synonyms(persons, 5, model, spark)
    # print_elem(persons, persons_synonyms)
    #
    # pprint("Поиск контекстных синонимов достопримечательностей:")
    # places_synonyms = get_synonyms(places, 5, model, spark)
    # print_elem(places, places_synonyms)
    #
    # spark.stop()


if __name__ == '__main__':
    client = MongoClient("mongodb+srv://admin:admin@cluster0-y2po7.mongodb.net/vpravda")
    db = client.vpravda
    collection = db.archive
    createModel()