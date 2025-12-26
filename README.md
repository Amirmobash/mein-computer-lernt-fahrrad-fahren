````md
# 🚲 Bicycle Detector (Raspberry Pi 5) — Schritt für Schritt (für Kinder)

✅ **Wichtig:** Die große Projekt-Datei ist NICHT direkt auf GitHub (zu groß).  
Du lädst sie über diesen Link herunter und machst dann weiter.

## 📥 1) Projekt-Datei herunterladen (LimeWire)
👉 Öffne diesen Link im Browser:

https://limewire.com/d/qLV4k#DsNmQDDfxe

Dann:
1. Klicke auf **Download**
2. Warte bis der Download fertig ist

✅ Die Datei liegt danach meistens im Ordner **Downloads**.

---

## 📦 2) Entpacken (Extract)
### Option A: Mit dem Datei-Manager (am einfachsten)
1. Öffne **File Manager**
2. Gehe zu **Downloads**
3. Rechtsklick auf die Datei (z.B. `fahrrad_projekt.7z`)
4. Klicke **Extract Here** oder **Extract to…**

Du bekommst danach einen Ordner: **`fahrrad_projekt`**

### Option B: Mit Terminal
Öffne Terminal und tippe:

```bash
cd ~/Downloads
7z x fahrrad_projekt.7z
````

---

## 📁 3) Ordner in den Home-Ordner verschieben

Wir wollen, dass der Ordner hier ist:

`/home/pi/fahrrad_projekt`

Wenn er noch in Downloads ist, verschiebe ihn so:

```bash
mv ~/Downloads/fahrrad_projekt ~/
```

✅ Prüfen:

```bash
ls ~
```

Du solltest `fahrrad_projekt` sehen.

---

# 🧪 Jetzt beginnt das Projekt!

## 4) In den Projektordner gehen

```bash
cd ~/fahrrad_projekt
pwd
```

---

## 5) System updaten + Tools installieren

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y python3-pip python3-venv python3-tk p7zip-full
```

---

## 6) Python-Umgebung (venv) erstellen und aktivieren

```bash
cd ~/fahrrad_projekt
python3 -m venv meine_umgebung
source meine_umgebung/bin/activate
```

✅ Wenn du `(meine_umgebung)` siehst, ist es richtig.

Dann:

```bash
python -m pip install -U pip setuptools wheel
```

---

## 7) Pakete installieren (stabil für Raspberry Pi)

```bash
pip install --no-cache-dir "protobuf>=5.28.0,<6" "flatbuffers>=24.3.25,<25"
pip install --no-cache-dir "tensorflow==2.20.0" "numpy" "pillow" "scipy"
```

(Optional) Test:

```bash
python3 -c "import tensorflow as tf; print('TF OK:', tf.__version__)"
```

---

## 8) Bilder-Ordner prüfen

Diese Ordner müssen existieren:

* `daten/train/bicycle/`
* `daten/train/not_bicycle/`
* `daten/test/bicycle/`
* `daten/test/not_bicycle/`

Check:

```bash
ls -R daten
```

---

## 9) ⭐ Tipp für bessere Treffer: Mehr Bilder = besser!

Wenn der Computer manchmal falsch liegt, ist das normal.

✅ Je mehr Bilder du sammelst, desto schlauer wird er:

* mehr Fahrräder (verschiedene Winkel, Orte)
* mehr Nicht-Fahrräder (Stuhl, Auto, Pflanze, Tasche, Schuhe, Helm…)

---

## 10) Training starten (Modell bauen)

```bash
cd ~/fahrrad_projekt
source meine_umgebung/bin/activate
python3 fahrrad_lernen.py
```

Am Ende entsteht:

* `mein_fahrrad_modell.h5`

Check:

```bash
ls -l mein_fahrrad_modell.h5
```

---

## 11) Test-App starten (GUI)

```bash
python3 testen.py
```

Dann:

* **Open Image** klicken
* Bild auswählen
* Ergebnis anschauen: **BICYCLE** oder **NOT BICYCLE**

---

## 12) Optional: Drag & Drop aktivieren

```bash
pip install --no-cache-dir tkinterdnd2
python3 testen.py
```

✅ Fertig! Viel Spaß 🚲🤖

```
