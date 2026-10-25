
const canvas = document.getElementById("drawingCanvas");
const ctx = canvas.getContext("2d");

const predictButton = document.getElementById("predictButton");
const clearButton = document.getElementById("clearButton");
const predictedDigit = document.getElementById("predictedDigit");
const confidenceText = document.getElementById("confidence");
const probabilitiesDiv = document.getElementById("probabilities");
const errorMessage = document.getElementById("errorMessage");

let drawing = false;
let hasDrawing = false;

// White canvas with black strokes
function clearCanvas() {
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = "black";
    ctx.lineWidth = 18;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";

    drawing = false;
    hasDrawing = false;

    predictedDigit.textContent = "?";
    confidenceText.textContent = "Draw a digit to begin";
    probabilitiesDiv.innerHTML = "";
    errorMessage.textContent = "";
}

function getPosition(event) {
    const rect = canvas.getBoundingClientRect();

    return {
        x: (event.clientX - rect.left) * canvas.width / rect.width,
        y: (event.clientY - rect.top) * canvas.height / rect.height
    };
}

canvas.addEventListener("pointerdown", (event) => {
    drawing = true;
    hasDrawing = true;

    canvas.setPointerCapture(event.pointerId);

    const pos = getPosition(event);

    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);

    // Draw a dot even if the pointer does not move
    ctx.lineTo(pos.x + 0.01, pos.y + 0.01);
    ctx.stroke();
});

canvas.addEventListener("pointermove", (event) => {
    if (!drawing) return;

    const pos = getPosition(event);

    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
});

function stopDrawing() {
    drawing = false;
}

canvas.addEventListener("pointerup", stopDrawing);
canvas.addEventListener("pointercancel", stopDrawing);

clearButton.addEventListener("click", clearCanvas);

predictButton.addEventListener("click", async () => {
    errorMessage.textContent = "";

    if (!hasDrawing) {
        errorMessage.textContent = "Please draw a digit first.";
        return;
    }

    predictButton.disabled = true;
    predictButton.textContent = "Predicting...";

    try {
        const imageData = canvas.toDataURL("image/png");

        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                image: imageData
            })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Prediction failed");
        }

        predictedDigit.textContent = result.digit;
        confidenceText.textContent =
            `Confidence: ${(result.confidence * 100).toFixed(2)}%`;

        displayProbabilities(result.probabilities);

    } catch (error) {
        errorMessage.textContent = error.message;
    } finally {
        predictButton.disabled = false;
        predictButton.textContent = "Predict";
    }
});

function displayProbabilities(probabilities) {
    probabilitiesDiv.innerHTML = "";

    probabilities.forEach((probability, digit) => {
        const percentage = probability * 100;

        const row = document.createElement("div");
        row.className = "probability-row";

        const label = document.createElement("span");
        label.className = "digit-label";
        label.textContent = digit;

        const background = document.createElement("div");
        background.className = "bar-background";

        const fill = document.createElement("div");
        fill.className = "bar-fill";
        fill.style.width = `${percentage}%`;

        const value = document.createElement("span");
        value.className = "probability-value";
        value.textContent = `${percentage.toFixed(2)}%`;

        background.appendChild(fill);
        row.appendChild(label);
        row.appendChild(background);
        row.appendChild(value);

        probabilitiesDiv.appendChild(row);
    });
}

clearCanvas();
