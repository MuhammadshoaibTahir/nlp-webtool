let latestData = [];

async function analyzeText() {
  const input = document.getElementById("inputText").value.trim();
  const output = document.getElementById("output");
  output.innerHTML = "⏳ Analyzing...";
  latestData = [];

  if (!input) {
    output.innerHTML = "<p class='text-red-600'>Please enter some text.</p>";
    return;
  }

  try {
    const response = await fetch("https://abcd1234.ngrok.io/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: input })
    });

    const data = await response.json();
    latestData = data;
    showRowTable(data.tokens, data.extra);
  } catch (err) {
    output.innerHTML = `<p class='text-red-600'>❌ Server error. Is Flask running?</p>`;
    console.error(err);
  }
}

function showRowTable(tokens, extra) {
  if (!Array.isArray(tokens) || tokens.length === 0) {
    document.getElementById("output").innerHTML = "<p>No data found.</p>";
    return;
  }

  const tokenTexts = tokens.map(d => d.text);
  const rows = {
    Lemma: tokens.map(d => d.lemma),
    POS: tokens.map(d => d.pos),
    Dependency: tokens.map(d => d.dep),
    Head: tokens.map(d => d.head),
    NER: tokens.map(d => d.ent)
  };

  let html = `
    <table id="resultTable" class="table-auto w-full text-sm border">
      <thead class="bg-blue-100">
        <tr>
          <th class="border px-2 py-1 bg-gray-100">Feature</th>
          ${tokenTexts.map(t => `<th class="border px-2 py-1 text-blue-700">${t}</th>`).join("")}
        </tr>
      </thead>
      <tbody>
  `;

  for (const [feature, values] of Object.entries(rows)) {
    html += `
      <tr class="text-center hover:bg-gray-50">
        <td class="border px-2 py-1 font-semibold bg-gray-50">${feature}</td>
        ${values.map(v => `<td class="border px-2 py-1">${v}</td>`).join("")}
      </tr>
    `;
  }

  // Add extra features below the token rows
  html += `
    <tr><td colspan="${tokenTexts.length + 1}" class="bg-gray-200 font-bold px-2 py-1">🔍 Extra Features</td></tr>
    <tr>
      <td class="font-semibold bg-gray-50 px-2 py-1">Noun Phrases</td>
      <td colspan="${tokenTexts.length}" class="px-2 py-1">${extra.np_chunks.join(", ")}</td>
    </tr>
    <tr>
      <td class="font-semibold bg-gray-50 px-2 py-1">Tense & Aspect</td>
      <td colspan="${tokenTexts.length}" class="px-2 py-1">${extra.tense_aspect.join(" | ")}</td>
    </tr>
    <tr>
      <td class="font-semibold bg-gray-50 px-2 py-1">SVO Structure</td>
      <td colspan="${tokenTexts.length}" class="px-2 py-1">${extra.svo.join(" | ")}</td>
    </tr>
    <tr>
      <td class="font-semibold bg-gray-50 px-2 py-1">Negation</td>
      <td colspan="${tokenTexts.length}" class="px-2 py-1">${extra.negation.join(" | ")}</td>
    </tr>
    <tr>
      <td class="font-semibold bg-gray-50 px-2 py-1">Sentence Complexity</td>
      <td colspan="${tokenTexts.length}" class="px-2 py-1">${extra.complexity.toFixed(2)}</td>
    </tr>
  `;

  html += "</tbody></table>";
  document.getElementById("output").innerHTML = html;
}

function clearAll() {
  document.getElementById("inputText").value = "";
  document.getElementById("output").innerHTML = "";
  latestData = [];
}

function downloadExcel() {
  alert("Download disabled for now — extended features are sentence-level.");
}