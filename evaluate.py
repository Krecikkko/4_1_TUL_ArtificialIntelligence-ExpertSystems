
import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report
)

os.makedirs("results", exist_ok=True)

# 1. Load the test dataset
(_, _), (x_test, y_test) = keras.datasets.mnist.load_data()

# 2. Normalize pixels
x_test = x_test.astype("float32") / 255.0

# 3. Load ANN-4, the same trained model used by the web app
model = keras.models.load_model("models/ANN-4.keras")

# 4. Predict all test images
probabilities = model.predict(x_test, verbose=0)
predictions = np.argmax(probabilities, axis=1)

# 5. Classification report
print("\n===== CLASSIFICATION REPORT =====")
print(classification_report(y_test, predictions, digits=4))

# 6. Confusion matrix
cm = confusion_matrix(y_test, predictions)

fig, ax = plt.subplots(figsize=(9, 8))
disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=np.arange(10)
)
disp.plot(ax=ax, cmap="Blues", values_format="d")
plt.title("ANN-4 MNIST Confusion Matrix")
plt.tight_layout()
plt.savefig("results/confusion_matrix.png", dpi=150)
plt.show()

# 7. Identify incorrect predictions
incorrect = np.where(predictions != y_test)[0]

print(f"\nTotal incorrect predictions: {len(incorrect)}")
print(f"Total correct predictions: {len(y_test) - len(incorrect)}")

# 8. Display first 20 mistakes
fig, axes = plt.subplots(4, 5, figsize=(12, 10))

for ax, index in zip(axes.flat, incorrect[:20]):
    ax.imshow(x_test[index], cmap="gray")
    ax.set_title(
        f"True: {y_test[index]} | Pred: {predictions[index]}\n"
        f"Confidence: {np.max(probabilities[index]):.1%}",
        fontsize=9
    )
    ax.axis("off")

for ax in axes.flat[len(incorrect[:20]):]:
    ax.axis("off")

plt.suptitle("ANN-4 Incorrectly Classified MNIST Digits")
plt.tight_layout()
plt.savefig("results/incorrect_predictions.png", dpi=150)
plt.show()

print("\nEvaluation completed.")
