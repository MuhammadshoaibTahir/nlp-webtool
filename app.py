from flask import Flask, render_template, request
import spacy
from textblob import TextBlob
from langdetect import detect
import textstat
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from collections import Counter
from wordcloud import WordCloud
import os
import matplotlib.pyplot as plt
from spacy import displacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.datasets import fetch_20newsgroups
from sklearn.model_selection import train_test_split
import uuid

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

# Utility functions
def clean_text(text):
    tokens = word_tokenize(text.lower())
    return [t for t in tokens if t.isalpha() and t not in stopwords.words('english')]

def topic_modeling(text):
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform([text])
    lda = LatentDirichletAllocation(n_components=1, random_state=0)
    lda.fit(X)
    topic = lda.components_[0]
    words = vectorizer.get_feature_names_out()
    return [words[i] for i in topic.argsort()[-5:]]

def classify_text(text):
    try:
        data = fetch_20newsgroups(subset='train', categories=['sci.space', 'comp.graphics', 'rec.autos'], remove=('headers', 'footers', 'quotes'))
        model = make_pipeline(CountVectorizer(), MultinomialNB())
        model.fit(data.data, data.target)
        prediction = model.predict([text])[0]
        return data.target_names[prediction]
    except Exception as e:
        return "Error in classification"

def keyword_extraction(text, top_n=10):
    words = clean_text(text)
    freq = Counter(words)
    return freq.most_common(top_n)

def text_statistics(text):
    words = word_tokenize(text)
    sentences = sent_tokenize(text)
    avg_word_length = sum(len(word) for word in words if word.isalpha()) / len(words) if words else 0
    return {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "avg_word_length": round(avg_word_length, 2)
    }

def passive_voice_detection(text):
    doc = nlp(text)
    passive_sentences = [sent.text for sent in doc.sents if any(tok.dep_ == "auxpass" for tok in sent)]
    return passive_sentences

@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    result = {}
    if request.method == "POST":
        text = request.form["text"]
        blob = TextBlob(text)
        doc = nlp(text)

        result["pos_tags"] = blob.tags
        result["entities"] = [(ent.text, ent.label_) for ent in doc.ents]
        result["dep_svg"] = displacy.render(doc, style="dep", jupyter=False, page=False)
        result["ent_svg"] = displacy.render(doc, style="ent", jupyter=False, page=False)

        result["language"] = detect(text)
        result["sentiment"] = {
            "polarity": round(blob.sentiment.polarity, 3),
            "subjectivity": round(blob.sentiment.subjectivity, 3)
        }
        result["readability"] = {
            "flesch": textstat.flesch_reading_ease(text),
            "fk_grade": textstat.flesch_kincaid_grade(text),
            "smog": textstat.smog_index(text)
        }
        result["topics"] = topic_modeling(text)
        result["classification"] = classify_text(text)
        result["keywords"] = keyword_extraction(text)
        result["text_stats"] = text_statistics(text)
        result["passive_voice"] = passive_voice_detection(text)
        result["corrected_text"] = str(blob.correct())

        # Create unique file name to avoid overwriting
        image_id = uuid.uuid4().hex

        # Generate WordCloud
        tokens = clean_text(text)
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(tokens))
        wordcloud_path = os.path.join("static", f"wordcloud_{image_id}.png")
        wordcloud.to_file(wordcloud_path)
        result["wordcloud_img"] = wordcloud_path

        # Sentiment Plot
        plt.figure()
        plt.bar(["Polarity", "Subjectivity"], [blob.sentiment.polarity, blob.sentiment.subjectivity], color=["blue", "orange"])
        plt.ylim(-1, 1)
        plt.title("Sentiment Scores")
        sentiment_path = os.path.join("static", f"sentiment_{image_id}.png")
        plt.savefig(sentiment_path)
        plt.close()
        result["sentiment_img"] = sentiment_path

    return render_template("index.html", text=text, result=result)

if __name__ == "__main__":
    app.run(debug=True)