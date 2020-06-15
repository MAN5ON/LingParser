
from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://admin:admin@cluster0-y2po7.mongodb.net/vpravda"
mongo = PyMongo(app)

@app. route('/', methods=['GET'])
@app.route('/renat', methods=['GET'])
def index():
    cur = mongo.db.archive.find({}, {'link': 1, 'title': 1, 'text_stat': 1, 'time_date': 1, '_id': 0})
    return render_template('index.html', cur=list(cur))


@app.route('/ruslan', methods=['GET'])
def person():
    per = mongo.db.sentence.find({}, {'sentence_person': 1, 'sentence_places': 1, 'news_id': 1, '_id': 0})
    return render_template('ruslan.html', per=list(per))


if __name__ == "__main__":
    app.run(debug=True)