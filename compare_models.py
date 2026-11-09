
import os
import random
import csv
import numpy as np
import matplotlib.pyplot as plt

# pyright: reportMissingModuleSource=false
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers
except ImportError as exc:
    raise ImportError(
        "TensorFlow is required to run this script. "
        "Install it with: pip install tensorflow"
    ) from exc

os.makedirs("results", exist_ok=True)
os.makedirs("models", exist_ok=True)

SEED = 42

# Load and normalize MNIST
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

# Fixed train/validation split, shared by every model
x_fit, x_val = x_train[:-6000], x_train[-6000:]
y_fit, y_val = y_train[:-6000], y_train[-6000:]


def build_model(hidden_layers, dropout=0.0):
    model = keras.Sequential()
    model.add(layers.Input(shape=(28, 28)))
    model.add(layers.Flatten())

    for neurons in hidden_layers:
        model.add(layers.Dense(neurons, activation="relu"))

        if dropout > 0:
            model.add(layers.Dropout(dropout))

    model.add(layers.Dense(10, activation="softmax"))

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


experiments = {
    "ANN-1": {"layers": [64], "dropout": 0.0},
    "ANN-2": {"layers": [128, 64], "dropout": 0.0},
    "ANN-3": {"layers": [256, 128, 64], "dropout": 0.0},
    "ANN-4": {"layers": [128, 64], "dropout": 0.2}
}

results = []
histories = {}

for name, config in experiments.items():
    print(f"\n===== Training {name} =====")

    keras.backend.clear_session()
    random.seed(SEED)
    np.random.seed(SEED)
    tf.random.set_seed(SEED)

    model = build_model(
        hidden_layers=config["layers"],
        dropout=config["dropout"]
    )

    callbacks = []

    if name == "ANN-4":
        callbacks.append(
            keras.callbacks.EarlyStopping(
                monitor="val_loss",
                patience=3,
                restore_best_weights=True
            )
        )

    history = model.fit(
        x_fit,
        y_fit,
        epochs=15,
        batch_size=32,
        validation_data=(x_val, y_val),
        callbacks=callbacks,
        verbose=1
    )

    test_loss, test_accuracy = model.evaluate(
        x_test, y_test, verbose=0
    )

    results.append({
        "Model": name,
        "Architecture": str(config["layers"]),
        "Parameters": model.count_params(),
        "Epochs": len(history.history["loss"]),
        "Test accuracy": round(test_accuracy, 5),
        "Test loss": round(test_loss, 5),
        "Best validation loss": round(
            min(history.history["val_loss"]), 5
        )
    })

    histories[name] = history.history
    model.save(f"models/{name}.keras")

    print(f"{name} accuracy: {test_accuracy:.4%}")
    print(f"{name} loss: {test_loss:.4f}")


# Save comparison table
with open("results/model_comparison.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)


# Plot validation accuracy
plt.figure(figsize=(10, 6))

for name, history in histories.items():
    epochs = range(1, len(history["val_accuracy"]) + 1)
    plt.plot(epochs, history["val_accuracy"], label=name)

plt.title("ANN Architecture Comparison")
plt.xlabel("Epoch")
plt.ylabel("Validation Accuracy")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("results/model_comparison.png", dpi=150)
plt.show()


# Print final summary
print("\n===== MODEL COMPARISON =====")

for result in results:
    print(result)
