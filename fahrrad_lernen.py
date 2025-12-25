import os, math, random
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

IMG_SIZE = (150, 150)
BATCH_SIZE = 16
EPOCHS = 5

TRAIN_DIR = "daten/train"
TEST_DIR = "daten/test"

MODEL_H5 = "mein_fahrrad_modell.h5"
MODEL_KERAS = "mein_fahrrad_modell.keras"

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

def count_images(folder: str) -> int:
    c = 0
    for root, _, files in os.walk(folder):
        for f in files:
            if f.lower().endswith((".jpg", ".jpeg", ".png")):
                c += 1
    return c

print("\n=== DATA CHECK ===")
print("Train images:", count_images(TRAIN_DIR))
print("Test images :", count_images(TEST_DIR))

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=10,
    zoom_range=0.10,
    width_shift_range=0.05,
    height_shift_range=0.05,
    horizontal_flip=True
)
test_datagen = ImageDataGenerator(rescale=1./255)

train_gen = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    shuffle=True,
    seed=SEED
)

test_gen = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    shuffle=False
)

print("\n=== CLASS INDICES ===")
print(train_gen.class_indices)

steps_per_epoch = max(1, math.ceil(train_gen.samples / BATCH_SIZE))
val_steps = max(1, math.ceil(test_gen.samples / BATCH_SIZE))

model = models.Sequential([
    layers.Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3)),
    layers.Conv2D(32, 3, activation="relu"),
    layers.MaxPooling2D(2),
    layers.Conv2D(64, 3, activation="relu"),
    layers.MaxPooling2D(2),
    layers.Conv2D(128, 3, activation="relu"),
    layers.MaxPooling2D(2),
    layers.Flatten(),
    layers.Dense(256, activation="relu"),
    layers.Dense(1, activation="sigmoid")
])

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

print("\n=== Training starts now! ===")
history = model.fit(
    train_gen,
    steps_per_epoch=steps_per_epoch,
    epochs=EPOCHS,
    validation_data=test_gen,
    validation_steps=val_steps
)

model.save(MODEL_H5)
model.save(MODEL_KERAS)

print(f"\n=== Done! Saved as '{MODEL_H5}' and '{MODEL_KERAS}' ===")
