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

* **Buchtext/Manuskript:** © 2025 AmirMobasheraghdam — Alle Rechte vorbehalten (nicht in diesem Repo)
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
````

#
```bash
git pull
# README.md را با متن بالا جایگزین کن
# .gitignore را ایجاد کن

git add README.md .gitignore
git commit -m "Clean README, prevent book leaks, add gitignore"
git push
