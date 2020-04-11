# coding utf-8
# docker run --name flask -p 5000:5000 -v G:\workspace:/flask -it python bash
# export FLASK_APP="server.py"
# flask run --host=0.0.0.0
# or python -m forever.run -t 1000000 python server.py &
from flask import Flask, jsonify
import feedparser

from flair.data import build_japanese_tokenizer, Sentence
from flair.models import TextClassifier


app = Flask(__name__)
classifier = TextClassifier.load('resources/best-model.pt')
japanese_tokenizer = build_japanese_tokenizer()

def get_score(text):
    # create example sentence
    sentence = Sentence(text, use_tokenizer=japanese_tokenizer)
    # predict class and print
    classifier.predict(sentence)

    label_dict = sentence.to_dict()["labels"][0]
    
    return label_dict["confidence"] if label_dict["value"] == "__label__O" else 0


def get_feed():
    RSS_URL = "https://www.lifehacker.jp/feed/index.xml"
    feed = feedparser.parse(RSS_URL)

    before_score = 0
    response_message = ""
    for entry in feed.entries:
        score = get_score(entry.title)
        print(entry.title, score)
        if score > before_score :
            before_score = score
            response_message = entry.title
    return response_message

@app.route('/')
def get_message():
    return jsonify(
        {'args':{'message': get_feed()}}
    )

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)