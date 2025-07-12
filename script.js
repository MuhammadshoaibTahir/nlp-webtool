document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("analyzeBtn").addEventListener("click", analyzeText);
});

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
  const topics = doc.topics().out('array');

  const wordList = doc.terms().out('array');
  const lemmas = doc.terms().data().map(t => `${t.text} → ${t.normal}`);
  const syllables = wordList.map(w => `${w} (${syllable(w)})`).join(', ');

  let output = `📝 Total Sentences: ${sentences.length}\n\n`;

  sentences.forEach((s, i) => {
    const sDoc = nlp(s);
    const v = sDoc.verbs().data()[0];
    const tense = v ? v.tense : "Unknown";
    const hasNeg = sDoc.has('#Negative') ? 'Yes' : 'No';

    output += `Sentence ${i + 1}:\n`;
    output += `• ${s}\n`;
    output += `  - Tense: ${tense}\n`;
    output += `  - Negation: ${hasNeg}\n`;
    output += `  - Complexity: ${s.length > 120 ? 'Complex' : 'Simple'}\n\n`;
  });

  output += `🔍 Noun Phrases: ${nounPhrases.join(', ') || 'None'}\n`;
  output += `🔍 Verbs: ${verbs.out('array').join(', ') || 'None'}\n`;
  output += `🔍 Negation Words: ${negations.out('array').join(', ') || 'None'}\n`;
  output += `🔍 Named Entities: ${topics.join(', ') || 'None'}\n\n`;

  output += `📚 POS Count:\n`;
  const posCounts = doc.out('tags');
  let counts = {};
  posCounts.forEach(tags => {
    tags.forEach(tag => counts[tag] = (counts[tag] || 0) + 1);
  });
  for (let [tag, count] of Object.entries(counts)) {
    output += `- ${tag}: ${count}\n`;
  }

  output += `\n🧩 Lemmas:\n${lemmas.join('\n')}\n\n`;
  output += `🔠 Syllables per Word:\n${syllables}\n`;

  document.getElementById("output").innerText = output;
}