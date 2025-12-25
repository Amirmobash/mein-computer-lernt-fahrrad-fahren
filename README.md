# Mein Computer lernt Fahrrad fahren
**Ein Mitmach-Buch von Finn**

Dieses Repository enthält **Code & Projektstruktur** zum Buchprojekt rund um Raspberry Pi
(Bilderkennung: „BICYCLE“ vs. „NOT BICYCLE“).

✅ **Wichtig:** Das **vollständige Manuskript / Buch-PDF ist NICHT in diesem Repository enthalten**, damit keine Inhalte unbeabsichtigt öffentlich werden.

> Hinweis: Alle technischen Befehle und Code-Beispiele sind absichtlich **in ENGLISCH**, damit sie exakt so funktionieren, wie der Computer sie erwartet.

---

## Was ist in diesem Repo?
- 🧠 Python-Code (Training & Test)
- 🗂️ Ordnerstruktur für Trainings- und Testbilder
- 🖼️ Optionale Assets (Screenshots/Illustrationen), **ohne Buchtext**

---

## Voraussetzungen
- Raspberry Pi **4 oder 5**
- Raspberry Pi OS
- System-Sprache: **English** (empfohlen)
- Internetverbindung
- Tastatur, Maus, Bildschirm

---

## Quick Start (Kurz-Anleitung)

### 1) System aktualisieren
```bash
sudo apt update && sudo apt full-upgrade -y
````

### 2) Python-Werkzeuge installieren

```bash
sudo apt install python3-pip python3-venv -y
```

### 3) Projektordner & virtuelle Umgebung

```bash
mkdir fahrrad_projekt
cd fahrrad_projekt
python3 -m venv meine_umgebung
source meine_umgebung/bin/activate
```

### 4) Bibliotheken

```bash
pip install tensorflow pillow numpy
```

### 5) Ordnerstruktur für Bilder

```bash
mkdir -p daten/train/bicycle daten/train/not_bicycle daten/test/bicycle daten/test/not_bicycle
```

Beispiel-Dateien:

* `daten/train/bicycle/bike_01.jpg`
* `daten/train/not_bicycle/chair_01.jpg`
* `daten/test/bicycle/bike_test_01.jpg`
* `daten/test/not_bicycle/plant_test_01.jpg`

---

## Training

Lege deinen Trainings-Code z.B. in `code/fahrrad_lernen.py` ab und starte:
باشه — این **کد کاملِ داخل کتاب** برای دو فایل `fahrrad_lernen.py` و `testen.py` هست (همه‌چیز انگلیسی)، دقیقاً مطابق متن PDF. 

---

## 1) فایل آموزش: `fahrrad_lernen.py`

ساخت فایل:

```bash
nano fahrrad_lernen.py
```

این کد را **کامل** Paste کن:

```python
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# --- 1) DATA: prepare images ---
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    'daten/train',
    target_size=(150, 150),
    batch_size=16,
    class_mode='binary'
)

test_generator = test_datagen.flow_from_directory(
    'daten/test',
    target_size=(150, 150),
    batch_size=16,
    class_mode='binary'
)

