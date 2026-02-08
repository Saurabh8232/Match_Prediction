const form = document.getElementById("predictionForm");
const resultDiv = document.getElementById("result");

const API_URL = "http://127.0.0.1:8000/predict/";

form.addEventListener("submit", function (e) {
    e.preventDefault();

    resultDiv.style.display = "block";
    resultDiv.style.background = "#f8f9fa";
    resultDiv.innerHTML = "Predicting...";

    const payload = {
        age: Number(document.getElementById("age").value),
        gender: Number(document.getElementById("gender").value),
        heart_rate: Number(document.getElementById("heartRate").value),
        systolic_bp: Number(document.getElementById("sbp").value),
        diastolic_bp: Number(document.getElementById("dbp").value),
        ck_mb: Number(document.getElementById("ckmb").value),
        troponin: Number(document.getElementById("troponin").value)
    };

    fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        resultDiv.style.background = "#e6fffa";
        resultDiv.innerHTML = 
            "Predicted Blood Sugar: <br><strong>" + data.prediction + "</strong>";
    })
    .catch(err => {
        resultDiv.style.background = "#ffe6e6";
        resultDiv.innerHTML = "Unable to connect to server";
        console.error(err);
    });
});
