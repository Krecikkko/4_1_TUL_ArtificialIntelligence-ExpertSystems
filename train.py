
import os
import random
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# 1. Reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

os.makedirs("models", exist_ok=True)
os.makedirs("results", exist_ok=True)

# 2. Load MNIST
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# 3. Normalize images to [0, 1]
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

# 4. Define ANN architecture
model = keras.Sequential([
    layers.Input(shape=(28, 28)),
    layers.Flatten(),
    layers.Dense(128, activation="relu"),
    layers.Dense(64, activation="relu"),
    layers.Dense(10, activation="softmax")
])

# 5. Configure training
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# 6. Display model architecture
model.summary()

# 7. Train the neural network
history = model.fit(
    x_train,
    y_train,
    epochs=15,
    batch_size=32,
    validation_split=0.1,
    verbose=1
)

# 8. Evaluate on unseen test data
test_loss, test_accuracy = model.evaluate(
    x_test, y_test, verbose=0
)

print("\n===== FINAL RESULTS =====")
print(f"Test accuracy: {test_accuracy:.4%}")
print(f"Test loss: {test_loss:.4f}")

# 9. Save trained model
model.save("models/digit_model.keras")

# 10. Plot training history
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].plot(history.history["accuracy"], label="Training")
axes[0].plot(history.history["val_accuracy"], label="Validation")
axes[0].set_title("Model Accuracy")
axes[0].set_xlabel("Epoch")
axes[0].set_ylabel("Accuracy")
axes[0].legend()
axes[0].grid(True)

axes[1].plot(history.history["loss"], label="Training")
axes[1].plot(history.history["val_loss"], label="Validation")
axes[1].set_title("Model Loss")
axes[1].set_xlabel("Epoch")
axes[1].set_ylabel("Loss")
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.savefig("results/training_history.png", dpi=150)
plt.show()

print("\nModel saved to models/digit_model.keras")
print("Training graph saved to results/training_history.png")
