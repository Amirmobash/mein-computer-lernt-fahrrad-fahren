import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from dataclasses import dataclass
from typing import Dict, Tuple, Optional

import numpy as np
from PIL import Image, ImageTk
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image

# ============================================================
# Kid-friendly Bicycle Detector (EN/DE) for Raspberry Pi OS
# File: testen.py
# ============================================================
# What you need installed in your venv:
#   pip install tensorflow pillow numpy scipy
# Optional for drag & drop:
#   pip install tkinterdnd2
# ============================================================

MODEL_PATH = "mein_fahrrad_modell.h5"
IMG_SIZE = (150, 150)           # must match training
PREVIEW_MAX = (520, 340)        # preview size on screen
PATH_MAX_LEN = 60               # how long file paths can be shown before shortening

# Training folder mapping (most common):
# bicycle = 0, not_bicycle = 1
# model output = sigmoid -> probability of class 1 (not_bicycle)
# so:
#   prob_not_bicycle = pred
#   prob_bicycle     = 1 - pred


# ---------------------------
# Optional Drag & Drop support
# ---------------------------
DND_AVAILABLE = False
DND_FILES = None
TkRoot = tk.Tk
try:
    from tkinterdnd2 import TkinterDnD, DND_FILES as _DND_FILES  # type: ignore
    DND_AVAILABLE = True
    DND_FILES = _DND_FILES
    TkRoot = TkinterDnD.Tk  # type: ignore
except Exception:
    DND_AVAILABLE = False
    DND_FILES = None
    TkRoot = tk.Tk


# ---------------------------
# Translations (EN/DE)
# ---------------------------
def _how_it_works_text_en() -> str:
    return (
        "HOW IT WORKS (Kid-friendly)\n"
        "\n"
        "1) What is the model?\n"
        "   A model is a tiny 'brain file' that learned from many pictures.\n"
        "   Our model file is called: mein_fahrrad_modell.h5\n"
        "\n"
        "2) What does training mean?\n"
        "   Training is like practice. The computer saw bicycle pictures and\n"
        "   not-bicycle pictures and learned patterns (shapes, edges, circles).\n"
        "\n"
        "3) What happens when you test one image?\n"
        "   - The program makes the image smaller (150x150 pixels).\n"
        "   - It asks the model: 'Is this a bicycle?'\n"
        "   - The model answers with a number from 0.0 to 1.0.\n"
        "\n"
        "4) What is probability?\n"
        "   Probability is a 'confidence number'.\n"
        "   Example:\n"
        "     Bicycle: 0.80  means 'I am pretty sure it is a bicycle'.\n"
        "     Not Bicycle: 0.80 means 'I am pretty sure it is NOT a bicycle'.\n"
        "\n"
        "5) Why can it be wrong sometimes?\n"
        "   - Too few training pictures.\n"
        "   - Pictures are blurry or very different.\n"
        "   - A not-bicycle picture looks like a bicycle (circles like wheels).\n"
        "\n"
        "Tip: More good training pictures usually makes the model better!"
    )


def _how_it_works_text_de() -> str:
    return (
        "WIE FUNKTIONIERT DAS? (Kinderleicht)\n"
        "\n"
        "1) Was ist das Modell?\n"
        "   Ein Modell ist wie eine kleine 'Gehirn-Datei'. Es hat aus vielen\n"
        "   Bildern gelernt. Unsere Datei heißt: mein_fahrrad_modell.h5\n"
        "\n"
        "2) Was bedeutet Training?\n"
        "   Training ist Üben. Der Computer sieht Fahrrad-Bilder und\n"
        "   Nicht-Fahrrad-Bilder und lernt Muster (Formen, Kanten, Kreise).\n"
        "\n"
        "3) Was passiert beim Testen eines Bildes?\n"
        "   - Das Programm macht das Bild kleiner (150x150 Pixel).\n"
        "   - Es fragt das Modell: 'Ist das ein Fahrrad?'\n"
        "   - Das Modell antwortet mit einer Zahl von 0.0 bis 1.0.\n"
        "\n"
        "4) Was ist Wahrscheinlichkeit?\n"
        "   Das ist eine 'Sicherheits-Zahl'.\n"
        "   Beispiel:\n"
        "     Fahrrad: 0.80  heißt 'Ziemlich sicher Fahrrad'.\n"
        "     Kein Fahrrad: 0.80 heißt 'Ziemlich sicher kein Fahrrad'.\n"
        "\n"
        "5) Warum kann es manchmal falsch liegen?\n"
        "   - Zu wenige Trainingsbilder.\n"
        "   - Bilder sind unscharf oder sehr unterschiedlich.\n"
        "   - Ein Nicht-Fahrrad-Bild sieht aus wie ein Fahrrad (Kreise wie Räder).\n"
        "\n"
        "Tipp: Mit mehr guten Trainingsbildern wird das Modell oft besser!"
    )


