````md
# 🚲 Mein Computer lernt Fahrrad fahren (Raspberry Pi 5) — Kinder-README (DE)

Hier lernst du, wie dein Raspberry Pi Bilder anschaut und sagt:

✅ **BICYCLE** (Fahrrad)  
❌ **NOT BICYCLE** (kein Fahrrad)

**Wichtig:** Die Befehle im Terminal sind **Englisch** (so wie im Buch).  
Du tippst sie **Zeile für Zeile** genau so ein.

---

# 📦 0) Das Projekt herunterladen (große Datei ist NICHT auf GitHub)

Die Projekt-Datei ist zu groß für GitHub. Du lädst sie hier herunter:

👉 **Download-Link (LimeWire):**  
https://limewire.com/d/qLV4k#DsNmQDDfxe

## 0.1 So lädst du die Datei herunter (ganz einfach)
1. Öffne den Link im Browser.
2. Klicke auf **Download**.
3. Warte bis es fertig ist.

✅ Danach liegt die Datei meistens in **Downloads**:  
`/home/pi/Downloads/`

Die Datei heißt z.B.:
- `fahrrad_projekt.7z` (oder ähnlich)

---

# 🧰 1) Entpacken (Extract) + in den Home-Ordner legen

## Option A — mit File Manager (am leichtesten)
1. Öffne **File Manager**
2. Gehe zu **Downloads**
3. Rechtsklick auf `fahrrad_projekt.7z`
4. Wähle **Extract Here** oder **Extract to…**

✅ Danach hast du einen Ordner:
- `fahrrad_projekt`

## Option B — mit Terminal (wenn du lieber tippst)

Terminal öffnen und eingeben:

```bash
cd ~/Downloads
sudo apt update
sudo apt install -y p7zip-full
7z x fahrrad_projekt.7z
````

✅ Danach sollte der Ordner hier sein:
`~/Downloads/fahrrad_projekt`

---

## 1.1 Ordner in den Home-Ordner verschieben

Wir wollen den Projektordner hier haben:

✅ `~/fahrrad_projekt`

Verschieben:

```bash
mv ~/Downloads/fahrrad_projekt ~/
```

Prüfen:

```bash
ls ~
```

✅ Du solltest `fahrrad_projekt` sehen.

---

# 🟣 2) Terminal öffnen und in den Projektordner gehen

```bash
cd ~/fahrrad_projekt
pwd
```

✅ Erwartet (ähnlich):

```text
/home/pi/fahrrad_projekt
```

Wenn `cd` nicht klappt:

1. Tippe `ls ~`
2. Schau wie der Ordner wirklich heißt
3. Gehe dann in diesen Ordner

---

# 🛠️ 3) System updaten + Werkzeuge installieren

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y python3-pip python3-venv python3-tk
```

✅ Gut: keine roten **ERROR**-Zeilen.

---

# 🧪 4) Python-Umgebung (venv) erstellen und aktivieren

Eine venv ist wie eine saubere „Zauber-Box“ nur für dieses Projekt.

```bash
cd ~/fahrrad_projekt
python3 -m venv meine_umgebung
source meine_umgebung/bin/activate
```

✅ Wenn alles richtig ist, siehst du vorne:

```text
(meine_umgebung)
```

Dann:

```bash
python -m pip install -U pip setuptools wheel
```

---

# 📚 5) Python-Pakete installieren (stabil für Raspberry Pi)

```bash
pip install --no-cache-dir "protobuf>=5.28.0,<6" "flatbuffers>=24.3.25,<25"
pip install --no-cache-dir "tensorflow==2.20.0" "numpy" "pillow" "scipy"
```

(Optional) Mini-Test:

```bash
python3 -c "import tensorflow as tf; print('TF OK:', tf.__version__)"
```

---

# 🗂️ 6) Bilder-Ordner (Dataset) prüfen

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

# 🖼️ 7) Wo kommen die Bilder hin?

✅ **Fahrrad-Bilder** kommen hier rein:

* `daten/train/bicycle/`
* `daten/test/bicycle/`

✅ **Nicht-Fahrrad-Bilder** (Stuhl, Auto, Pflanze, Tasche …) kommen hier rein:

* `daten/train/not_bicycle/`
* `daten/test/not_bicycle/`

✅ Erlaubte Bildtypen:

* `.jpg` `.jpeg` `.png`

✅ Dateinamen dürfen so bleiben wie sie sind (egal!).

📂 Ordner im File Manager öffnen:

```bash
xdg-open .
```

---

# ⭐ Super wichtig: Mehr Bilder = schlauerer Computer!

Wenn dein Raspberry Pi manchmal falsch rät, ist das normal.

✅ Damit er genauer wird:

* Sammle **mehr** Bilder
* Sammle **verschiedenere** Bilder (andere Winkel, andere Orte, anderes Licht)
* Besonders bei **NOT BICYCLE** viele verschiedene Dinge (Stuhl, Auto, Pflanze, Schuhe, Helm, Scooter …)

Je mehr er sieht, desto besser lernt er.

---

# 🧠 8) Training starten (das „Gehirn“ bauen)

```bash
cd ~/fahrrad_projekt
source meine_umgebung/bin/activate
python3 fahrrad_lernen.py
```

✅ Am Ende entsteht die Modell-Datei:

* `mein_fahrrad_modell.h5`

Prüfen:

```bash
ls -l mein_fahrrad_modell.h5
```

---

# 🪟 9) Test-App starten (GUI)

```bash
cd ~/fahrrad_projekt
source meine_umgebung/bin/activate
python3 testen.py
```

Dann:

* Klicke **Open Image**
* Wähle ein Bild
* Schau das Ergebnis: **BICYCLE** oder **NOT BICYCLE**

---

# 🧲 10) Optional: Drag & Drop aktivieren

```bash
pip install --no-cache-dir tkinterdnd2
python3 testen.py
```

---

# ✅ Fertig!

Du hast deinem Raspberry Pi etwas Neues beigebracht. 🚲🤖
