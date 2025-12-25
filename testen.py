# testen.py
# GUI test app (English) — drag & drop an image (if tkinterdnd2 is installed)
# or click "Open Image". Shows the image + prediction + probability.

import os
import sys
import numpy as np
from PIL import Image, ImageTk

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image

MODEL_PATH = "mein_fahrrad_modell.h5"
IMG_SIZE = (150, 150)
THRESHOLD = 0.5

# Optional drag & drop support
DND_AVAILABLE = False
try:
    from tkinterdnd2 import TkinterDnD, DND_FILES  # pip install tkinterdnd2
    DND_AVAILABLE = True
except Exception:
    DND_AVAILABLE = False

import tkinter as tk
from tkinter import filedialog, messagebox


def predict_image(model, img_path: str):
    """Return (probability, label_text). Probability is model output (0..1)."""
    img = keras_image.load_img(img_path, target_size=IMG_SIZE)
    arr = keras_image.img_to_array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)

    pred = model.predict(arr, verbose=0)[0][0]
    label = "BICYCLE" if pred > THRESHOLD else "NOT BICYCLE"
    return float(pred), label


class App:
    def __init__(self, root, model):
        self.root = root
        self.model = model
        self.root.title("Bicycle Detector (Raspberry Pi)")

        self.root.geometry("900x520")
        self.root.minsize(900, 520)

        # Top instructions
        self.title_lbl = tk.Label(
            root,
            text="Drop an image here (JPG/PNG) or click 'Open Image' — English output",
            font=("Arial", 14),
        )
        self.title_lbl.pack(pady=10)

        # Main frame
        self.main = tk.Frame(root)
        self.main.pack(fill="both", expand=True, padx=12, pady=8)

        # Left: drop area + image preview
        self.left = tk.Frame(self.main)
        self.left.pack(side="left", fill="both", expand=True)

        self.drop_area = tk.Label(
            self.left,
            text="DROP IMAGE HERE\n(JPG / PNG)",
            font=("Arial", 16, "bold"),
            relief="ridge",
            bd=3,
            width=40,
            height=18,
            bg="#f2f2f2",
        )
        self.drop_area.pack(fill="both", expand=True)

        self.preview_lbl = tk.Label(self.left)
        self.preview_lbl.pack(pady=10)

        # Right: controls + results
        self.right = tk.Frame(self.main, width=320)
        self.right.pack(side="right", fill="y", padx=12)

        self.open_btn = tk.Button(self.right, text="Open Image", command=self.open_file, height=2)
        self.open_btn.pack(fill="x", pady=6)

        self.path_lbl = tk.Label(self.right, text="File: (none)", wraplength=300, justify="left")
        self.path_lbl.pack(fill="x", pady=10)

        self.result_title = tk.Label(self.right, text="Result:", font=("Arial", 14, "bold"))
        self.result_title.pack(anchor="w", pady=(10, 2))

        self.result_lbl = tk.Label(self.right, text="—", font=("Arial", 20, "bold"))
        self.result_lbl.pack(fill="x", pady=6)

        self.prob_lbl = tk.Label(self.right, text="Probability: —", font=("Arial", 12))
        self.prob_lbl.pack(fill="x", pady=4)

        self.hint_lbl = tk.Label(
            self.right,
            text=f"Rule: probability > {THRESHOLD} => BICYCLE",
            font=("Arial", 10),
            fg="gray",
        )
        self.hint_lbl.pack(fill="x", pady=6)

        self.quit_btn = tk.Button(self.right, text="Quit", command=root.quit, height=2)
        self.quit_btn.pack(fill="x", pady=18)

        # Enable drag & drop if available
        if DND_AVAILABLE and hasattr(self.drop_area, "drop_target_register"):
            self.drop_area.drop_target_register(DND_FILES)
            self.drop_area.dnd_bind("<<Drop>>", self.on_drop)
            self.drop_area.config(text="DROP IMAGE HERE\n(JPG / PNG)\n(Drag & Drop is ON)")
        else:
            self.drop_area.config(text="DROP IMAGE HERE\n(JPG / PNG)\n(Install drag & drop: pip install tkinterdnd2)")

        # If user passed a path in terminal: python3 testen.py path/to/img.jpg
        if len(sys.argv) >= 2:
            p = sys.argv[1]
            if os.path.isfile(p):
                self.handle_image(p)

    def open_file(self):
        filetypes = [("Images", "*.jpg *.jpeg *.png *.JPG *.JPEG *.PNG"), ("All files", "*.*")]
        path = filedialog.askopenfilename(title="Choose an image", filetypes=filetypes)
        if path:
            self.handle_image(path)

    def on_drop(self, event):
        # event.data may contain braces and multiple files; take first
        data = event.data.strip()
        # Remove surrounding braces: {path}
        if data.startswith("{") and data.endswith("}"):
            data = data[1:-1]
        # If multiple files are dropped, they may be space-separated
        path = data.split()[0]
        if os.path.isfile(path):
            self.handle_image(path)
        else:
            messagebox.showerror("Error", "Dropped item is not a file.")

    def handle_image(self, path: str):
        ext_ok = path.lower().endswith((".jpg", ".jpeg", ".png"))
        if not ext_ok:
            messagebox.showerror("Error", "Please use JPG or PNG.")
            return

        self.path_lbl.config(text=f"File: {path}")

        # Show image preview (fit to a safe size)
        try:
            pil = Image.open(path).convert("RGB")
            pil_preview = pil.copy()
            pil_preview.thumbnail((520, 320))
            tk_img = ImageTk.PhotoImage(pil_preview)
            self.preview_lbl.config(image=tk_img)
            self.preview_lbl.image = tk_img
        except Exception as e:
            messagebox.showerror("Error", f"Could not open image:\n{e}")
            return

        # Predict
        try:
            prob, label = predict_image(self.model, path)
        except Exception as e:
            messagebox.showerror("Error", f"Prediction failed:\n{e}")
            return

        # Display results
        self.result_lbl.config(text=label)
        self.prob_lbl.config(text=f"Probability: {prob:.4f}")

        if label == "BICYCLE":
            self.result_lbl.config(fg="green")
        else:
            self.result_lbl.config(fg="red")


def main():
    # Check model exists
    if not os.path.isfile(MODEL_PATH):
        print(f"ERROR: Model file not found: {MODEL_PATH}")
        print("Run training first: python3 fahrrad_lernen.py")
        sys.exit(1)

    # Load model
    model = load_model(MODEL_PATH)

    # Create GUI
    if DND_AVAILABLE:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()

    App(root, model)
    root.mainloop()


if __name__ == "__main__":
    main()