T: Dict[str, Dict[str, str]] = {
    "EN": {
        "app_title": "Bicycle Detector (Raspberry Pi)",
        "subtitle_dnd_on": "Drop a JPG/PNG image or click 'Open Image'  •  Drag & Drop: ON",
        "subtitle_dnd_off": "Drop a JPG/PNG image or click 'Open Image'  •  Drag & Drop: install: pip install tkinterdnd2",
        "drop_placeholder": "DROP IMAGE HERE\n(or click 'Open Image')",
        "btn_open": "Open Image",
        "btn_clear": "Clear",
        "btn_quit": "Quit",
        "label_language": "Language:",
        "file_none": "File: (none)",
        "result_title": "Result:",
        "prob_title": "Probabilities:",
        "prob_bike": "Bicycle",
        "prob_not": "Not Bicycle",
        "confidence_title": "Confidence:",
        "how_title": "How it works",
        "err_title": "Error",
        "err_model_missing": "Model file not found:\n{path}\n\nTrain first:\npython3 fahrrad_lernen.py",
        "err_not_image": "Please choose a JPG or PNG image.",
        "err_open_image": "Could not open the image:\n{msg}",
        "err_predict": "Prediction failed:\n{msg}",
    },
    "DE": {
        "app_title": "Fahrrad-Erkenner (Raspberry Pi)",
        "subtitle_dnd_on": "Ziehe ein JPG/PNG Bild rein oder klicke 'Bild öffnen'  •  Drag & Drop: AN",
        "subtitle_dnd_off": "Ziehe ein JPG/PNG Bild rein oder klicke 'Bild öffnen'  •  Drag & Drop: installieren: pip install tkinterdnd2",
        "drop_placeholder": "BILD HIER REINZIEHEN\n(oder 'Bild öffnen' klicken)",
        "btn_open": "Bild öffnen",
        "btn_clear": "Zurücksetzen",
        "btn_quit": "Beenden",
        "label_language": "Sprache:",
        "file_none": "Datei: (keine)",
        "result_title": "Ergebnis:",
        "prob_title": "Wahrscheinlichkeiten:",
        "prob_bike": "Fahrrad",
        "prob_not": "Kein Fahrrad",
        "confidence_title": "Sicherheit:",
        "how_title": "Wie funktioniert das?",
        "err_title": "Fehler",
        "err_model_missing": "Modelldatei nicht gefunden:\n{path}\n\nBitte zuerst trainieren:\npython3 fahrrad_lernen.py",
        "err_not_image": "Bitte ein JPG oder PNG Bild auswählen.",
        "err_open_image": "Bild konnte nicht geöffnet werden:\n{msg}",
        "err_predict": "Vorhersage fehlgeschlagen:\n{msg}",
    },
}


def how_text(lang: str) -> str:
    return _how_it_works_text_en() if lang == "EN" else _how_it_works_text_de()


# ---------------------------
# Helper functions required
# ---------------------------
def shorten_path(path: str, max_len: int = PATH_MAX_LEN) -> str:
    """Shorten a long path to show it nicely in the GUI."""
    if not path:
        return path
    if len(path) <= max_len:
        return path
    # keep start and end
    keep = max_len - 5
    front = keep // 2
    back = keep - front
    return path[:front] + " ... " + path[-back:]


def is_image_file(path: str) -> bool:
    return path.lower().endswith((".jpg", ".jpeg", ".png"))


def predict_image(model, path: str) -> Tuple[str, float, float, float]:
    """
    Predict one image.
    Returns:
      label_key: "BICYCLE" or "NOT_BICYCLE"
      conf: confidence of the winning label (0..1)
      p_bike: probability of bicycle (0..1)
      p_not: probability of not_bicycle (0..1)
    """
    img = keras_image.load_img(path, target_size=IMG_SIZE)
    arr = keras_image.img_to_array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)

    pred = float(model.predict(arr, verbose=0)[0][0])  # sigmoid output (0..1)

    p_not = pred
    p_bike = 1.0 - pred

    if p_bike >= p_not:
        return "BICYCLE", p_bike, p_bike, p_not
    return "NOT_BICYCLE", p_not, p_bike, p_not


