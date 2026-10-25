
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist

# 1. Load the MNIST dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 2. Display dataset information
print("Training images shape:", x_train.shape)
print("Training labels shape:", y_train.shape)
print("Testing images shape:", x_test.shape)
print("Testing labels shape:", y_test.shape)

print("\nPixel value range:")
print("Minimum:", np.min(x_train))
print("Maximum:", np.max(x_train))

# 3. Visualize 10 handwritten digits
fig, axes = plt.subplots(2, 5, figsize=(10, 5))

for i, ax in enumerate(axes.flat):
    ax.imshow(x_train[i], cmap="gray")
    ax.set_title(f"Label: {y_train[i]}")
    ax.axis("off")

plt.suptitle("MNIST - Sample Handwritten Digits")
plt.tight_layout()
plt.savefig("mnist_samples.png", dpi=150)
plt.show()

# 4. Examine class distribution
unique, counts = np.unique(y_train, return_counts=True)

print("\nTraining samples per digit:")
for digit, count in zip(unique, counts):
    print(f"Digit {digit}: {count} images")
