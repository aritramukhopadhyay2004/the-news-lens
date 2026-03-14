async function predictNews() {
  const text = document.getElementById("newsText").value;
  if (!text) return alert("Enter news text!");

  const resultDiv = document.getElementById("result");
  resultDiv.innerHTML = "Detecting...";

  try {
    fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await response.json();
    resultDiv.innerHTML = `
      <h2>${data.prediction}</h2>
      <p>Confidence: ${(data.confidence * 100).toFixed(1)}%</p>
      <span class="${data.prediction.toLowerCase()}">${data.prediction}</span>
    `;
  } catch (e) {
    resultDiv.innerHTML = "Error: Check console";
  }
}
async function checkURL() {
  const url = document.getElementById("urlInput").value;

  fetch("/api/predict_url", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      url: url,
    }),
  });

  const data = await response.json();

  document.getElementById("result").innerText =
    "Prediction: " +
    data.prediction +
    " | Confidence: " +
    data.confidence +
    "%";
}
