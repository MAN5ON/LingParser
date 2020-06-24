from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://admin:admin@cluster0-y2po7.mongodb.net/vpravda"
mongo = PyMongo(app)


@app.route('/', methods=['GET'])
@app.route('/renat', methods=['GET'])
def index():
    cur = mongo.db.archive.find({}, {'link': 1, 'title': 1, 'text_stat': 1, 'time_date': 1, '_id': 0})
    return render_template('Renat.html', cur=list(cur))


@app.route('/ruslan', methods=['GET'])
def person():
    per = mongo.db.sentence.find({}, {'sentence_person': 1, 'sentence_places': 1, 'news_id': 1, '_id': 0})
    return render_template('Ruslan.html', per=list(per))


@app.route('/ruslanchik', methods=['GET'])
def synonyms():
    syn = mongo.db.synonyms.find({}, {'places': 1, 'person': 1, 'synonyms': 1, '_id': 0})
    return render_template('Ruslanchik.html', syn=list(syn))


@app.route('/vlad', methods=['GET'])
def classyfic():
    cly = mongo.db.classify.find({}, {'sentence': 1, 'sentiment': 1, 'link': 1, '_id': 0})
    return render_template('Vlados.html', cly=list(cly))


if __name__ == "__main__":
    app.run(debug=True)
