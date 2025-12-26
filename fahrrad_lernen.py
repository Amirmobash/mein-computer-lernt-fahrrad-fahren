import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from dataclasses import dataclass
from typing import Dict, Tuple, Optional, List

import numpy as np
from PIL import Image, ImageTk

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# ============================================================
# testen.py  (DO NOT rename)
# Kid-friendly Bicycle Detector (EN/DE) for Raspberry Pi OS
# Loads: mein_fahrrad_modell.h5 (same folder)
#
# Required packages:
#   pip install tensorflow pillow numpy scipy
# Optional (drag & drop):
#   pip install tkinterdnd2
# ============================================================

MODEL_PATH = "mein_fahrrad_modell.h5"
IMG_SIZE = (150, 150)          # must match training
PREVIEW_MAX = (520, 340)       # image preview size in the window
PATH_MAX_LEN = 62              # shorten long file paths in UI

# If dataset folders exist, we will auto-detect the true class mapping:
#   daten/train/bicycle
#   daten/train/not_bicycle
TRAIN_DIR = "daten/train"

# Optional Drag & Drop
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
# Bilingual text (EN / DE)
# ---------------------------
def _how_it_works_text_en() -> str:
    return (
        "HOW IT WORKS (Kid-friendly)\n"
        "\n"
        "• What is the model?\n"
        "  A model is like a tiny 'brain file'. It learned from many pictures.\n"
        "  Our model file is: mein_fahrrad_modell.h5\n"
        "\n"
        "• What does training mean?\n"
        "  Training is practice. The computer sees bicycle pictures and\n"
        "  not-bicycle pictures and learns patterns (edges, circles, shapes).\n"
        "\n"
        "• What happens when you test one image?\n"
        "  1) The picture becomes smaller (150×150 pixels).\n"
        "  2) The model looks at the pixels.\n"
        "  3) The model returns probabilities.\n"
        "\n"
        "• What is probability?\n"
        "  A probability is a confidence number from 0.0000 to 1.0000.\n"
        "  Example: Bicycle 0.9000 means: 'I feel very sure it is a bicycle'.\n"
        "\n"
        "• Why can it be wrong sometimes?\n"
        "  - Too few training images.\n"
        "  - Images are blurry or very different.\n"
        "  - A not-bicycle image has circle shapes like wheels.\n"
        "\n"
        "TIP: More and more varied training images usually makes it better!"
    )


def _how_it_works_text_de() -> str:
    return (
        "WIE FUNKTIONIERT DAS? (Kinderleicht)\n"
        "\n"
        "• Was ist das Modell?\n"
        "  Ein Modell ist wie eine kleine 'Gehirn-Datei'. Es hat aus vielen\n"
        "  Bildern gelernt. Unsere Datei heißt: mein_fahrrad_modell.h5\n"
        "\n"
        "• Was bedeutet Training?\n"
        "  Training ist Üben. Der Computer sieht Fahrrad-Bilder und\n"
        "  Nicht-Fahrrad-Bilder und lernt Muster (Kanten, Kreise, Formen).\n"
        "\n"
        "• Was passiert beim Testen eines Bildes?\n"
        "  1) Das Bild wird kleiner (150×150 Pixel).\n"
        "  2) Das Modell schaut auf die Pixel.\n"
        "  3) Das Modell gibt Wahrscheinlichkeiten zurück.\n"
        "\n"
        "• Was ist Wahrscheinlichkeit?\n"
        "  Das ist eine Sicherheits-Zahl von 0.0000 bis 1.0000.\n"
        "  Beispiel: Fahrrad 0.9000 heißt: 'Ich bin sehr sicher: Fahrrad'.\n"
        "\n"
        "• Warum kann es manchmal falsch liegen?\n"
        "  - Zu wenige Trainingsbilder.\n"
        "  - Bilder sind unscharf oder sehr unterschiedlich.\n"
        "  - Ein Nicht-Fahrrad-Bild hat Kreise wie Räder.\n"
        "\n"
        "TIPP: Mehr und vielfältigere Trainingsbilder machen es oft besser!"
    )


