````md
# Fahrrad-Erkenner auf Raspberry Pi 5 (Schritt für Schritt – Deutsch)

**Ziel:** Dein Raspberry Pi lernt, Bilder als **FAHRRAD** oder **KEIN FAHRRAD** zu erkennen.  
Du kannst danach ein Bild öffnen (oder per Drag & Drop reinziehen) und bekommst ein klares Ergebnis.

---

## ✅ Was du brauchst
- Raspberry Pi 5 (oder Pi 4)
- Raspberry Pi OS (Desktop)
- Internet
- **Terminal** (schwarzes Fenster)

---

## 0) Terminal öffnen
Öffne **Terminal**.  
Du siehst ungefähr so eine Zeile:

```bash
amir@Amir:~ $
````

(Optional) Schau, wo du gerade bist:

```bash
pwd
```

---

## 1) System aktualisieren + Werkzeuge installieren

Tippe diese Befehle **Zeile für Zeile** ein:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y python3-pip python3-venv python3-tk
```

**Erwartung:** Keine roten “ERROR”-Zeilen.

---

## 2) Projektordner erstellen + virtuelle Umgebung (venv)

Jetzt erstellen wir einen Ordner für das Projekt:

```bash
mkdir -p ~/fahrrad_projekt
cd ~/fahrrad_projekt
```

Jetzt erstellen wir eine virtuelle Python-Umgebung:

```bash
python3 -m venv meine_umgebung
source meine_umgebung/bin/activate
```

**Erwartung:** Vor deiner Zeile steht jetzt `(meine_umgebung)`:

```bash
(meine_umgebung) amir@Amir:~/fahrrad_projekt $
```

Pip aktualisieren:

```bash
python -m pip install -U pip setuptools wheel
```

---

## 3) Python-Pakete installieren (stabil für Raspberry Pi)

Diese Versionen vermeiden typische Probleme (z.B. `imp`-Fehler, protobuf-Konflikte):

```bash
pip install --no-cache-dir "protobuf>=5.28.0,<6" "flatbuffers>=24.3.25,<25"
pip install --no-cache-dir "tensorflow==2.20.0" "numpy" "pillow" "scipy"
```

(Optional) Test: Versionen anzeigen (soll ohne Fehler laufen)

```bash
python3 -c "import tensorflow as tf, flatbuffers, google.protobuf, scipy; print('TF:', tf.__version__); print('flatbuffers:', flatbuffers.__version__); print('protobuf:', google.protobuf.__version__); print('scipy:', scipy.__version__)"
```

---

## 4) Ordner für die Bilder erstellen (wichtige Struktur!)

Wir brauchen 4 Ordner:

* Training:

  * `daten/train/bicycle`
  * `daten/train/not_bicycle`
* Test:

  * `daten/test/bicycle`
  * `daten/test/not_bicycle`

Erstelle sie so:

```bash
cd ~/fahrrad_projekt
mkdir -p daten/train/bicycle daten/train/not_bicycle daten/test/bicycle daten/test/not_bicycle
ls -R daten
```

**Erwartung:**

```text
daten:
test  train

daten/test:
bicycle  not_bicycle

daten/train:
bicycle  not_bicycle
```

---

## 5) Bilder in die richtigen Ordner legen (File Manager)

Öffne den Datei-Manager direkt im Projektordner:

```bash
xdg-open .
```

### 📌 Bilder einsortieren

**FAHRRAD-Bilder (BICYCLE):**

* `daten/train/bicycle/`
* `daten/test/bicycle/`

**KEIN FAHRRAD (NOT_BICYCLE):**

* `daten/train/not_bicycle/`
* `daten/test/not_bicycle/`

✅ **Wichtig**

* Nur `.jpg` / `.jpeg` / `.png`
* Dateinamen dürfen **egal wie** heißen (auch komisch aus dem Internet) ✅
  **Aber:** Bilder dürfen nicht in den falschen Ordner rutschen!

### 📌 Anzahl prüfen

Tippe:

```bash
ls daten/train/bicycle | wc -l
ls daten/train/not_bicycle | wc -l
ls daten/test/bicycle | wc -l
ls daten/test/not_bicycle | wc -l
```

**Tipp:** Versuche ungefähr gleich viele Bilder pro Ordner zu haben.

---

## 6) Trainingsprogramm erstellen: `fahrrad_lernen.py`

Öffne den Editor:

```bash
nano fahrrad_lernen.py
```

Kopiere jetzt **alles** hier rein:

```python
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
```

### 💾 Speichern + schließen

* `CTRL + O` → `ENTER`
* `CTRL + X`

---

## 7) Modell trainieren

Starte das Training:

```bash
cd ~/fahrrad_projekt
source meine_umgebung/bin/activate
python3 fahrrad_lernen.py
```

