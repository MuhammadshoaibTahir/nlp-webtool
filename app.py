from flask import Flask, render_template, request, send_file
import nltk
import spacy
import os
from textblob import TextBlob
from langdetect import detect
from nltk.corpus import stopwords
from collections import Counter
from io import BytesIO
from spacy import displacy

# Ensure nltk_data path exists
nltk.data.path.append("nltk_data")
nltk.data.path.append("./nltk_data")

# Try downloading essential packages (safe version)
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")
try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")
try:
    nltk.data.find("taggers/averaged_perceptron_tagger")
except LookupError:
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

        sentence_sentiments = []
        for i, sentence in enumerate(blob.sentences):
            sentence_sentiments.append({
                "sentence": str(sentence),
                "polarity": round(sentence.sentiment.polarity, 3),
                "subjectivity": round(sentence.sentiment.subjectivity, 3),
                "index": i + 1
            })

        # Try extracting noun phrases (may fail if Brown corpus is missing)
        try:
            noun_phrases = blob.noun_phrases
        except Exception:
            noun_phrases = ["Error: Missing corpus for noun phrases."]

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
            "noun_phrases": noun_phrases,
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