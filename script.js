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

  let output = `📝 Total Sentences: ${sentences.length}\n\n`;

  sentences.forEach((s, i) => {
    const sDoc = nlp(s);
    const v = sDoc.verbs().data()[0];
    const tense = v ? v.tense : "Unknown";
    const hasNeg = sDoc.has('#Negative') ? 'Yes' : 'No';

    output += `Sentence ${i + 1}:\n`;
    output += `• ${s}\n`;
    output += `  - Tense: ${tense}\n`;
    output += `  - Negation: ${hasNeg}\n\n`;
  });

  output += `🔍 Noun Phrases: ${nounPhrases.join(', ') || 'None'}\n`;
  output += `🔍 Verbs: ${verbs.out('array').join(', ') || 'None'}\n`;
  output += `🔍 Negation Words: ${negations.out('array').join(', ') || 'None'}\n`;

  document.getElementById("output").innerText = output;
}
