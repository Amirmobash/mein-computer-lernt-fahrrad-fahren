"""
fahrrad_lernen.py
Raspberry Pi 5 friendly training script (binary: bicycle vs not_bicycle)

Folder structure expected:
daten/
  train/
    bicycle/
    not_bicycle/
  test/
    bicycle/
    not_bicycle/
"""

import os
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# --- SETTINGS (Pi-friendly) ---
IMG_SIZE = (150, 150)
BATCH_SIZE = 16
EPOCHS = 5
MODEL_PATH = "mein_fahrrad_modell.h5"

TRAIN_DIR = "daten/train"
TEST_DIR = "daten/test"


def _check_folder(path: str) -> None:
    if not os.path.isdir(path):
        raise FileNotFoundError(f"Folder not found: {path}")

def _count_images(root: str) -> int:
    exts = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp")
    count = 0
    for base, _, files in os.walk(root):
        for f in files:
            if f.lower().endswith(exts):
                count += 1
    return count


# --- 0) QUICK CHECKS ---
_check_folder(TRAIN_DIR)
_check_folder(TEST_DIR)

train_count = _count_images(TRAIN_DIR)
test_count = _count_images(TEST_DIR)

print("\n=== DATA CHECK ===")
print(f"Train folder: {TRAIN_DIR}  -> images: {train_count}")
print(f"Test folder : {TEST_DIR}   -> images: {test_count}")

if train_count == 0 or test_count == 0:
    raise RuntimeError(
        "No images found. Put JPG/PNG images into:\n"
        "  daten/train/bicycle, daten/train/not_bicycle,\n"
        "  daten/test/bicycle,  daten/test/not_bicycle\n"
    )

# --- 1) DATA: prepare images ---
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255.0,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(rescale=1.0 / 255.0)

train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    shuffle=True
)

test_generator = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    shuffle=False
)

print("\n=== CLASS INDICES ===")
print(train_generator.class_indices)  # should show {'bicycle': 0/1, 'not_bicycle': 1/0}

# --- 2) MODEL: build a small network (Pi-friendly) ---
model = models.Sequential([
    layers.Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3)),
    layers.Conv2D(32, (3, 3), activation="relu"),
    layers.MaxPooling2D(2, 2),
    layers.Conv2D(64, (3, 3), activation="relu"),
    layers.MaxPooling2D(2, 2),
    layers.Conv2D(128, (3, 3), activation="relu"),
    layers.MaxPooling2D(2, 2),
    layers.Flatten(),
    layers.Dense(256, activation="relu"),
    layers.Dense(1, activation="sigmoid"),
])

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

print("\n=== Training starts now! ===")
print("Be patient: Raspberry Pi may be slower than a big PC.\n")

# Steps: use ceil so we don't skip data when counts < batch size
steps_per_epoch = max(1, (train_generator.samples + BATCH_SIZE - 1) // BATCH_SIZE)
validation_steps = max(1, (test_generator.samples + BATCH_SIZE - 1) // BATCH_SIZE)

# --- 3) TRAIN ---
history = model.fit(
    train_generator,
    steps_per_epoch=steps_per_epoch,
    epochs=EPOCHS,
    validation_data=test_generator,
    validation_steps=validation_steps
)

# --- 4) SAVE ---
model.save(MODEL_PATH)
print(f"\n=== Done! Saved as '{MODEL_PATH}' ===")
