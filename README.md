# Mein Computer lernt Fahrrad fahren
**Ein Mitmach-Buch von Finn** :contentReference[oaicite:1]{index=1}

Dieses Repository begleitet das Kinder-Mitmachbuch **„Mein Computer lernt Fahrrad fahren“**.
Kinder lernen Schritt für Schritt auf einem **Raspberry Pi (Modell 4 oder 5)**, wie ein kleines Programm Bilder in **„BICYCLE“** und **„NOT BICYCLE“** einteilt – spielerisch, kindgerecht und praktisch. :contentReference[oaicite:2]{index=2}

> Wichtig: Alle technischen Befehle und Code-Beispiele sind absichtlich **in ENGLISCH**, damit sie exakt so funktionieren, wie der Computer sie erwartet. :contentReference[oaicite:3]{index=3}

---

## Inhalt des Buchs (Kapitelübersicht)
- Hinweis für Erwachsene
- Regeln für dieses Mitmach-Buch
- Kapitel 1–11: Vom Terminal bis zum fertigen Modell
- Anhang A: Mini-Spickzettel (Befehle)
- Anhang B: Häufige Probleme & ruhige Lösungen
- Danksagung :contentReference[oaicite:4]{index=4}

---

## Was du hier findest
- 📘 **Manuskript (PDF)** (falls du es in `manuscript/` ablegst)
- 🧠 **Python-Code** zum Trainieren eines kleinen Bildklassifikations-Modells (Pi-friendly)
- 🗂️ **Projektstruktur** (Ordner für Trainings- und Testbilder)
- 🧩 Platz für **Cover/Illustrationen/Screenshots** (in `assets/`)

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

### 4) Benötigte Bibliotheken

```bash
pip install tensorflow pillow numpy
```

### 5) Ordnerstruktur für Bilder

```bash
mkdir -p daten/train/bicycle daten/train/not_bicycle daten/test/bicycle daten/test/not_bicycle
```

Lege danach Bilder ab wie z.B.: 

* `daten/train/bicycle/bike_01.jpg`
* `daten/train/not_bicycle/chair_01.jpg`
* `daten/test/bicycle/bike_test_01.jpg`
* `daten/test/not_bicycle/plant_test_01.jpg`

---

## Trainieren (fahrrad_lernen.py)

Erstelle im Projektordner eine Datei **`fahrrad_lernen.py`** und nutze den Code aus dem Buch. 

Dann Training starten:

```bash
python3 fahrrad_lernen.py
```

Am Ende wird das Modell gespeichert als:

* `mein_fahrrad_modell.h5` 

---

## Testen (testen.py)

Erstelle **`testen.py`** (siehe Buch) und setze `img_path` auf ein echtes Testbild. 

Dann:

```bash
python3 testen.py
```

---Amir Mobasheraghdam

## Repository-Struktur (Empfehlung)

```
.
├─ manuscript/
│  └─ Mein_Computer_lernt_Fahrrad_fahren_Manuskript_Voll.pdf
├─ code/
│  ├─ fahrrad_lernen.py
│  └─ testen.py
├─ assets/
│  ├─ images/        # Cover/Illustrationen
│  └─ screenshots/   # Raspberry-Pi Screenshots
└─ README.md
```

---

## Credits

* **Autor:** Amir Mobasher
* **Technische Übersetzung & fachliche Bearbeitung:** Ladan Seddighi
* **(Optional) Technische Prüfung (IT):** [Name eintragen]

---

## Lizenz / Copyright (WICHTIG)

Bitte wähle bewusst, was auf GitHub öffentlich sein soll.

### Option A (empfohlen für Bücher):

* **Manuskript/Book-Text:** © [Jahr] Amir Mobasher – **Alle Rechte vorbehalten**
* **Code (optional):** MIT License (frei nutzbar)

### Option B:

* Alles unter einer Creative-Commons-Lizenz (nur wenn du das wirklich willst)

> Trage hier deine Entscheidung ein:

* Manuskript-Lizenz: **[All rights reserved / ...]**
* Code-Lizenz: **[MIT / ...]**

---

## Kontakt

* E-Mail: [deine E-Mail]
* Website (optional): [Link]

---

## Hinweis

Dieses Repository ist für Lern- und Bildungszwecke gedacht.
Bilder, Logos und Marken gehören ihren jeweiligen Inhabern.