@dataclass
class Colors:
    ok: str = "#1f8f3a"
    bad: str = "#cc1f1f"
    neutral: str = "#1f1f1f"
    panel: str = "#f4f6f8"
    border: str = "#d0d4d8"


class BicycleApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.colors = Colors()

        self.lang = "EN"
        self.model = None

        # Keep a reference so Tk doesn't garbage-collect the image
        self._preview_imgtk: Optional[ImageTk.PhotoImage] = None

        self._build_ui()
        self._load_model_or_exit()

        # Allow passing a file path argument: python3 testen.py path/to/image.jpg
        if len(sys.argv) >= 2:
            maybe_path = sys.argv[1]
            if os.path.isfile(maybe_path) and is_image_file(maybe_path):
                self.handle_image(maybe_path)

    def _t(self, key: str) -> str:
        return T[self.lang][key]

    def _build_ui(self):
        self.root.title(self._t("app_title"))
        self.root.geometry("920x620")
        self.root.minsize(920, 620)

        # Top bar
        top = tk.Frame(self.root)
        top.pack(fill="x", padx=14, pady=(12, 6))

        self.title_lbl = tk.Label(top, text=self._t("app_title"), font=("Arial", 20, "bold"))
        self.title_lbl.pack(side="left", anchor="w")

        # Language dropdown (top right)
        lang_frame = tk.Frame(top)
        lang_frame.pack(side="right", anchor="e")

        self.lang_lbl = tk.Label(lang_frame, text=self._t("label_language"), font=("Arial", 11))
        self.lang_lbl.pack(side="left", padx=(0, 6))

        self.lang_var = tk.StringVar(value=self.lang)
        self.lang_menu = ttk.Combobox(lang_frame, textvariable=self.lang_var, values=["EN", "DE"], width=5, state="readonly")
        self.lang_menu.pack(side="left")
        self.lang_menu.bind("<<ComboboxSelected>>", self._on_lang_change)

        # Subtitle
        sub = tk.Frame(self.root)
        sub.pack(fill="x", padx=14, pady=(0, 10))

        subtitle_text = self._t("subtitle_dnd_on") if DND_AVAILABLE else self._t("subtitle_dnd_off")
        self.subtitle_lbl = tk.Label(sub, text=subtitle_text, font=("Arial", 10), fg="#555555")
        self.subtitle_lbl.pack(anchor="w")

        # Main content
        main = tk.Frame(self.root)
        main.pack(fill="both", expand=True, padx=14, pady=10)

        # Left panel: image preview / drop area
        self.left = tk.Frame(main, bd=1, relief="solid", bg=self.colors.panel, highlightbackground=self.colors.border, highlightthickness=1)
        self.left.pack(side="left", fill="both", expand=True, padx=(0, 12))

        self.drop_area = tk.Label(
            self.left,
            text=self._t("drop_placeholder"),
            bg=self.colors.panel,
            fg="#444444",
            font=("Arial", 15, "bold"),
            justify="center"
        )
        self.drop_area.pack(fill="both", expand=True, padx=14, pady=14)

        # Drag & drop binding
        if DND_AVAILABLE and DND_FILES is not None:
            try:
                self.drop_area.drop_target_register(DND_FILES)  # type: ignore
                self.drop_area.dnd_bind("<<Drop>>", self._on_drop)  # type: ignore
            except Exception:
                # If something fails, we still work without drag & drop
                pass

        # Right panel: controls + result + how-it-works
        self.right = tk.Frame(main, width=360)
        self.right.pack(side="right", fill="y")

        # Buttons
        btns = tk.Frame(self.right)
        btns.pack(fill="x", pady=(0, 10))

        self.btn_open = tk.Button(btns, text=self._t("btn_open"), height=2, command=self.open_image)
        self.btn_open.pack(fill="x", pady=(0, 6))

        self.btn_clear = tk.Button(btns, text=self._t("btn_clear"), height=2, command=self.clear)
        self.btn_clear.pack(fill="x", pady=(0, 6))

        self.btn_quit = tk.Button(btns, text=self._t("btn_quit"), height=2, command=self.root.quit)
        self.btn_quit.pack(fill="x")

        # File label
        self.file_lbl = tk.Label(self.right, text=self._t("file_none"), font=("Arial", 10), wraplength=340, justify="left")
        self.file_lbl.pack(fill="x", pady=(12, 8))

        # Result
        self.result_title = tk.Label(self.right, text=self._t("result_title"), font=("Arial", 13, "bold"))
        self.result_title.pack(anchor="w")

        self.result_lbl = tk.Label(self.right, text="—", font=("Arial", 24, "bold"), fg=self.colors.neutral)
        self.result_lbl.pack(fill="x", pady=(6, 12))

        # Probabilities
        self.prob_title = tk.Label(self.right, text=self._t("prob_title"), font=("Arial", 12, "bold"))
        self.prob_title.pack(anchor="w")

        self.prob_lbl = tk.Label(self.right, text=f"{self._t('prob_bike')}: —\n{self._t('prob_not')}: —", font=("Arial", 12), justify="left")
        self.prob_lbl.pack(fill="x", pady=(6, 10))

        # Confidence bar
        self.conf_title = tk.Label(self.right, text=self._t("confidence_title"), font=("Arial", 12, "bold"))
        self.conf_title.pack(anchor="w")

        self.conf_canvas = tk.Canvas(self.right, width=340, height=34, bg="white", highlightthickness=0)
        self.conf_canvas.pack(pady=(6, 12))
        self.conf_canvas.create_rectangle(10, 10, 330, 24, outline="black")
        self._bar = self.conf_canvas.create_rectangle(10, 10, 10, 24, fill=self.colors.ok, outline="")
        self._bar_text = self.conf_canvas.create_text(170, 17, text="0%")

        # How it works (scrollable text)
        how_frame = tk.Frame(self.right)
        how_frame.pack(fill="both", expand=True, pady=(8, 0))

        self.how_title = tk.Label(how_frame, text=self._t("how_title"), font=("Arial", 12, "bold"))
        self.how_title.pack(anchor="w")

        text_frame = tk.Frame(how_frame)
        text_frame.pack(fill="both", expand=True, pady=(6, 0))

        self.how_text = tk.Text(text_frame, wrap="word", height=12, font=("Arial", 10))
        self.how_text.pack(side="left", fill="both", expand=True)

        scroll = tk.Scrollbar(text_frame, command=self.how_text.yview)
        scroll.pack(side="right", fill="y")
        self.how_text.configure(yscrollcommand=scroll.set)

        self.how_text.insert("1.0", how_text(self.lang))
        self.how_text.configure(state="disabled")

    def _load_model_or_exit(self):
        if not os.path.isfile(MODEL_PATH):
            self._show_error(self._t("err_model_missing").format(path=MODEL_PATH))
            self.root.after(100, self.root.destroy)
            return
        try:
            self.model = load_model(MODEL_PATH, compile=False)
        except Exception as e:
            self._show_error(self._t("err_predict").format(msg=str(e)))
            self.root.after(100, self.root.destroy)

    def _show_error(self, msg: str):
        messagebox.showerror(self._t("err_title"), msg)

    def _on_lang_change(self, _event=None):
        new_lang = self.lang_var.get().strip().upper()
        if new_lang not in ("EN", "DE"):
            return
        self.set_language(new_lang)

    def set_language(self, lang: str):
        """Update ALL visible UI text immediately."""
        self.lang = lang
        self.root.title(self._t("app_title"))
        self.title_lbl.config(text=self._t("app_title"))

        subtitle_text = self._t("subtitle_dnd_on") if DND_AVAILABLE else self._t("subtitle_dnd_off")
        self.subtitle_lbl.config(text=subtitle_text)

        self.lang_lbl.config(text=self._t("label_language"))
        self.btn_open.config(text=self._t("btn_open"))
        self.btn_clear.config(text=self._t("btn_clear"))
        self.btn_quit.config(text=self._t("btn_quit"))

        # Keep current file label but update prefix language
        current = self.file_lbl.cget("text")
        if current.startswith("File:") or current.startswith("Datei:"):
            if current.endswith("(none)") or current.endswith("(keine)"):
                self.file_lbl.config(text=self._t("file_none"))
            else:
                # keep path part
                parts = current.split(":", 1)
                path_part = parts[1].strip() if len(parts) == 2 else current
                prefix = "File:" if self.lang == "EN" else "Datei:"
                self.file_lbl.config(text=f"{prefix} {path_part}")
        else:
            self.file_lbl.config(text=self._t("file_none"))

        self.result_title.config(text=self._t("result_title"))
        self.prob_title.config(text=self._t("prob_title"))
        self.conf_title.config(text=self._t("confidence_title"))
        self.how_title.config(text=self._t("how_title"))

        # Update placeholder only if no image is currently displayed
        if self._preview_imgtk is None:
            self.drop_area.config(text=self._t("drop_placeholder"))

        # Update probability labels text if they are currently shown
        prob_text = self.prob_lbl.cget("text")
        if "—" in prob_text:
            self.prob_lbl.config(text=f"{self._t('prob_bike')}: —\n{self._t('prob_not')}: —")
        else:
            # if already predicted, we will re-render based on stored values if possible
            # If not available, we keep the numbers and just swap labels.
            lines = prob_text.splitlines()
            nums = []
            for line in lines:
                if ":" in line:
                    nums.append(line.split(":", 1)[1].strip())
            if len(nums) == 2:
                self.prob_lbl.config(text=f"{self._t('prob_bike')}: {nums[0]}\n{self._t('prob_not')}: {nums[1]}")
            else:
                self.prob_lbl.config(text=f"{self._t('prob_bike')}: —\n{self._t('prob_not')}: —")

        # Update How-it-works text
        self.how_text.configure(state="normal")
        self.how_text.delete("1.0", "end")
        self.how_text.insert("1.0", how_text(self.lang))
        self.how_text.configure(state="disabled")

    def _on_drop(self, event):
        data = (event.data or "").strip()
        if not data:
            return
        # Handle {path with spaces} or multiple files
        if data.startswith("{") and data.endswith("}"):
            data = data[1:-1]
        path = data.split()[0]
        if os.path.isfile(path):
            self.handle_image(path)

    def open_image(self):
        if self.lang == "EN":
            title = "Choose an image"
        else:
            title = "Bild auswählen"
        path = filedialog.askopenfilename(
            title=title,
            filetypes=[("Images", "*.jpg *.jpeg *.png"), ("All files", "*.*")]
        )
        if path:
            self.handle_image(path)

    def clear(self):
        self._preview_imgtk = None
        self.drop_area.config(image="", text=self._t("drop_placeholder"))
        self.file_lbl.config(text=self._t("file_none"))
        self.result_lbl.config(text="—", fg=self.colors.neutral)
        self.prob_lbl.config(text=f"{self._t('prob_bike')}: —\n{self._t('prob_not')}: —")

        self.conf_canvas.coords(self._bar, 10, 10, 10, 24)
        self.conf_canvas.itemconfig(self._bar_text, text="0%")
        self.conf_canvas.itemconfig(self._bar, fill=self.colors.ok)

    def handle_image(self, path: str):
        if not is_image_file(path):
            self._show_error(self._t("err_not_image"))
            return

        # Update file label (language-specific prefix)
        prefix = "File:" if self.lang == "EN" else "Datei:"
        self.file_lbl.config(text=f"{prefix} {shorten_path(path)}")

        # Load preview
        try:
            pil = Image.open(path).convert("RGB")
            preview = pil.copy()
            preview.thumbnail(PREVIEW_MAX)
            self._preview_imgtk = ImageTk.PhotoImage(preview)
            self.drop_area.config(image=self._preview_imgtk, text="")
        except Exception as e:
            self._show_error(self._t("err_open_image").format(msg=str(e)))
            return

        # Predict
        try:
            if self.model is None:
                raise RuntimeError("Model is not loaded.")
            label_key, conf, p_bike, p_not = predict_image(self.model, path)
        except Exception as e:
            self._show_error(self._t("err_predict").format(msg=str(e)))
            return

        # Result text in selected language
        if self.lang == "EN":
            result_text = "BICYCLE" if label_key == "BICYCLE" else "NOT BICYCLE"
        else:
            result_text = "FAHRRAD" if label_key == "BICYCLE" else "KEIN FAHRRAD"

        self.result_lbl.config(
            text=result_text,
            fg=(self.colors.ok if label_key == "BICYCLE" else self.colors.bad)
        )

        self.prob_lbl.config(
            text=f"{self._t('prob_bike')}: {p_bike:.4f}\n{self._t('prob_not')}: {p_not:.4f}"
        )

        # Confidence bar
        conf_pct = int(round(conf * 100))
        x0 = 10
        x1 = 10 + int(320 * max(0.0, min(1.0, conf)))
        self.conf_canvas.coords(self._bar, x0, 10, x1, 24)
        self.conf_canvas.itemconfig(self._bar_text, text=f"{conf_pct}%")
        self.conf_canvas.itemconfig(self._bar, fill=(self.colors.ok if label_key == "BICYCLE" else self.colors.bad))


def main():
    root = TkRoot()
    app = BicycleApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
