# Handwritten digit recognition

The project uses one training script. Both evaluation and the web app load
`models/ANN-4.keras`.

Run commands from the project directory with the project's Python environment active.

## Train and compare models

```powershell
python compare_models.py
```

This trains ANN-1 through ANN-4, saves them in `models/`, and writes a comparison
table and validation accuracy graph to `results/`. ANN-2 is the baseline with
128 and 64 hidden neurons. ANN-4 uses the same hidden layer sizes with dropout
and early stopping.

The trained models are already included, so retraining is optional.

## Evaluate the web app's model

```powershell
python evaluate.py
```

This loads ANN-4 without retraining, prints a classification report, and saves
`results/confusion_matrix.png` and `results/incorrect_predictions.png`.

## Start the web app

```powershell
python app.py
```

Open the local address printed by Flask, draw a digit, and click Predict.
The app prepares the drawing and uses ANN-4 to predict it without updating
the model's weights.

## Explore the dataset

`python explore_mnist.py` prints MNIST dataset information and saves sample images.

`results/training_history.png` is a historical graph from the former standalone
baseline training script. The current training script produces
`results/model_comparison.png` instead.
