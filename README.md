# 🚲 Mein Computer lernt von mir (Raspberry Pi 5)
## Kinder-README (Deutsch) — Befehle & Code sind Englisch ✅

Hallo! In diesem Projekt lernt dein Raspberry Pi Bilder zu sortieren:

✅ **BICYCLE** (Fahrrad)  
❌ **NOT BICYCLE** (kein Fahrrad)

Du trainierst zuerst ein Modell (das ist wie ein kleines „Gehirn“)  
und testest danach Bilder in einer App.

---

# 0) 📥 Das Projekt herunterladen (große Datei)


## 0.1 Download (super einfach)
1) Öffne den Link im Browser  
2) Klicke **Download**  
3) Warte bis es fertig ist

✅ Danach liegt die Datei meistens hier:
`/home/pi/Downloads/`

Die Datei heißt z.B.:
`fahrrad_projekt.7z`

---

# 1) 📦 Entpacken (Extract)

## Option A — File Manager (am leichtesten)
1) Öffne **File Manager**
2) Gehe zu **Downloads**
3) Rechtsklick auf `fahrrad_projekt.7z`
4) Klicke **Extract Here** oder **Extract to…**

✅ Danach hast du einen Ordner:
`fahrrad_projekt`

## Option B — Terminal (wenn du lieber tippst)
Öffne Terminal und tippe:

```bash
cd ~/Downloads
sudo apt update
sudo apt install -y p7zip-full
7z x fahrrad_projekt.7z
````

---

# 2) 📁 Ordner in den Home-Ordner verschieben (wichtig!)

Wir wollen den Projektordner hier haben:
✅ `/home/pi/fahrrad_projekt`  (kurz: `~/fahrrad_projekt`)

Wenn der Ordner noch in Downloads ist, verschiebe ihn so:

```bash
mv ~/Downloads/fahrrad_projekt ~/
```

Prüfen:

```bash
ls ~
```

✅ Du solltest `fahrrad_projekt` sehen.

---

# 3) 🟣 In den Projektordner gehen

```bash
cd ~/fahrrad_projekt
pwd
```

✅ Erwartet (ähnlich):
`/home/pi/fahrrad_projekt`

---

# 4) 🛠️ System updaten + Tools installieren

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y python3-pip python3-venv python3-tk
```

✅ Gut: keine roten **ERROR**-Zeilen.

---

# 5) 🧪 Python-Umgebung (venv) erstellen & aktivieren

Eine venv ist wie eine „Zauber-Box“ nur für dieses Projekt.

```bash
cd ~/fahrrad_projekt
python3 -m venv meine_umgebung
source meine_umgebung/bin/activate
```

✅ Wenn alles richtig ist, siehst du vorne:
`(meine_umgebung)`

Dann:

```bash
python -m pip install -U pip setuptools wheel
```

---

# 6) 📚 Pakete installieren (stabil für Raspberry Pi)

```bash
pip install --no-cache-dir "protobuf>=5.28.0,<6" "flatbuffers>=24.3.25,<25"
pip install --no-cache-dir "tensorflow==2.20.0" "numpy" "pillow" "scipy"
```

(Optional) Mini-Test:

```bash
python3 -c "import tensorflow as tf; print('TF OK:', tf.__version__)"
```

---

# 7) 🗂️ Bilder-Ordner prüfen (Dataset)

Im Projekt gibt es diese Ordner:

* `daten/train/bicycle/`
* `daten/train/not_bicycle/`
* `daten/test/bicycle/`
* `daten/test/not_bicycle/`

Prüfen:

```bash
cd ~/fahrrad_projekt
ls -R daten
```

---

# 8) 🖼️ Bilder: Wo kommen sie hin?

✅ **Fahrrad-Bilder** kommen hier rein:

* `daten/train/bicycle/`
* `daten/test/bicycle/`

✅ **Nicht-Fahrrad-Bilder** (Stuhl, Auto, Pflanze, Tasche …) kommen hier rein:

* `daten/train/not_bicycle/`
* `daten/test/not_bicycle/`

✅ Erlaubte Bildtypen:
`.jpg` `.jpeg` `.png`

✅ Dateinamen sind egal (du darfst die Download-Namen lassen).

Ordner im File Manager öffnen:

```bash
xdg-open .
```

---

# ⭐ Super Tipp: Mehr Bilder = schlauerer Computer!

Wenn dein Raspberry Pi manchmal falsch rät, ist das normal.

✅ Für bessere Genauigkeit:

* Sammle **mehr** Bilder
* Sammle **verschiedene** Bilder (anderes Licht, andere Orte, andere Winkel)
* Besonders bei **NOT BICYCLE** viele verschiedene Dinge (Stuhl, Auto, Schuhe, Helm, Scooter …)

Je mehr er sieht, desto besser lernt er.

---

# 9) 🧠 Training starten (Gehirn bauen)

```bash
cd ~/fahrrad_projekt
source meine_umgebung/bin/activate
python3 fahrrad_lernen.py
```

✅ Am Ende entsteht die Modell-Datei:
`mein_fahrrad_modell.h5`

Prüfen:

```bash
ls -l mein_fahrrad_modell.h5
```

---

# 10) 🪟 Test-App starten (GUI)

```bash
cd ~/fahrrad_projekt
source meine_umgebung/bin/activate
python3 testen.py
```

Dann:

* **Open Image** klicken
* Bild auswählen
* Ergebnis ansehen: **BICYCLE** oder **NOT BICYCLE**

---

# 11) 🧲 Optional: Drag & Drop aktivieren

```bash
pip install --no-cache-dir tkinterdnd2
python3 testen.py
```

---

# 12) Wenn es falsch erkennt (NOT BICYCLE → BICYCLE) Amir Mobasheraghdam

✅ Lösung:

1. Mehr Bilder sammeln (besonders NOT BICYCLE Vielfalt)
2. Prüfen, dass kein Fahrrad im `not_bicycle` Ordner ist
3. Neu trainieren:

```bash
python3 fahrrad_lernen.py
```

---

✅ Fertig! Viel Spaß 🚲🤖
