from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
import textstat

app = Flask(__name__)
CORS(app)

nlp = spacy.load("en_core_web_sm")

# Tense and aspect detection from tags
def detect_tense_aspect(sent):
    tense = "Unknown"
    aspect = "Simple"
    for tok in sent:
        if tok.tag_ in ["VBD", "VBN"]:
            tense = "Past"
        elif tok.tag_ in ["VBZ", "VBP", "VB"]:
            tense = "Present"
        elif tok.tag_ == "MD":
            tense = "Modal/Future"
        if tok.tag_ in ["VBG"]:
            aspect = "Progressive"
        if any(x.tag_ == "VBN" for x in sent) and any(x.text.lower() in ["have", "has", "had"] for x in sent):
            aspect = "Perfect"
        if aspect == "Perfect" and any(x.tag_ == "VBG" for x in sent):
            aspect = "Perfect Progressive"
    return tense, aspect

# Extract SVO triples
def extract_svo(sent):
    subject = object_ = verb = "-"
    for tok in sent:
        if tok.dep_ in ["nsubj", "nsubjpass"]:
            subject = tok.text
        if tok.dep_ == "dobj":
            object_ = tok.text
        if tok.pos_ == "VERB":
            verb = tok.text
    return f"{subject} → {verb} → {object_}"

# Detect negation
def detect_negation(sent):
    return "Yes" if any(tok.dep_ == "neg" for tok in sent) else "No"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    doc = nlp(text)
    results = []
    extra = {
        "np_chunks": [],
        "svo": [],
        "negation": [],
        "tense_aspect": [],
        "complexity": textstat.flesch_reading_ease(text)
    }

    for sent in doc.sents:
        tense, aspect = detect_tense_aspect(sent)
        svo = extract_svo(sent)
        neg = detect_negation(sent)

        extra["tense_aspect"].append(f"{tense} {aspect}")
        extra["svo"].append(svo)
        extra["negation"].append(neg)

    extra["np_chunks"] = [chunk.text for chunk in doc.noun_chunks]

    for token in doc:
        results.append({
            "text": token.text,
            "lemma": token.lemma_,
            "pos": token.pos_,
            "tag": token.tag_,
            "dep": token.dep_,
            "head": token.head.text,
            "ent": token.ent_type_ if token.ent_type_ else "-"
        })

    return jsonify({"tokens": results, "extra": extra})

if __name__ == "__main__":
    app.run(debug=True)