def how_text(lang: str) -> str:
    return _how_it_works_text_en() if lang == "EN" else _how_it_works_text_de()


T: Dict[str, Dict[str, str]] = {
    "EN": {
        "app_title": "Bicycle Detector (Raspberry Pi)",
        "subtitle_on": "Drop a JPG/PNG image or click 'Open Image'  •  Drag & Drop: ON",
        "subtitle_off": "Drop a JPG/PNG image or click 'Open Image'  •  Drag & Drop: install: pip install tkinterdnd2",
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
        "status_ready": "Ready. Choose an image.",
        "status_pred": "Prediction done.",
        "status_loading": "Loading model...",
        "status_error": "Something went wrong.",
        "err_title": "Error",
        "err_model_missing": "Model file not found:\n{path}\n\nTrain first:\npython3 fahrrad_lernen.py",
        "err_not_image": "Please choose a JPG or PNG image.",
        "err_open_image": "Could not open the image:\n{msg}",
        "err_predict": "Prediction failed:\n{msg}",
        "hint_mapping": "Class mapping: {mapping}",
    },
    "DE": {
        "app_title": "Fahrrad-Erkenner (Raspberry Pi)",
        "subtitle_on": "Ziehe ein JPG/PNG Bild rein oder klicke 'Bild öffnen'  •  Drag & Drop: AN",
        "subtitle_off": "Ziehe ein JPG/PNG Bild rein oder klicke 'Bild öffnen'  •  Drag & Drop: installieren: pip install tkinterdnd2",
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
        "status_ready": "Bereit. Bild auswählen.",
        "status_pred": "Vorhersage fertig.",
        "status_loading": "Modell wird geladen...",
        "status_error": "Etwas ist schiefgelaufen.",
        "err_title": "Fehler",
        "err_model_missing": "Modelldatei nicht gefunden:\n{path}\n\nBitte zuerst trainieren:\npython3 fahrrad_lernen.py",
        "err_not_image": "Bitte ein JPG oder PNG Bild auswählen.",
        "err_open_image": "Bild konnte nicht geöffnet werden:\n{msg}",
        "err_predict": "Vorhersage fehlgeschlagen:\n{msg}",
        "hint_mapping": "Klassen-Zuordnung: {mapping}",
    },
}


# ---------------------------
# Helper functions (required)
# ---------------------------
def shorten_path(path: str, max_len: int = PATH_MAX_LEN) -> str:
    if not path:
        return path
    if len(path) <= max_len:
        return path
    keep = max_len - 5
    front = keep // 2
    back = keep - front
    return path[:front] + " ... " + path[-back:]


def is_image_file(path: str) -> bool:
    return path.lower().endswith((".jpg", ".jpeg", ".png"))


def _safe_parse_drop_data(data: str) -> List[str]:
    """
    Convert drop text into a list of file paths.
    Handles:
      - {path with spaces}
      - multiple paths separated by spaces
    """
    if not data:
        return []
    s = data.strip()

    # Many DnD systems wrap paths with spaces like: { /path/with space/file.png }
    paths: List[str] = []
    buf = ""
    in_brace = False
    for ch in s:
        if ch == "{":
            in_brace = True
            buf = ""
        elif ch == "}":
            in_brace = False
            if buf.strip():
                paths.append(buf.strip())
            buf = ""
        elif ch == " " and not in_brace:
            if buf.strip():
                paths.append(buf.strip())
            buf = ""
        else:
            buf += ch
    if buf.strip():
        paths.append(buf.strip())

    # Deduplicate while preserving order
    seen = set()
    out = []
    for p in paths:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def _try_detect_class_mapping() -> Optional[Dict[str, int]]:
    """
    If TRAIN_DIR exists, detect class_indices using flow_from_directory.
    This prevents the common mistake of interpreting sigmoid output the wrong way.
    Returns dict like: {'bicycle': 0, 'not_bicycle': 1}
    """
    try:
        if not os.path.isdir(TRAIN_DIR):
            return None
        # Only detect if there are subfolders
        sub = [d for d in os.listdir(TRAIN_DIR) if os.path.isdir(os.path.join(TRAIN_DIR, d))]
        if len(sub) < 2:
            return None

        gen = ImageDataGenerator(rescale=1.0 / 255.0).flow_from_directory(
            TRAIN_DIR,
            target_size=IMG_SIZE,
            batch_size=1,
            class_mode="binary",
            shuffle=False
        )
        # Avoid keeping an open generator around
        mapping = dict(gen.class_indices)
        return mapping
    except Exception:
        return None


