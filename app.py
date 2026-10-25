
import base64
import io

import numpy as np
from flask import Flask, jsonify, render_template, request
from PIL import Image, ImageOps
from tensorflow import keras

app = Flask(__name__)

# Load the model - ANN-4
model = keras.models.load_model("models/ANN-4.keras")


def preprocess_image(image_data):
    encoded = image_data.split(",", 1)[1]
    image_bytes = base64.b64decode(encoded)

    image = Image.open(io.BytesIO(image_bytes)).convert("L")
    image = ImageOps.invert(image)

    # Remove faint background pixels
    image = image.point(lambda p: 0 if p < 20 else p)

    bbox = image.getbbox()
    if bbox is None:
        raise ValueError("Please draw a digit first.")

    image = image.crop(bbox)

    # Scale longest dimension to 20 pixels
    image.thumbnail((20, 20), Image.Resampling.LANCZOS)

    # Place the digit on a 28x28 black canvas
    processed = Image.new("L", (28, 28), 0)

    x = (28 - image.width) // 2
    y = (28 - image.height) // 2
    processed.paste(image, (x, y))

    # Calculate center of mass
    pixels = np.asarray(processed, dtype=np.float32)

    yy, xx = np.indices(pixels.shape)
    mass = pixels.sum()

    if mass > 0:
        center_x = (xx * pixels).sum() / mass
        center_y = (yy * pixels).sum() / mass

        shift_x = int(round(13.5 - center_x))
        shift_y = int(round(13.5 - center_y))

        # Shift with zero padding (no wraparound)
        centered = np.zeros_like(pixels)

        src_x0 = max(0, -shift_x)
        src_x1 = min(28, 28 - shift_x)
        src_y0 = max(0, -shift_y)
        src_y1 = min(28, 28 - shift_y)

        dst_x0 = max(0, shift_x)
        dst_y0 = max(0, shift_y)

        centered[
            dst_y0:dst_y0 + (src_y1 - src_y0),
            dst_x0:dst_x0 + (src_x1 - src_x0)
        ] = pixels[src_y0:src_y1, src_x0:src_x1]

        pixels = centered

    # Optional: save the processed image for debugging
    Image.fromarray(pixels.astype(np.uint8)).resize(
        (280, 280), Image.Resampling.NEAREST
    ).save("processed_digit.png")

    return (pixels / 255.0).reshape(1, 28, 28)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not data or "image" not in data:
            return jsonify({"error": "Missing image data"}), 400

        image = preprocess_image(data["image"])

        # Neural network prediction
        probabilities = model.predict(image, verbose=0)[0]

        predicted_digit = int(np.argmax(probabilities))
        confidence = float(np.max(probabilities))

        return jsonify({
            "digit": predicted_digit,
            "confidence": confidence,
            "probabilities": probabilities.tolist()
        })

    except (ValueError, KeyError, TypeError, OSError) as error:
        return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    app.run(debug=True)
