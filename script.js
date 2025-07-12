function analyzeText() {
  const text = document.getElementById("textInput").value.trim();
  if (!text) {
    alert("Please enter a sentence.");
    return;
  }

  const doc = nlp(text);
  const sentences = doc.sentences().out('array');
  const nounPhrases = doc.nouns().out('array');
  const verbs = doc.verbs();
  const negations = doc.match('#Negative');

  let output = `<h3>Analysis</h3>`;
  output += `<b>Total Sentences:</b> ${sentences.length}<br><br>`;

  sentences.forEach((s, i) => {
    const sDoc = nlp(s);
    const v = sDoc.verbs().data()[0];
    const tense = v ? v.tense : "Unknown";

    const hasNeg = sDoc.has('#Negative') ? 'Yes' : 'No';

    output += `<b>Sentence ${i + 1}:</b> ${s}<br>`;
    output += ` - Tense: ${tense}<br>`;
    output += ` - Negation: ${hasNeg}<br>`;
    output += `<hr>`;
  });

  output += `<b>Noun Phrases:</b> ${nounPhrases.join(', ') || 'None'}<br>`;
  output += `<b>Verbs:</b> ${verbs.out('array').join(', ') || 'None'}<br>`;
  output += `<b>Negation Words:</b> ${negations.out('array').join(', ') || 'None'}<br>`;

  document.getElementById("output").innerHTML = output;
}
