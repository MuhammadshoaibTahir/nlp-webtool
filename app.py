from flask import Flask, render_template, request, send_file
import nltk
import spacy
nltk.data.path.append("./nltk_data")
from textblob import TextBlob
from langdetect import detect
from nltk.corpus import stopwords
from collections import Counter
from io import BytesIO
import os

from spacy import displacy

# Download required NLTK resources
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("averaged_perceptron_tagger")

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    output = {}

    if request.method == "POST":
        text = request.form["text"]
        blob = TextBlob(text)
        doc = nlp(text)

        tokens = nltk.word_tokenize(text)
        lemmatized = [token.lemma_ for token in doc]
        pos_tags = nltk.pos_tag(tokens)
        entities = [(ent.text, ent.label_) for ent in doc.ents]

        try:
            language = detect(text)
        except:
            language = "Could not detect"

        stop_words = set(stopwords.words("english"))
        filtered = [w for w in tokens if w.lower() not in stop_words]
        word_freq = Counter(filtered)

        dependencies = [(token.text, token.dep_, token.head.text) for token in doc]
        dep_svg = displacy.render(doc, style="dep", jupyter=False)

        # Sentiment timeline
        sentence_sentiments = []
        for i, sentence in enumerate(blob.sentences):
            sentence_sentiments.append({
                "sentence": str(sentence),
                "polarity": round(sentence.sentiment.polarity, 3),
                "subjectivity": round(sentence.sentiment.subjectivity, 3),
                "index": i + 1
            })

        output = {
            "tokens": tokens,
            "lemmatized": lemmatized,
            "pos_tags": pos_tags,
            "entities": entities,
            "language": language,
            "sentiment": {
                "polarity": round(blob.sentiment.polarity, 3),
                "subjectivity": round(blob.sentiment.subjectivity, 3)
            },
            "sentence_sentiments": sentence_sentiments,
            "summary": str(blob)[:300] + "...",
            "word_freq": word_freq.most_common(10),
            "noun_phrases": blob.noun_phrases,
            "dependencies": dependencies,
            "dep_svg": dep_svg
        }

    return render_template("index.html", output=output, text=text)

@app.route("/download", methods=["POST"])
def download():
    text = request.form["export_text"]
    buffer = BytesIO()
    buffer.write(text.encode("utf-8"))
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name="nlp_output.txt",
        mimetype="text/plain"
    )

if __name__ == "__main__":
    app.run(debug=True)