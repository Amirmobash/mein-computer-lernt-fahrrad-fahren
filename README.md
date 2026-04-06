# 🚲 Bicycle Classifier for Raspberry Pi 5  
### Train a Computer Vision Model to Recognize Bicycles – No Cloud Needed

[![Watch the tutorial on YouTube](https://img.shields.io/badge/YouTube-Watch%20tutorial-red?logo=youtube)](https://youtu.be/eXKJaKfzpSQ?si=P_K_YV2heAU3mP6X)
[![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-5-C51A4A?logo=raspberry-pi)](https://www.raspberrypi.com/products/raspberry-pi-5/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.20-FF6F00?logo=tensorflow)](https://www.tensorflow.org/)

> **Teach your Raspberry Pi 5 to sort images into `BICYCLE` 🚲 and `NOT BICYCLE` ❌**  
> This project includes a full training pipeline + a GUI test app. Perfect for learning AI on edge devices.

---

## 📺 Video Guide (German / English subtitles available)

👉 **Click the badge above or use this link:**  
[https://youtu.be/eXKJaKfzpSQ](https://youtu.be/eXKJaKfzpSQ?si=P_K_YV2heAU3mP6X)

The video walks you through every step – from downloading the dataset to training and testing your own model.

---

## 🧠 What you will build

- A **neural network** (TensorFlow/Keras) that classifies images as bicycle or not.
- A **graphical application** to test new images with drag & drop (optional).
- A **fully offline AI** that runs entirely on your Raspberry Pi 5.

---

## 📦 Project Download (Large File – not on GitHub)

Because the dataset contains many images, the project archive is hosted on Dropbox:

🔗 **[Download `fahrrad_projekt.7z`](https://www.nivta.de/Downloads/index.html))**

After downloading, place the file in `/home/pi/Downloads/` or use the commands below.

---

## 🛠️ Setup Instructions (Raspberry Pi OS – Bookworm)

Open a terminal and follow these steps.

### 1️⃣ Update system & install dependencies

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y python3-pip python3-venv python3-tk p7zip-full
```

### 2️⃣ Extract the project archive

```bash
cd ~/Downloads
7z x fahrrad_projekt.7z
mv ~/Downloads/fahrrad_projekt ~/
cd ~/fahrrad_projekt
```

### 3️⃣ Create a virtual environment (isolated Python)

```bash
python3 -m venv meine_umgebung
source meine_umgebung/bin/activate
python -m pip install -U pip setuptools wheel
```

### 4️⃣ Install required Python packages

```bash
pip install --no-cache-dir "protobuf>=5.28.0,<6" "flatbuffers>=24.3.25,<25"
pip install --no-cache-dir "tensorflow==2.20.0" "numpy" "pillow" "scipy"
```

> ✅ Optional: Install `tkinterdnd2` for drag & drop support in the test app:
> ```bash
> pip install tkinterdnd2
> ```

### 5️⃣ Prepare your image dataset

Place your own images into these folders:

| Category         | Training folder                         | Testing folder                        |
|------------------|-----------------------------------------|---------------------------------------|
| `BICYCLE` 🚲     | `daten/train/bicycle/`                  | `daten/test/bicycle/`                 |
| `NOT BICYCLE` ❌ | `daten/train/not_bicycle/`              | `daten/test/not_bicycle/`             |

Supported formats: `.jpg`, `.jpeg`, `.png`

> 💡 **Tip for better accuracy**  
> - Add **many different images** (different angles, lighting, backgrounds).  
> - For `NOT BICYCLE`, include chairs, cars, bags, helmets, scooters – anything that is **not** a bicycle.  
> - The more diverse your training data, the smarter your model becomes.

### 6️⃣ Train the model

```bash
cd ~/fahrrad_projekt
source meine_umgebung/bin/activate
python3 fahrrad_lernen.py
```

When training finishes, you will get a file:  
**`mein_fahrrad_modell.h5`** (the trained “brain”).

### 7️⃣ Run the test GUI

```bash
python3 testen.py
```

Click **Open Image** → select a picture → see the prediction:  
**BICYCLE** or **NOT BICYCLE**.

---

## 🔍 Troubleshooting & FAQs

### ❌ Model misclassifies a non‑bicycle as a bicycle

**Solutions:**  
1. Add more **diverse** non‑bicycle images (different objects, scenes).  
2. Verify that no bicycle images accidentally ended up in the `not_bicycle` folders.  
3. Retrain the model after cleaning the dataset.

### ❌ “ModuleNotFoundError: No module named 'tkinter'”

Run:
```bash
sudo apt install python3-tk
```

### ❌ Training is very slow

- Make sure you are using a **Raspberry Pi 5** (older models are much slower).  
- Reduce image sizes (the script already resizes to 150x150).  
- Use fewer training epochs (edit `fahrrad_lernen.py` and lower `epochs`).

### ❌ I get a memory error during training

Close other applications and try adding `batch_size=16` in the `model.fit()` call inside the training script.

---

## 📁 Project structure after extraction

```
~/fahrrad_projekt/
├── daten/
│   ├── train/
│   │   ├── bicycle/
│   │   └── not_bicycle/
│   └── test/
│       ├── bicycle/
│       └── not_bicycle/
├── fahrrad_lernen.py          # training script
├── testen.py                  # GUI testing app
├── meine_umgebung/            # Python virtual environment
└── mein_fahrrad_modell.h5     # generated after training
```

---

## 🧪 Requirements (tested on)

- **Hardware:** Raspberry Pi 5 (4GB or 8GB)  
- **OS:** Raspberry Pi OS Bookworm (64-bit)  
- **Python:** 3.11+  
- **TensorFlow:** 2.20.0 (optimized for ARM64)

---

## 🙌 Credits & License

- Project created by **Amir Mobasheraghdam** (see video description)  
- Free to use for personal & educational purposes  
- If you improve the model or dataset, feel free to share your results!

---

## 🔗 Links

- [📺 Full video tutorial](https://youtu.be/eXKJaKfzpSQ?si=P_K_YV2heAU3mP6X)  
- [💾 Project download ](https://www.nivta.de/Downloads/index.html)  
- [🐍 TensorFlow on Raspberry Pi](https://www.tensorflow.org/install/pip)

---

**Happy building! 🚲🤖**  
*Your Raspberry Pi will soon be a bicycle‑spotting expert.*
```
