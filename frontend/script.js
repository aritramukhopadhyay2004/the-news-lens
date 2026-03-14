document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("predictBtn").addEventListener("click", predictNews);
  document.getElementById("urlBtn").addEventListener("click", checkURL);
});

async function predictNews() {
  const text = document.getElementById("newsText").value.trim();
  if (!text) {
    alert("Enter news text!");
    return;
  }

  const resultDiv = document.getElementById("result");
  resultDiv.innerHTML = "<p>Detecting...</p>";

  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    const confidence = (data.confidence * 100).toFixed(1);
    resultDiv.innerHTML = `
      <h2>${data.prediction}</h2>
      <p>Confidence: ${confidence}%</p>
      <span class="${data.prediction.toLowerCase()}">${data.prediction}</span>
    `;
  } catch (error) {
    console.error("Prediction error:", error);
    resultDiv.innerHTML = "<p>Error: Check console or server.</p>";
  }
}

async function checkURL() {
  const url = document.getElementById("urlInput").value.trim();
  if (!url) {
    alert("Enter URL!");
    return;
  }

  const resultDiv = document.getElementById("result");
  resultDiv.innerHTML = "<p>Extracting & detecting...</p>";

  try {
    const response = await fetch("/api/predict_url", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    const confidence = data.confidence;
    resultDiv.innerHTML = `
      <h2>${data.prediction}</h2>
      <p>Confidence: ${confidence}%</p>
      <span class="${data.prediction.toLowerCase()}">${data.prediction}</span>
    `;
  } catch (error) {
    console.error("URL prediction error:", error);
    resultDiv.innerHTML = "<p>Error extracting/predicting from URL.</p>";
  }
}
