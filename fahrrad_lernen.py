# fahrrad_lernen.py  (DO NOT rename)
# Train a small CNN on Raspberry Pi 5 to detect: bicycle vs not_bicycle
#
# Folder structure (must exist):
#   daten/train/bicycle/
#   daten/train/not_bicycle/
#   daten/test/bicycle/
#   daten/test/not_bicycle/
#
# Output model:
#   mein_fahrrad_modell.h5   (used by testen.py)
#
# Run (inside venv):
#   python3 fahrrad_lernen.py

import os
import random
import numpy as np
import tensorflow as tf

from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# -----------------------------
# Settings (Pi-friendly)
# -----------------------------
IMG_SIZE = (150, 150)
BATCH_SIZE = 16
EPOCHS = 5
SEED = 42

TRAIN_DIR = "daten/train"
TEST_DIR = "daten/test"

# IMPORTANT: Force fixed class order to avoid label confusion:
# bicycle -> 0, not_bicycle -> 1
CLASSES = ["bicycle", "not_bicycle"]

MODEL_H5 = "mein_fahrrad_modell.h5"

# -----------------------------
# Reproducibility
# -----------------------------
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

# -----------------------------
# Helpers
# -----------------------------
def count_images(folder: str) -> int:
    total = 0
    for root, _, files in os.walk(folder):
        for f in files:
            if f.lower().endswith((".jpg", ".jpeg", ".png")):
                total += 1
    return total


def must_exist(path: str):
    if not os.path.isdir(path):
        raise FileNotFoundError(f"Folder not found: {path}")


def print_dataset_report():
    print("\n=== DATA CHECK ===")
    must_exist(TRAIN_DIR)
    must_exist(TEST_DIR)

    for split_dir, split_name in [(TRAIN_DIR, "train"), (TEST_DIR, "test")]:
        for c in CLASSES:
            p = os.path.join(split_dir, c)
            must_exist(p)

    train_total = count_images(TRAIN_DIR)
    test_total = count_images(TEST_DIR)
    train_b = count_images(os.path.join(TRAIN_DIR, "bicycle"))
    train_n = count_images(os.path.join(TRAIN_DIR, "not_bicycle"))
    test_b = count_images(os.path.join(TEST_DIR, "bicycle"))
    test_n = count_images(os.path.join(TEST_DIR, "not_bicycle"))

    print(f"Train folder: {TRAIN_DIR} -> images: {train_total} (bicycle={train_b}, not_bicycle={train_n})")
    print(f"Test  folder: {TEST_DIR}  -> images: {test_total} (bicycle={test_b}, not_bicycle={test_n})")

    if train_total < 40:
        print("WARNING: Very few training images. Try adding more pictures for better accuracy.")
    if min(train_b, train_n) == 0:
        print("WARNING: One class has 0 images! You need BOTH classes.")
    if abs(train_b - train_n) > max(10, 0.5 * min(train_b, train_n)):
        print("WARNING: Classes are imbalanced. Try adding more images to the smaller class.")

    print("\nExpected class mapping (fixed):")
    print("  bicycle = 0")
    print("  not_bicycle = 1")


# -----------------------------
# Main Training Script
# -----------------------------
def main():
    print_dataset_report()

    # Data generators
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,
        rotation_range=8,
        width_shift_range=0.05,
        height_shift_range=0.05,
        zoom_range=0.10,
        horizontal_flip=True
    )

    test_datagen = ImageDataGenerator(rescale=1.0 / 255.0)

    train_gen = train_datagen.flow_from_directory(
        TRAIN_DIR,
        classes=CLASSES,                 # IMPORTANT (fixed order)
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="binary",
        shuffle=True,
        seed=SEED
    )

    test_gen = test_datagen.flow_from_directory(
        TEST_DIR,
        classes=CLASSES,                 # IMPORTANT (fixed order)
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="binary",
        shuffle=False
    )

    print("\n=== CLASS INDICES (must be bicycle:0, not_bicycle:1) ===")
    print(train_gen.class_indices)

    # Build a small CNN (Pi-friendly)
    model = models.Sequential([
        layers.Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3)),
        layers.Conv2D(16, (3, 3), activation="relu"),
        layers.MaxPooling2D(2, 2),

        layers.Conv2D(32, (3, 3), activation="relu"),
        layers.MaxPooling2D(2, 2),

        layers.Conv2D(64, (3, 3), activation="relu"),
        layers.MaxPooling2D(2, 2),

        layers.Flatten(),
        layers.Dense(128, activation="relu"),
        layers.Dense(1, activation="sigmoid")  # binary output (0..1)
    ])

    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    print("\n=== Training starts now! ===")
    print("Be patient: Raspberry Pi may be slower than a big PC.\n")

    steps_per_epoch = max(1, train_gen.samples // BATCH_SIZE)
    validation_steps = max(1, test_gen.samples // BATCH_SIZE)

    history = model.fit(
        train_gen,
        steps_per_epoch=steps_per_epoch,
        epochs=EPOCHS,
        validation_data=test_gen,
        validation_steps=validation_steps
    )

    print("\n=== Evaluation on test set (one pass) ===")
    loss, acc = model.evaluate(test_gen, verbose=1)
    print(f"Test accuracy: {acc:.4f}   Test loss: {loss:.4f}")

    # Save model for testen.py
    model.save(MODEL_H5)
    print(f"\n=== Done! Saved as '{MODEL_H5}' ===")
    print("Next step: run the GUI tester:")
    print("  python3 testen.py")


if __name__ == "__main__":
    main()