**Erwartung:**

* `Found XX images belonging to 2 classes.`
* `Epoch 1/5 ...`
* Am Ende:

  * `Saved as 'mein_fahrrad_modell.h5'`

Prüfe, ob die Dateien da sind:

```bash
ls -l mein_fahrrad_modell.h5 mein_fahrrad_modell.keras
```

---

## 8) (Optional) Drag & Drop aktivieren

Wenn du Bilder per Drag & Drop reinziehen willst:

```bash
pip install --no-cache-dir tkinterdnd2
```

---

## 9) Test-Programm mit Fenster erstellen: `testen.py`

Öffne:

```bash
nano testen.py
```

Kopiere **alles** hier rein (zeigt Bild + Ergebnis + Balken):

```python
import os
import sys
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image

MODEL_PATH = "mein_fahrrad_modell.h5"
IMG_SIZE = (150, 150)

DND_AVAILABLE = False
try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    DND_AVAILABLE = True
except Exception:
    DND_AVAILABLE = False


def predict_image(model, img_path: str):
    img = keras_image.load_img(img_path, target_size=IMG_SIZE)
    arr = keras_image.img_to_array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)

    pred = float(model.predict(arr, verbose=0)[0][0])

    # Häufige Zuordnung:
    # bicycle = 0, not_bicycle = 1
    prob_not_bicycle = pred
    prob_bicycle = 1.0 - pred

    if prob_bicycle >= prob_not_bicycle:
        label = "FAHRRAD"
        confidence = prob_bicycle
    else:
        label = "KEIN FAHRRAD"
        confidence = prob_not_bicycle

    return label, confidence, prob_bicycle, prob_not_bicycle


def is_image_file(path: str) -> bool:
    return path.lower().endswith((".jpg", ".jpeg", ".png"))


class FahrradGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Fahrrad-Erkenner (Raspberry Pi)")
        self.root.geometry("820x560")
        self.root.minsize(820, 560)

        if not os.path.isfile(MODEL_PATH):
            messagebox.showerror(
                "Modell fehlt",
                f"Modelldatei nicht gefunden:\n{MODEL_PATH}\n\n"
                "Bitte zuerst trainieren:\npython3 fahrrad_lernen.py"
            )
            self.root.destroy()
            return

        self.model = load_model(MODEL_PATH, compile=False)
        self._tk_preview = None

        top = tk.Frame(root)
        top.pack(fill="x", padx=12, pady=(12, 6))

        title = tk.Label(top, text="Fahrrad-Erkenner", font=("Arial", 20, "bold"))
        title.pack(anchor="w")

        subtitle_text = "Öffne ein JPG/PNG Bild, um es zu testen."
        if DND_AVAILABLE:
            subtitle_text += " Drag & Drop: AKTIV"
        else:
            subtitle_text += " (Drag & Drop: pip install tkinterdnd2)"
        self.subtitle = tk.Label(top, text=subtitle_text, font=("Arial", 10), fg="gray")
        self.subtitle.pack(anchor="w", pady=(4, 0))

        main = tk.Frame(root)
        main.pack(fill="both", expand=True, padx=12, pady=8)

        self.left = tk.Frame(main, bd=2, relief="groove")
        self.left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.drop_label = tk.Label(
            self.left,
            text="BILD HIER REINZIEHEN\n(oder 'Bild öffnen' klicken)",
            font=("Arial", 14, "bold"),
            bg="#f3f3f3",
            width=52,
            height=18
        )
        self.drop_label.pack(fill="both", expand=True, padx=10, pady=10)

        self.right = tk.Frame(main, width=320)
        self.right.pack(side="right", fill="y")

        btn_frame = tk.Frame(self.right)
        btn_frame.pack(fill="x", pady=(0, 10))

        self.open_btn = tk.Button(btn_frame, text="Bild öffnen", height=2, command=self.open_image)
        self.open_btn.pack(fill="x", pady=(0, 6))

        self.clear_btn = tk.Button(btn_frame, text="Zurücksetzen", height=2, command=self.clear)
        self.clear_btn.pack(fill="x")

        self.file_lbl = tk.Label(self.right, text="Datei: (keine)", wraplength=300, justify="left")
        self.file_lbl.pack(fill="x", pady=(10, 10))

        self.result_title = tk.Label(self.right, text="Ergebnis:", font=("Arial", 14, "bold"))
        self.result_title.pack(anchor="w")

        self.result_lbl = tk.Label(self.right, text="—", font=("Arial", 22, "bold"))
        self.result_lbl.pack(fill="x", pady=(6, 12))

        self.prob_lbl = tk.Label(self.right, text="Fahrrad: —\nKein Fahrrad: —", font=("Arial", 12), justify="left")
        self.prob_lbl.pack(fill="x", pady=(0, 10))

        self.conf_title = tk.Label(self.right, text="Sicherheit:", font=("Arial", 12, "bold"))
        self.conf_title.pack(anchor="w")

        self.canvas = tk.Canvas(self.right, width=300, height=34)
        self.canvas.pack(pady=(6, 0))

        self.canvas.create_rectangle(10, 10, 290, 24, outline="black")
        self.bar = self.canvas.create_rectangle(10, 10, 10, 24, fill="green", outline="")
        self.bar_text = self.canvas.create_text(150, 17, text="0%")

        if DND_AVAILABLE:
            self.drop_label.drop_target_register(DND_FILES)
            self.drop_label.dnd_bind("<<Drop>>", self.on_drop)

    def open_image(self):
        path = filedialog.askopenfilename(
            title="Bild auswählen",
            filetypes=[("Bilder", "*.jpg *.jpeg *.png"), ("Alle Dateien", "*.*")]
        )
        if path:
            self.handle_image(path)

    def on_drop(self, event):
        data = event.data.strip()
        if data.startswith("{") and data.endswith("}"):
            data = data[1:-1]
        path = data.split()[0]
        if os.path.isfile(path) and is_image_file(path):
            self.handle_image(path)
        else:
            messagebox.showerror("Fehler", "Bitte ein gültiges JPG/PNG Bild reinziehen.")

    def clear(self):
        self.file_lbl.configure(text="Datei: (keine)")
        self.result_lbl.configure(text="—", fg="black")
        self.prob_lbl.configure(text="Fahrrad: —\nKein Fahrrad: —")
        self.drop_label.configure(image="", text="BILD HIER REINZIEHEN\n(oder 'Bild öffnen' klicken)")
        self._tk_preview = None
        self.canvas.coords(self.bar, 10, 10, 10, 24)
        self.canvas.itemconfig(self.bar_text, text="0%")
        self.canvas.itemconfig(self.bar, fill="green")

    def handle_image(self, path: str):
        if not is_image_file(path):
            messagebox.showerror("Fehler", "Nur JPG/PNG Bilder sind erlaubt.")
            return

        self.file_lbl.configure(text=f"Datei: {path}")

        try:
            img = Image.open(path).convert("RGB")
            preview = img.copy()
            preview.thumbnail((560, 360))
            self._tk_preview = ImageTk.PhotoImage(preview)
            self.drop_label.configure(image=self._tk_preview, text="")
        except Exception as e:
            messagebox.showerror("Fehler", f"Bild konnte nicht geöffnet werden:\n{e}")
            return

        try:
            label, conf, p_bike, p_not = predict_image(self.model, path)
        except Exception as e:
            messagebox.showerror("Fehler", f"Vorhersage fehlgeschlagen:\n{e}")
            return

        self.result_lbl.configure(text=label, fg=("green" if label == "FAHRRAD" else "red"))
        self.prob_lbl.configure(text=f"Fahrrad: {p_bike:.4f}\nKein Fahrrad: {p_not:.4f}")

        conf_pct = int(round(conf * 100))
        x0 = 10
        x1 = 10 + int(280 * conf)
        self.canvas.coords(self.bar, x0, 10, x1, 24)
        self.canvas.itemconfig(self.bar_text, text=f"{conf_pct}%")
        self.canvas.itemconfig(self.bar, fill=("green" if label == "FAHRRAD" else "red"))


def main():
    if DND_AVAILABLE:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    FahrradGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
```

Speichern + schließen:

* `CTRL + O` → `ENTER`
* `CTRL + X`

---

## 10) Test-Fenster starten (GUI)

Starte die App:

```bash
cd ~/fahrrad_projekt
source meine_umgebung/bin/activate
python3 testen.py
```

Jetzt kannst du:

* **Bild öffnen** klicken
* oder ein Bild **reinziehen** (wenn tkinterdnd2 installiert ist)

---

## ✅ Warum erkennt er manchmal falsch?

Das ist normal, wenn:

* du **zu wenige Bilder** hast (z.B. nur 20–50)
* im falschen Ordner aus Versehen ein Fahrrad-Bild liegt
* die Bilder sind nicht abwechslungsreich genug

**Tipp:** Mit 200+ Bildern pro Klasse wird es deutlich besser.

---

## 🔍 Bonus: Prüfe die Klassen-Zuordnung

Manchmal ist die Zuordnung so:

* `bicycle = 0`
* `not_bicycle = 1`

Prüfe das so:

```bash
python3 -c "from tensorflow.keras.preprocessing.image import ImageDataGenerator; gen=ImageDataGenerator().flow_from_directory('daten/train'); print(gen.class_indices)"
```

---

Viel Spaß beim Trainieren! 🚲

```
```