def predict_image(model, path: str, class_indices: Optional[Dict[str, int]] = None) -> Tuple[str, float, float, float]:
    """
    Predict one image.

    Returns:
      label_key: "BICYCLE" or "NOT_BICYCLE"
      conf: confidence of winning label (0..1)
      p_bike: probability of bicycle (0..1)
      p_not: probability of not_bicycle (0..1)

    Default assumption: bicycle=0, not_bicycle=1, and sigmoid output = prob(class 1).
    If class_indices is available, we will map correctly using it.
    """
    img = keras_image.load_img(path, target_size=IMG_SIZE)
    arr = keras_image.img_to_array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)

    pred = float(model.predict(arr, verbose=0)[0][0])  # probability of class "1"

    # Default meaning:
    p_class1 = pred
    p_class0 = 1.0 - pred

    # If mapping exists, we interpret which folder is class 0 and class 1
    # and compute p_bike/p_not accordingly.
    if class_indices and isinstance(class_indices, dict):
        rev = {v: k for k, v in class_indices.items()}
        name0 = rev.get(0, "class0").lower()
        name1 = rev.get(1, "class1").lower()

        # Determine which one is bicycle/not_bicycle
        # We accept several common variations
        def _is_bike(n: str) -> bool:
            return "bicycle" in n or "bike" in n or "fahrrad" in n

        def _is_not_bike(n: str) -> bool:
            return "not_bicycle" in n or "notbike" in n or "no_bike" in n or "kein" in n or "not" in n

        # Try mapping by names
        if _is_bike(name0) and (_is_not_bike(name1) or not _is_bike(name1)):
            p_bike, p_not = p_class0, p_class1
        elif _is_bike(name1) and (_is_not_bike(name0) or not _is_bike(name0)):
            p_bike, p_not = p_class1, p_class0
        else:
            # Fallback: assume your training structure bicycle=0 not_bicycle=1
            p_bike, p_not = p_class0, p_class1
    else:
        p_bike, p_not = p_class0, p_class1

    if p_bike >= p_not:
        return "BICYCLE", p_bike, p_bike, p_not
    return "NOT_BICYCLE", p_not, p_bike, p_not


@dataclass
class Colors:
    ok: str = "#1f8f3a"
    bad: str = "#cc1f1f"
    neutral: str = "#222222"
    panel: str = "#f4f6f8"
    border: str = "#d0d4d8"
    soft: str = "#666666"


class BicycleApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.colors = Colors()
        self.lang = "EN"

        self.model = None
        self.class_indices: Optional[Dict[str, int]] = None

        self._preview_imgtk: Optional[ImageTk.PhotoImage] = None
        self._last_probs: Optional[Tuple[float, float]] = None  # (p_bike, p_not)
        self._last_result_key: Optional[str] = None             # "BICYCLE" / "NOT_BICYCLE"

        self._build_ui()
        self._load_model_or_exit()

        # Optional: detect mapping from dataset folders (prevents wrong interpretation)
        self.class_indices = _try_detect_class_mapping()
        self._update_mapping_hint()

        # Accept optional image path argument
        if len(sys.argv) >= 2:
            maybe_path = sys.argv[1]
            if os.path.isfile(maybe_path) and is_image_file(maybe_path):
                self.handle_image(maybe_path)

        # Small keyboard shortcuts (kid-friendly)
        self.root.bind("<Control-o>", lambda e: self.open_image())
        self.root.bind("<Escape>", lambda e: self.clear())

    def _t(self, key: str) -> str:
        return T[self.lang][key]

    def _build_ui(self):
        self.root.title(self._t("app_title"))
        self.root.geometry("940x650")
        self.root.minsize(940, 650)

        top = tk.Frame(self.root)
        top.pack(fill="x", padx=14, pady=(12, 6))

        self.title_lbl = tk.Label(top, text=self._t("app_title"), font=("Arial", 20, "bold"))
        self.title_lbl.pack(side="left", anchor="w")

        lang_frame = tk.Frame(top)
        lang_frame.pack(side="right", anchor="e")

        self.lang_lbl = tk.Label(lang_frame, text=self._t("label_language"), font=("Arial", 11))
        self.lang_lbl.pack(side="left", padx=(0, 6))

        self.lang_var = tk.StringVar(value=self.lang)
        self.lang_menu = ttk.Combobox(lang_frame, textvariable=self.lang_var, values=["EN", "DE"], width=5, state="readonly")
        self.lang_menu.pack(side="left")
        self.lang_menu.bind("<<ComboboxSelected>>", self._on_lang_change)

        sub = tk.Frame(self.root)
        sub.pack(fill="x", padx=14, pady=(0, 6))

        subtitle_text = self._t("subtitle_on") if DND_AVAILABLE else self._t("subtitle_off")
        self.subtitle_lbl = tk.Label(sub, text=subtitle_text, font=("Arial", 10), fg=self.colors.soft)
        self.subtitle_lbl.pack(anchor="w")

        # Mapping hint line (small, helpful)
        self.mapping_lbl = tk.Label(sub, text="", font=("Arial", 9), fg=self.colors.soft)
        self.mapping_lbl.pack(anchor="w", pady=(3, 0))

        main = tk.Frame(self.root)
        main.pack(fill="both", expand=True, padx=14, pady=10)

        # Left: preview
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

        if DND_AVAILABLE and DND_FILES is not None:
            try:
                self.drop_area.drop_target_register(DND_FILES)  # type: ignore
                self.drop_area.dnd_bind("<<Drop>>", self._on_drop)  # type: ignore
            except Exception:
                pass

        # Right: controls + results + explanation
        self.right = tk.Frame(main, width=370)
        self.right.pack(side="right", fill="y")

        btns = tk.Frame(self.right)
        btns.pack(fill="x", pady=(0, 10))

        self.btn_open = tk.Button(btns, text=self._t("btn_open"), height=2, command=self.open_image)
        self.btn_open.pack(fill="x", pady=(0, 6))

        self.btn_clear = tk.Button(btns, text=self._t("btn_clear"), height=2, command=self.clear)
        self.btn_clear.pack(fill="x", pady=(0, 6))

        self.btn_quit = tk.Button(btns, text=self._t("btn_quit"), height=2, command=self.root.quit)
        self.btn_quit.pack(fill="x")

        self.file_lbl = tk.Label(self.right, text=self._t("file_none"), font=("Arial", 10), wraplength=350, justify="left")
        self.file_lbl.pack(fill="x", pady=(12, 8))

        self.result_title = tk.Label(self.right, text=self._t("result_title"), font=("Arial", 13, "bold"))
        self.result_title.pack(anchor="w")

        self.result_lbl = tk.Label(self.right, text="—", font=("Arial", 24, "bold"), fg=self.colors.neutral)
        self.result_lbl.pack(fill="x", pady=(6, 10))

        self.prob_title = tk.Label(self.right, text=self._t("prob_title"), font=("Arial", 12, "bold"))
        self.prob_title.pack(anchor="w")

        self.prob_lbl = tk.Label(self.right, text=f"{self._t('prob_bike')}: —\n{self._t('prob_not')}: —", font=("Arial", 12), justify="left")
        self.prob_lbl.pack(fill="x", pady=(6, 10))

        self.conf_title = tk.Label(self.right, text=self._t("confidence_title"), font=("Arial", 12, "bold"))
        self.conf_title.pack(anchor="w")

        self.conf_canvas = tk.Canvas(self.right, width=350, height=34, bg="white", highlightthickness=0)
        self.conf_canvas.pack(pady=(6, 10))
        self.conf_canvas.create_rectangle(10, 10, 340, 24, outline="black")
        self._bar = self.conf_canvas.create_rectangle(10, 10, 10, 24, fill=self.colors.ok, outline="")
        self._bar_text = self.conf_canvas.create_text(175, 17, text="0%")

        # How-it-works (scrollable)
        how_frame = tk.Frame(self.right)
        how_frame.pack(fill="both", expand=True, pady=(10, 0))

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

        # Status bar
        status = tk.Frame(self.root)
        status.pack(fill="x", padx=14, pady=(0, 10))
        self.status_var = tk.StringVar(value=self._t("status_ready"))
        self.status_lbl = tk.Label(status, textvariable=self.status_var, font=("Arial", 10), fg=self.colors.soft, anchor="w")
        self.status_lbl.pack(fill="x")

    def _set_status(self, key: str):
        self.status_var.set(self._t(key))

    def _update_mapping_hint(self):
        if self.class_indices:
            self.mapping_lbl.config(text=self._t("hint_mapping").format(mapping=str(self.class_indices)))
        else:
            # Keep a gentle hint, not scary
            self.mapping_lbl.config(text=self._t("hint_mapping").format(mapping="(auto-detect off)"))

    def _load_model_or_exit(self):
        self._set_status("status_loading")
        self.root.update_idletasks()

        if not os.path.isfile(MODEL_PATH):
            messagebox.showerror(self._t("err_title"), self._t("err_model_missing").format(path=MODEL_PATH))
            self.root.after(100, self.root.destroy)
            return

        try:
            self.model = load_model(MODEL_PATH, compile=False)
        except Exception as e:
            messagebox.showerror(self._t("err_title"), self._t("err_predict").format(msg=str(e)))
            self.root.after(100, self.root.destroy)
            return

        self._set_status("status_ready")

    def _on_lang_change(self, _event=None):
        new_lang = self.lang_var.get().strip().upper()
        if new_lang in ("EN", "DE"):
            self.set_language(new_lang)

    def set_language(self, lang: str):
        self.lang = lang

        self.root.title(self._t("app_title"))
        self.title_lbl.config(text=self._t("app_title"))

        subtitle_text = self._t("subtitle_on") if DND_AVAILABLE else self._t("subtitle_off")
        self.subtitle_lbl.config(text=subtitle_text)
        self.lang_lbl.config(text=self._t("label_language"))

        self.btn_open.config(text=self._t("btn_open"))
        self.btn_clear.config(text=self._t("btn_clear"))
        self.btn_quit.config(text=self._t("btn_quit"))

        self.result_title.config(text=self._t("result_title"))
        self.prob_title.config(text=self._t("prob_title"))
        self.conf_title.config(text=self._t("confidence_title"))
        self.how_title.config(text=self._t("how_title"))

        # Update status text
        # If prediction already done, keep "Prediction done." equivalent, else ready
        if self._last_result_key is None:
            self._set_status("status_ready")
        else:
            self._set_status("status_pred")

        # Update mapping hint text (language changes)
        self._update_mapping_hint()

        # Update file label prefix
        current = self.file_lbl.cget("text")
        if current.startswith("File:") or current.startswith("Datei:"):
            if "(none)" in current or "(keine)" in current:
                self.file_lbl.config(text=self._t("file_none"))
            else:
                # keep only the path part after ":"
                parts = current.split(":", 1)
                path_part = parts[1].strip() if len(parts) == 2 else current
                prefix = "File:" if self.lang == "EN" else "Datei:"
                self.file_lbl.config(text=f"{prefix} {path_part}")
        else:
            self.file_lbl.config(text=self._t("file_none"))

        # Update placeholder text if no image is shown
        if self._preview_imgtk is None:
            self.drop_area.config(text=self._t("drop_placeholder"))

        # Update probabilities display labels while keeping numbers
        if self._last_probs is None:
            self.prob_lbl.config(text=f"{self._t('prob_bike')}: —\n{self._t('prob_not')}: —")
        else:
            p_bike, p_not = self._last_probs
            self.prob_lbl.config(text=f"{self._t('prob_bike')}: {p_bike:.4f}\n{self._t('prob_not')}: {p_not:.4f}")

        # Update how-it-works text
        self.how_text.configure(state="normal")
        self.how_text.delete("1.0", "end")
        self.how_text.insert("1.0", how_text(self.lang))
        self.how_text.configure(state="disabled")

        # Update current result label language (if any)
        if self._last_result_key is None:
            self.result_lbl.config(text="—", fg=self.colors.neutral)
        else:
            self._render_result_label(self._last_result_key)

    def _render_result_label(self, label_key: str):
        if self.lang == "EN":
            text = "BICYCLE" if label_key == "BICYCLE" else "NOT BICYCLE"
        else:
            text = "FAHRRAD" if label_key == "BICYCLE" else "KEIN FAHRRAD"

        self.result_lbl.config(
            text=text,
            fg=(self.colors.ok if label_key == "BICYCLE" else self.colors.bad)
        )

    def _on_drop(self, event):
        data = (event.data or "").strip()
        paths = _safe_parse_drop_data(data)
        if not paths:
            return
        # Take the first valid image file
        for p in paths:
            if os.path.isfile(p) and is_image_file(p):
                self.handle_image(p)
                return
        # If none is valid
        messagebox.showerror(self._t("err_title"), self._t("err_not_image"))

    def open_image(self):
        title = "Choose an image" if self.lang == "EN" else "Bild auswählen"
        path = filedialog.askopenfilename(
            title=title,
            filetypes=[("Images", "*.jpg *.jpeg *.png"), ("All files", "*.*")]
        )
        if path:
            self.handle_image(path)

    def clear(self):
        self._preview_imgtk = None
        self._last_probs = None
        self._last_result_key = None

        self.drop_area.config(image="", text=self._t("drop_placeholder"))
        self.file_lbl.config(text=self._t("file_none"))
        self.result_lbl.config(text="—", fg=self.colors.neutral)
        self.prob_lbl.config(text=f"{self._t('prob_bike')}: —\n{self._t('prob_not')}: —")

        self.conf_canvas.coords(self._bar, 10, 10, 10, 24)
        self.conf_canvas.itemconfig(self._bar_text, text="0%")
        self.conf_canvas.itemconfig(self._bar, fill=self.colors.ok)

        self._set_status("status_ready")

    def handle_image(self, path: str):
        if not is_image_file(path):
            messagebox.showerror(self._t("err_title"), self._t("err_not_image"))
            return

        # Update file label
        prefix = "File:" if self.lang == "EN" else "Datei:"
        self.file_lbl.config(text=f"{prefix} {shorten_path(path)}")

        # Load preview (robust)
        try:
            pil = Image.open(path).convert("RGB")
            preview = pil.copy()
            preview.thumbnail(PREVIEW_MAX)
            self._preview_imgtk = ImageTk.PhotoImage(preview)
            self.drop_area.config(image=self._preview_imgtk, text="")
        except Exception as e:
            messagebox.showerror(self._t("err_title"), self._t("err_open_image").format(msg=str(e)))
            self._set_status("status_error")
            return

        # Predict
        try:
            if self.model is None:
                raise RuntimeError("Model is not loaded.")
            label_key, conf, p_bike, p_not = predict_image(self.model, path, self.class_indices)
        except Exception as e:
            messagebox.showerror(self._t("err_title"), self._t("err_predict").format(msg=str(e)))
            self._set_status("status_error")
            return

        # Store last state (so language switching keeps numbers)
        self._last_probs = (p_bike, p_not)
        self._last_result_key = label_key

        # Render results
        self._render_result_label(label_key)
        self.prob_lbl.config(text=f"{self._t('prob_bike')}: {p_bike:.4f}\n{self._t('prob_not')}: {p_not:.4f}")

        # Confidence bar
        conf = float(max(0.0, min(1.0, conf)))
        conf_pct = int(round(conf * 100))
        x0 = 10
        x1 = 10 + int(330 * conf)  # bar width range
        self.conf_canvas.coords(self._bar, x0, 10, x1, 24)
        self.conf_canvas.itemconfig(self._bar_text, text=f"{conf_pct}%")
        self.conf_canvas.itemconfig(self._bar, fill=(self.colors.ok if label_key == "BICYCLE" else self.colors.bad))

        self._set_status("status_pred")


def main():
    root = TkRoot()
    app = BicycleApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
