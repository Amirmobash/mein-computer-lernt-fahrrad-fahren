````md
# Bicycle Detector on Raspberry Pi 5 (Step-by-step — German)

**Goal:** Your Raspberry Pi learns to classify pictures as **BICYCLE** or **NOT BICYCLE**.  
After training, you can open an image (and optionally drag & drop) and the app shows the result with probabilities.

✅ **Important:** You do NOT need to create or copy Python files manually.  
Everything is already inside the project folder you download.

---

## ✅ What you need
- Raspberry Pi 5 (or Pi 4)
- Raspberry Pi OS (Desktop)
- Internet
- Terminal (the black window)

---

## 1) Download + Extract the project

Download this file from GitHub:

- **`fahrrad_projekt.7z`**

Extract it into your **home folder**.

After extracting, you should have this folder:

- `~/fahrrad_projekt/`

Open Terminal and check:

```bash
ls ~
````

You should see:

```text
fahrrad_projekt
```

Go into the folder:

```bash
cd ~/fahrrad_projekt
pwd
```

Expected (similar):

```text
/home/pi/fahrrad_projekt
```

---

## 2) Update the system + install tools

Run these commands line by line:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y python3-pip python3-venv python3-tk p7zip-full
```

✅ Good sign: no red **ERROR** lines.

---

## 3) Create + activate a Python virtual environment (venv)

A venv is a clean “project box” for Python packages.

```bash
cd ~/fahrrad_projekt
python3 -m venv meine_umgebung
source meine_umgebung/bin/activate
```

✅ Expected: your prompt starts with `(meine_umgebung)`:

```text
(meine_umgebung) pi@raspberrypi:~/fahrrad_projekt $
```

Upgrade pip tools:

```bash
python -m pip install -U pip setuptools wheel
```

---

## 4) Install Python packages (stable for Raspberry Pi)

These versions avoid common Raspberry Pi dependency problems:

```bash
pip install --no-cache-dir "protobuf>=5.28.0,<6" "flatbuffers>=24.3.25,<25"
pip install --no-cache-dir "tensorflow==2.20.0" "numpy" "pillow" "scipy"
```

(Optional) Quick version test:

```bash
python3 -c "import tensorflow as tf, flatbuffers, google.protobuf, scipy; print('TF:', tf.__version__); print('flatbuffers:', flatbuffers.__version__); print('protobuf:', google.protobuf.__version__); print('scipy:', scipy.__version__)"
```

---

## 5) Check the image folder structure (IMPORTANT)

The project already contains the correct folders:

* `daten/train/bicycle/`
* `daten/train/not_bicycle/`
* `daten/test/bicycle/`
* `daten/test/not_bicycle/`

Check:

```bash
cd ~/fahrrad_projekt
ls -R daten
```

You should see `train` and `test`, and inside them `bicycle` and `not_bicycle`.

---

## 6) Put images into the correct folders

### Where do bicycle images go?

Put bicycle photos into:

* `daten/train/bicycle/`
* `daten/test/bicycle/`

### Where do NOT-bicycle images go?

Put pictures of anything else into:

* `daten/train/not_bicycle/`
* `daten/test/not_bicycle/`

✅ Allowed file types: `.jpg`, `.jpeg`, `.png`
✅ File names can be anything (even weird downloaded names)

Open the file manager in the project folder:

```bash
xdg-open .
```

### Check how many images you have

Each number should be **greater than 0**:

```bash
ls daten/train/bicycle | wc -l
ls daten/train/not_bicycle | wc -l
ls daten/test/bicycle | wc -l
ls daten/test/not_bicycle | wc -l
```

---

## ⭐ Very important (accuracy tip for kids)

If the computer sometimes makes mistakes, that is normal.

✅ **More images = better accuracy.**

To make it smarter:

* add more bicycle images (different bikes, angles, backgrounds)
* add more not-bicycle images (chair, car, plant, bag, shoes, helmet, scooter, etc.)

---

## 7) Train the model (build the “brain file”)

Make sure venv is active:

```bash
cd ~/fahrrad_projekt
source meine_umgebung/bin/activate
```

Start training:

```bash
python3 fahrrad_lernen.py
```

Expected:

* It shows image counts
* It prints something like: `Found XX images belonging to 2 classes.`
* It runs `Epoch 1/5`, `Epoch 2/5`, ...
* At the end it saves the model file:

✅ `mein_fahrrad_modell.h5`

Check it exists:

```bash
ls -l mein_fahrrad_modell.h5
```

---

## 8) Run the GUI app (test images with a window)

Start the app:

```bash
python3 testen.py
```

Now you can:

* click **Open Image**
* (optional) drag & drop an image into the window if drag & drop is installed

---

## 9) Optional: enable Drag & Drop

If you want drag & drop support:

```bash
pip install --no-cache-dir tkinterdnd2
```

Then run again:

```bash
python3 testen.py
```

---

## 10) Optional: run with an image path (Terminal shortcut)

```bash
python3 testen.py daten/test/bicycle/your_image.jpg
```

---

## 11) If it predicts wrong (example: NOT BICYCLE → BICYCLE)

Do this checklist:

1. Add more images (especially more NOT-bicycle variety)
2. Make sure no bicycle image is accidentally inside `not_bicycle`
3. Train again:

```bash
python3 fahrrad_lernen.py
```

---

## Bonus check: class mapping (only if you are curious)

```bash
python3 -c "from tensorflow.keras.preprocessing.image import ImageDataGenerator; gen=ImageDataGenerator().flow_from_directory('daten/train'); print(gen.class_indices)"
```

Often you will see:

```text
{'bicycle': 0, 'not_bicycle': 1}
```

---

✅ Done — Have fun training your Raspberry Pi! 🚲
