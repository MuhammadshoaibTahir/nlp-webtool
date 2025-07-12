import tkinter as tk
from tkinter import messagebox, scrolledtext
import spacy
import textstat

# Load SpaCy English model
nlp = spacy.load("en_core_web_sm")

# Detect tense and aspect
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
        if tok.tag_ == "VBG":
            aspect = "Progressive"
        if any(x.tag_ == "VBN" for x in sent) and any(x.text.lower() in ["have", "has", "had"] for x in sent):
            aspect = "Perfect"
        if aspect == "Perfect" and any(x.tag_ == "VBG" for x in sent):
            aspect = "Perfect Progressive"
    return tense, aspect

# Extract Subject-Verb-Object
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

# Detect Negation
def detect_negation(sent):
    return "Yes" if any(tok.dep_ == "neg" for tok in sent) else "No"

# Analyze text
def analyze_text():
    input_text = text_input.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("Input Error", "Please enter some text.")
        return

    doc = nlp(input_text)
    output_text.delete("1.0", tk.END)

    # Display overall readability score
    readability = textstat.flesch_reading_ease(input_text)
    output_text.insert(tk.END, f"📘 Readability Score: {readability:.2f}\n\n")

    # Display all noun phrases (once)
    np_chunks = ", ".join(chunk.text for chunk in doc.noun_chunks)
    output_text.insert(tk.END, f"📌 Noun Phrases: {np_chunks}\n\n")

    # Sentence-level analysis
    for sent in doc.sents:
        tense, aspect = detect_tense_aspect(sent)
        svo = extract_svo(sent)
        neg = detect_negation(sent)

        output_text.insert(tk.END, f"📝 Sentence: {sent.text.strip()}\n")
        output_text.insert(tk.END, f" - Tense/Aspect: {tense} {aspect}\n")
        output_text.insert(tk.END, f" - SVO Structure: {svo}\n")
        output_text.insert(tk.END, f" - Contains Negation: {neg}\n")
        output_text.insert(tk.END, "-" * 50 + "\n")

# GUI Setup
root = tk.Tk()
root.title("Sentence-Level English Analyzer")
root.geometry("900x700")

tk.Label(root, text="Enter English Text:", font=("Arial", 12)).pack(pady=5)
text_input = scrolledtext.ScrolledText(root, height=10, wrap=tk.WORD, font=("Arial", 11))
text_input.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

tk.Button(root, text="Analyze", command=analyze_text, font=("Arial", 12), bg="skyblue").pack(pady=10)

tk.Label(root, text="Analysis Output:", font=("Arial", 12)).pack(pady=5)
output_text = scrolledtext.ScrolledText(root, height=25, wrap=tk.WORD, font=("Consolas", 10))
output_text.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

root.mainloop()
