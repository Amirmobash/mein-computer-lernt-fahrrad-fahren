# testen.py
# Bicycle Detector GUI (English)
#
# Features:
# - Open an image (JPG/PNG) and show a preview
# - Predict: BICYCLE vs NOT BICYCLE
# - Shows BOTH probabilities:
#     bicycle = 1 - model_output
#     not_bicycle = model_output
# - Confidence bar + clear English result
# - Optional Drag & Drop (install: pip install tkinterdnd2)
#
# Run (inside venv):
#   python3 testen.py
#
# CLI mode (optional):
#   python3 testen.py daten/test/bicycle/your_image.jpg

import os
import sys
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image

# -----------------------------
# SETTINGS
# -----------------------------
MODEL_PATH = "mein_fahrrad_modell.h5"
IMG_SIZE = (150, 150)

# Optional Drag&Drop support
DND_AVAILABLE = False
try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    DND_AVAILABLE = True
except Exception:
    DND_AVAILABLE = False


def predict_image(model, img_path: str):
    """
    Your training showed class_indices like:
      {'bicycle': 0, 'not_bicycle': 1}

    With sigmoid output:
      model_output ~ 0.0 => class 0 => bicycle
      model_output ~ 1.0 => class 1 => not_bicycle

    So:
      prob_not_bicycle = pred
      prob_bicycle = 1 - pred
    """
    img = keras_image.load_img(img_path, target_size=IMG_SIZE)
    arr = keras_image.img_to_array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)

    pred = float(model.predict(arr, verbose=0)[0][0])  # prob for class "1"
    prob_not_bicycle = pred
    prob_bicycle = 1.0 - pred

    if prob_bicycle >= prob_not_bicycle:
        label = "BICYCLE"
        confidence = prob_bicycle
    else:
        label = "NOT BICYCLE"
        confidence = prob_not_bicycle

    return label, confidence, prob_bicycle, prob_not_bicycle


def is_image_file(path: str) -> bool:
    return path.lower().endswith((".jpg", ".jpeg", ".png"))


class BicycleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bicycle Detector (Raspberry Pi)")
        self.root.geometry("820x560")
        self.root.minsize(820, 560)

        # Load model (compile=False prevents extra warnings)
        if not os.path.isfile(MODEL_PATH):
            messagebox.showerror(
                "Model file not found",
                f"Cannot find model file:\n{MODEL_PATH}\n\n"
                "Please train first:\npython3 fahrrad_lernen.py"
            )
            self.root.destroy()
            return

        self.model = load_model(MODEL_PATH, compile=False)

        # Keep reference to preview image
        self._tk_preview = None

        # -----------------------------
        # UI LAYOUT
        # -----------------------------
        top = tk.Frame(root)
        top.pack(fill="x", padx=12, pady=(12, 6))

        title = tk.Label(top, text="Bicycle Detector", font=("Arial", 20, "bold"))
        title.pack(anchor="w")

        subtitle_text = (
            "Open a JPG/PNG image to classify it.\n"
            "Tip: Install Drag & Drop with: pip install tkinterdnd2"
        )
        self.subtitle = tk.Label(top, text=subtitle_text, font=("Arial", 10), fg="gray")
        self.subtitle.pack(anchor="w", pady=(4, 0))

        main = tk.Frame(root)
        main.pack(fill="both", expand=True, padx=12, pady=8)

        # Left: Drop/Preview area
        self.left = tk.Frame(main, bd=2, relief="groove")
        self.left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.drop_label = tk.Label(
            self.left,
            text="DROP IMAGE HERE\n(or click 'Open Image')",
            font=("Arial", 14, "bold"),
            bg="#f3f3f3",
            width=52,
            height=18
        )
        self.drop_label.pack(fill="both", expand=True, padx=10, pady=10)

        # Right: Controls + Results
        self.right = tk.Frame(main, width=320)
        self.right.pack(side="right", fill="y")

        btn_frame = tk.Frame(self.right)
        btn_frame.pack(fill="x", pady=(0, 10))

        self.open_btn = tk.Button(btn_frame, text="Open Image", height=2, command=self.open_image)
        self.open_btn.pack(fill="x", pady=(0, 6))

        self.clear_btn = tk.Button(btn_frame, text="Clear", height=2, command=self.clear)
        self.clear_btn.pack(fill="x")

        self.file_lbl = tk.Label(self.right, text="File: (none)", wraplength=300, justify="left")
        self.file_lbl.pack(fill="x", pady=(10, 10))

        self.result_title = tk.Label(self.right, text="Result:", font=("Arial", 14, "bold"))
        self.result_title.pack(anchor="w")

        self.result_lbl = tk.Label(self.right, text="—", font=("Arial", 22, "bold"))
        self.result_lbl.pack(fill="x", pady=(6, 12))

        self.prob_lbl = tk.Label(self.right, text="bicycle: —\nnot_bicycle: —", font=("Arial", 12), justify="left")
        self.prob_lbl.pack(fill="x", pady=(0, 10))

        # Confidence bar
        self.conf_title = tk.Label(self.right, text="Confidence:", font=("Arial", 12, "bold"))
        self.conf_title.pack(anchor="w")

        self.canvas = tk.Canvas(self.right, width=300, height=34)
        self.canvas.pack(pady=(6, 0))

        # bar border
        self.canvas.create_rectangle(10, 10, 290, 24, outline="black")
        self.bar = self.canvas.create_rectangle(10, 10, 10, 24, fill="green", outline="")
        self.bar_text = self.canvas.create_text(150, 17, text="0%")

        info = tk.Label(
            self.right,
            text="Model output is sigmoid.\n"
                 "We show both probabilities.\n"
                 "Higher probability decides the label.",
            font=("Arial", 9),
            fg="gray",
            justify="left"
        )
        info.pack(fill="x", pady=(10, 0))

        # Drag & drop enabling (if available)
        if DND_AVAILABLE:
            self.subtitle.configure(
                text="Open a JPG/PNG image to classify it.\nDrag & Drop: ENABLED"
            )
            self.drop_label.drop_target_register(DND_FILES)
            self.drop_label.dnd_bind("<<Drop>>", self.on_drop)

        # If user provides image path in CLI: python3 testen.py path/to/image.jpg
        if len(sys.argv) >= 2:
            path = sys.argv[1]
            if os.path.isfile(path) and is_image_file(path):
                self.handle_image(path)

    # -----------------------------
    # Actions
    # -----------------------------
    def open_image(self):
        path = filedialog.askopenfilename(
            title="Choose an image",
            filetypes=[("Images", "*.jpg *.jpeg *.png"), ("All files", "*.*")]
        )
        if path:
            self.handle_image(path)

    def on_drop(self, event):
        data = event.data.strip()
        # Handle {path} format
        if data.startswith("{") and data.endswith("}"):
            data = data[1:-1]

        # If multiple files dropped, take first
        path = data.split()[0]

        if os.path.isfile(path) and is_image_file(path):
            self.handle_image(path)
        else:
            messagebox.showerror("Error", "Please drop a valid JPG/PNG file.")

    def clear(self):
        self.file_lbl.configure(text="File: (none)")
        self.result_lbl.configure(text="—", fg="black")
        self.prob_lbl.configure(text="bicycle: —\nnot_bicycle: —")
        self.drop_label.configure(image="", text="DROP IMAGE HERE\n(or click 'Open Image')")
        self._tk_preview = None

        self.canvas.coords(self.bar, 10, 10, 10, 24)
        self.canvas.itemconfig(self.bar_text, text="0%")
        self.canvas.itemconfig(self.bar, fill="green")

    def handle_image(self, path: str):
        if not is_image_file(path):
            messagebox.showerror("Error", "Only JPG/PNG images are supported.")
            return

        self.file_lbl.configure(text=f"File: {path}")

        # Show preview
        try:
            img = Image.open(path).convert("RGB")
            preview = img.copy()
            preview.thumbnail((560, 360))
            self._tk_preview = ImageTk.PhotoImage(preview)
            self.drop_label.configure(image=self._tk_preview, text="")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open image:\n{e}")
            return

        # Predict
        try:
            label, conf, p_bike, p_not = predict_image(self.model, path)
        except Exception as e:
            messagebox.showerror("Error", f"Prediction failed:\n{e}")
            return

        # Update UI
        self.result_lbl.configure(text=label, fg=("green" if label == "BICYCLE" else "red"))
        self.prob_lbl.configure(
            text=f"bicycle: {p_bike:.4f}\nnot_bicycle: {p_not:.4f}"
        )

        # Confidence bar
        conf_pct = int(round(conf * 100))
        x0 = 10
        x1 = 10 + int(280 * (conf / 1.0))
        self.canvas.coords(self.bar, x0, 10, x1, 24)
        self.canvas.itemconfig(self.bar_text, text=f"{conf_pct}%")
        self.canvas.itemconfig(self.bar, fill=("green" if label == "BICYCLE" else "red"))


def main():
    # Build root window
    if DND_AVAILABLE:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()

    BicycleGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