# --- 2) MODEL: build a small network (Pi-friendly) ---
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    layers.MaxPooling2D(2, 2),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),
    layers.Flatten(),
    layers.Dense(256, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("\n=== Training starts now! ===")
print("Be patient: Raspberry Pi may be slower than a big PC.\n")

# --- 3) TRAIN ---
history = model.fit(
    train_generator,
    steps_per_epoch=max(1, train_generator.samples // 16),
    epochs=5,
    validation_data=test_generator,
    validation_steps=max(1, test_generator.samples // 16)
)

# --- 4) SAVE ---
model.save('mein_fahrrad_modell.h5')
print("\n=== Done! Saved as 'mein_fahrrad_modell.h5' ===")
```




```bash
python3 fahrrad_lernen.py
```

```bash
nano testen.py
```
:

```python
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

model = load_model('mein_fahrrad_modell.h5')

# CHANGE THIS to a real file name from your test folder:
img_path = 'daten/test/bicycle/dein_test_bild.jpg'

img = image.load_img(img_path, target_size=(150, 150))
img_array = image.img_to_array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

prediction = model.predict(img_array)

if prediction[0] > 0.5:
    print("This is a BICYCLE!")
else:
    print("This is NOT a bicycle.")
```




```bash
python3 testen.py
```


```bash
python3 code/fahrrad_lernen.py
```

Das Modell kann z.B. als `mein_fahrrad_modell.h5` gespeichert werden.

---

## Test

Lege z.B. `code/testen.py` an und starte:

```bash
python3 code/testen.py
```

---

## Empfohlene Repo-Struktur

```text
.
├─ code/
│  ├─ fahrrad_lernen.py
│  └─ testen.py
├─ daten/                 # optional (lokal), Bilder nicht öffentlich committen!
├─ assets/
│  ├─ images/
│  └─ screenshots/
├─ .gitignore
└─ README.md
```

---

## Credits

* **Autor:** AmirMobasheraghdam
* **Technische Übersetzung & fachliche Bearbeitung:** Ladan Seddighi
* **Technische Prüfung (IT) (optional):** [Name eintragen]

---

## Copyright / Lizenz

* **Buchtext/Manuskript:** © 2025 AmirMobasheraghdam — Alle Rechte vorbehalten
* **Code:** (optional) MIT License

---

## Hinweis

Dieses Repository ist für Lern- und Bildungszwecke gedacht.
Bilder, Logos und Marken gehören ihren jeweiligen Inhabern.

````


```gitignore
# Book / manuscript (never publish)
manuscript/
*.pdf
*.docx
*.odt
*.epub
*.mobi
*.indd

# Exports / prints
export/
exports/
print/
build/
dist/

# Datasets / images (usually large or copyrighted)
daten/
data/
dataset/
datasets/
*.zip
*.7z
*.rar

# Model files
*.h5
*.keras
*.tflite

# Python junk
__pycache__/
*.pyc
.venv/
venv/
.env
.DS_Store
```md
# Raspberry Pi 5 (Linux / Raspberry Pi OS) 

All commands and code are intentionally in **ENGLISH**, exactly like in the book. :contentReference[oaicite:0]{index=0}

---

## 0) Open Terminal (the “magic window”)
You should see a prompt similar to:
```

pi@raspberrypi:~ $

````
:contentReference[oaicite:1]{index=1}

---

## 1) Update everything (Book version)
Run:
```bash
sudo apt update && sudo apt full-upgrade -y
````

You should see lines like:

* `Reading package lists... Done`
* `Hit:` / `Get:` lines scrolling
* It finishes and returns to your prompt (no fatal `E:` error). 

**Appendix A version (also OK if your book appendix uses it):**

```bash
sudo apt update && sudo apt upgrade -y
```



---

## 2) Install Python tools (pip + venv)

Run:

```bash
sudo apt install python3-pip python3-venv -y
```

You should see:

* `... is already the newest version` **OR**
* `Setting up ...`
  Then it returns to the prompt. 

---

## 3) Create the project folder + virtual environment

Run:

```bash
mkdir fahrrad_projekt
cd fahrrad_projekt
python3 -m venv meine_umgebung
source meine_umgebung/bin/activate
```

You should see the venv name before the prompt:

```
(meine_umgebung) pi@raspberrypi:~/fahrrad_projekt $
```



---

## 4) Install the libraries

Run:

```bash
pip install tensorflow pillow numpy
```

You should see:

* `Collecting tensorflow`
* `Collecting pillow`
* `Collecting numpy`
  Finish message:
* `Successfully installed ...` **OR** `Requirement already satisfied ...`
  (No blocking `ERROR:` at the end.) 

---

## 5) Create the dataset folder structure (as in the book)

Run these **line-by-line**:

```bash
mkdir daten
mkdir daten/train
mkdir daten/train/bicycle
mkdir daten/train/not_bicycle
mkdir daten/test
mkdir daten/test/bicycle
mkdir daten/test/not_bicycle
```

Expected:

* Usually **no output** (that’s normal)
* The folders are created. 

(Optional check)

```bash
ls -R daten
```

You should see `train/bicycle`, `train/not_bicycle`, `test/bicycle`, `test/not_bicycle`. 

---

## 6) Put images into folders (File Manager)

* training bicycle images:

  * `daten/train/bicycle`
* training non-bicycle images:

  * `daten/train/not_bicycle`
* test bicycle images:

  * `daten/test/bicycle`
* test non-bicycle images:

  * `daten/test/not_bicycle` 

Example paths from the book:

* `/home/pi/fahrrad_projekt/daten/train/bicycle/bike_01.jpg`
* `/home/pi/fahrrad_projekt/daten/train/not_bicycle/chair_01.jpg`
* `/home/pi/fahrrad_projekt/daten/test/bicycle/bike_test_01.jpg`
* `/home/pi/fahrrad_projekt/daten/test/not_bicycle/plant_test_01.jpg` 

---

## 7) Create the training file (book code)

Create the file:

```bash
nano fahrrad_lernen.py
```

Paste the **exact code from the book** and save. 

---

## 8) Train the model (the “big learning”)

Make sure you are in the project folder and venv is active:

```bash
cd ~/fahrrad_projekt
source meine_umgebung/bin/activate
```

Start training:

```bash
python3 fahrrad_lernen.py
```

You should see:

* `=== Training starts now! ===`
* output with:

  * `Epoch 1/5` … up to `Epoch 5/5`
  * words like `accuracy` and `loss`
* final line:

  * `=== Done! Saved as 'mein_fahrrad_modell.h5' ===` 

Confirm the file exists:

```bash
ls
```

You should see:

* `mein_fahrrad_modell.h5` 

---

## 9) Create the test script (book code)

Create:

```bash
nano testen.py
```

Paste the **exact code from the book**.
Change ONLY this line to a real test image file:

```python
img_path = 'daten/test/bicycle/dein_test_bild.jpg'
```



---

## 10) Run the test

Run:

```bash
python3 testen.py
```

You should see ONE of these outputs:

* `This is a BICYCLE!`
* `This is NOT a bicycle.` 

---

## Appendix A (Mini cheat sheet — commands list)

(Exactly as shown in the book appendix) 

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv -y
mkdir fahrrad_projekt
cd fahrrad_projekt
python3 -m venv meine_umgebung
source meine_umgebung/bin/activate
pip install tensorflow pillow numpy
mkdir -p daten/train/bicycle daten/train/not_bicycle daten/test/bicycle daten/test/not_bicycle
python3 fahrrad_lernen.py
python3 testen.py
```

```
```

