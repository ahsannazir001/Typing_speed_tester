#!/usr/bin/env python3
"""
Advanced Typing Speed & Accuracy Tester
A modern desktop GUI application built with Python and Tkinter.

Features:
  - Modern dark/light themed UI with sleek cards and custom fonts.
  - Split sections: Reference Text, Live Input, Live Stats Bar, Analytics Dashboard.
  - Real-time character highlighting (green = correct, red = incorrect).
  - Live WPM and countdown timer.
  - Difficulty modes: Easy, Medium, Hard.
  - Test duration selector: 30s, 60s, 120s.
  - Detailed analytics: Raw WPM, Net WPM, Accuracy, Key Hits, Backspaces.
  - Structured Error Analysis Table (expected vs typed words).
  - Local history/leaderboard saved to history.json with a viewer popup.

Run:  python typing_tester.py
"""

import base64
import json
import os
import random
import sys
import time
import datetime as dt
import tkinter as tk
from tkinter import ttk, messagebox


def resource_path(relative):
    """Resolve a resource path whether running as script or frozen exe."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative)
_ICON_B64 = "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"



# ---------------------------------------------------------------------------
# Theme definitions
# ---------------------------------------------------------------------------
class Theme:
    DARK = {
        "name": "dark",
        "bg": "#0f1115",
        "card": "#171a21",
        "card_alt": "#1f2430",
        "fg": "#e8ecf1",
        "muted": "#8b93a7",
        "accent": "#4f9cf9",
        "accent_2": "#7c5cff",
        "correct_bg": "#1f3d28",
        "correct_fg": "#7ee787",
        "wrong_bg": "#4a1f24",
        "wrong_fg": "#ff7b72",
        "pending_bg": "#222632",
        "pending_fg": "#5b6478",
        "border": "#2a3040",
        "header": "#11141b",
        "shadow": "#000000",
        "good": "#3fb950",
        "bad": "#f85149",
        "warn": "#d29922",
    }

    LIGHT = {
        "name": "light",
        "bg": "#f4f6fb",
        "card": "#ffffff",
        "card_alt": "#f0f3f9",
        "fg": "#1c2330",
        "muted": "#6b7488",
        "accent": "#2f6fed",
        "accent_2": "#6d4aff",
        "correct_bg": "#d7f5e1",
        "correct_fg": "#1a7f37",
        "wrong_bg": "#ffe0e0",
        "wrong_fg": "#cf222e",
        "pending_bg": "#eef1f6",
        "pending_fg": "#9aa3b2",
        "border": "#dde2ec",
        "header": "#ffffff",
        "shadow": "#c9cedb",
        "good": "#1a7f37",
        "bad": "#cf222e",
        "warn": "#9a6700",
    }

    @classmethod
    def get(cls, name):
        return cls.DARK if name == "dark" else cls.LIGHT


# ---------------------------------------------------------------------------
# Text bank for difficulty levels
# ---------------------------------------------------------------------------
class TextBank:
    EASY = [
        "the quick brown fox jumps over the lazy dog near the river bank every morning",
        "a small child found a shiny coin on the sidewalk and smiled at the bright sunny day",
        "she bought fresh bread and warm milk from the corner store before going back home",
        "the old cat slept quietly on the soft mat while the rain tapped gently on the window",
        "we walked slowly through the green park and watched the children play on the swings",
        "he always drinks a cup of hot tea and reads the morning paper before starting work",
        "the little boat floated calmly on the blue lake under a clear and peaceful sky",
        "my friend loves to bake sweet cookies and share them with everyone in the office",
    ]

    MEDIUM = [
        "Despite the heavy rain, the determined hiker continued up the muddy trail, pausing only to adjust his backpack and check the worn map he'd carried for three days straight.",
        "The library, built in 1892, still stands at the center of town; its tall windows, dusty shelves, and creaking floors remind every visitor of a slower, quieter era.",
        "In order to succeed, one must plan carefully, execute patiently, and review results honestly; shortcuts often lead to setbacks, while steady effort compounds over time.",
        "She opened the letter, read it twice, folded it neatly, and placed it inside the wooden box where she kept every message that ever truly mattered to her.",
        "The chef tasted the sauce, added a pinch of salt, stirred the pot slowly, and nodded; the dish was finally ready to be served to the waiting guests.",
    ]

    HARD = [
        "def quick_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr)//2]\n    left = [x for x in arr if x < pivot]\n    mid = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quick_sort(left) + mid + quick_sort(right)",
        "const fetchData = async (url) => {\n  try {\n    const res = await fetch(url, { method: 'GET', headers: { 'Accept': 'application/json' } });\n    if (!res.ok) throw new Error(`HTTP ${res.status}`);\n    return await res.json();\n  } catch (err) {\n    console.error('fetch failed:', err.message);\n    return null;\n  }\n};",
        "SELECT o.id, c.name, SUM(oi.qty * oi.price) AS total FROM orders o JOIN customers c ON o.cust_id = c.id JOIN order_items oi ON o.id = oi.order_id WHERE o.placed_at >= '2024-01-01' GROUP BY o.id, c.name HAVING total > 500.00 ORDER BY total DESC LIMIT 25;",
        "public class Cache<T> {\n    private final Map<String, T> store = new ConcurrentHashMap<>();\n    public T get(String key, Supplier<T> loader) {\n        return store.computeIfAbsent(key, k -> loader.get());\n    }\n    public void evict(String key) { store.remove(key); }\n}",
        "curl -X POST https://api.example.com/v2/users -H 'Content-Type: application/json' -H 'Authorization: Bearer $TOKEN' -d '{\"email\":\"a@b.co\",\"roles\":[\"admin\",\"editor\"],\"meta\":{\"plan\":\"pro\",\"price\":49.99}}' --max-time 30 -v",
    ]

    @classmethod
    def get_text(cls, difficulty):
        if difficulty == "Easy":
            return random.choice(cls.EASY)
        elif difficulty == "Medium":
            return random.choice(cls.MEDIUM)
        else:
            return random.choice(cls.HARD)


# ---------------------------------------------------------------------------
# History / Leaderboard persistence
# ---------------------------------------------------------------------------
class HistoryManager:
    def __init__(self, path=None):
        if path is None:
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "history.json")
        self.path = path
        self.records = self._load()

    def _load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            pass
        return []

    def add(self, record):
        self.records.append(record)
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.records, f, indent=2, ensure_ascii=False)
        except OSError:
            pass

    def clear(self):
        self.records = []
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.records, f)
        except OSError:
            pass

    def top_scores(self, n=10):
        return sorted(self.records, key=lambda r: r.get("net_wpm", 0), reverse=True)[:n]

    def recent(self, n=15):
        return list(reversed(self.records[-n:]))


# ---------------------------------------------------------------------------
# Main Application
# ---------------------------------------------------------------------------
class TypingTestApp:
    DURATIONS = [("30 seconds", 30), ("60 seconds", 60), ("120 seconds", 120)]
    DIFFICULTIES = ["Easy", "Medium", "Hard"]

    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed & Accuracy Tester")
        self.root.geometry("1080x760")
        self.root.minsize(960, 680)

        try:
            import tempfile as _tf
            _ico_path = os.path.join(_tf.gettempdir(), "_typing_tester_icon.ico")
            with open(_ico_path, "wb") as _f:
                _f.write(base64.b64decode(_ICON_B64))
            self.root.iconbitmap(_ico_path)
            self.root.wm_iconbitmap(_ico_path)
        except Exception:
            pass

        self.theme_name = "dark"
        self.theme = Theme.get(self.theme_name)
        self.history = HistoryManager()

        # Test state
        self.reference_text = ""
        self.duration = 60
        self.difficulty = "Easy"
        self.test_active = False
        self.test_finished = False
        self.start_time = 0.0
        self.time_left = 60
        self.key_hits = 0
        self.backspaces = 0
        self._timer_id = None

        # Custom fonts
        self.f_title = ("Segoe UI", 22, "bold")
        self.f_h = ("Segoe UI", 14, "bold")
        self.f_body = ("Segoe UI", 12)

        self.f_mono = ("Consolas", 15)
        self.f_small = ("Segoe UI", 10)
        self.f_stat = ("Segoe UI Semibold", 26, "bold")
        self.f_stat_label = ("Segoe UI", 10, "bold")

        self._build_ui()
        self._apply_theme()
        self._new_test(load=True)

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        self.root.configure(bg=self.theme["bg"])

        # Header bar
        self.header = tk.Frame(self.root)
        self.header.pack(side="top", fill="x")

        self.title_lbl = tk.Label(self.header, text="⚡ Typing Speed & Accuracy Tester",
                                  font=self.f_title, padx=20, pady=14)
        self.title_lbl.pack(side="left")

        self.theme_btn = tk.Button(self.header, text="🌙 Dark", font=self.f_body,
                                   relief="flat", padx=14, pady=6, cursor="hand2",
                                   command=self._toggle_theme)
        self.theme_btn.pack(side="right", padx=18, pady=14)

        self.history_btn = tk.Button(self.header, text="🏆 History / Leaderboard",
                                     font=self.f_body, relief="flat", padx=14, pady=6,
                                     cursor="hand2", command=self._open_history)
        self.history_btn.pack(side="right", padx=6, pady=14)

        # Control bar
        self.ctrl = tk.Frame(self.root)
        self.ctrl.pack(side="top", fill="x", padx=20, pady=(0, 8))

        self._build_controls()

        # Main content
        self.content = tk.Frame(self.root)
        self.content.pack(side="top", fill="both", expand=True, padx=20, pady=(0, 16))

        # Live stats bar
        self.stats_bar = tk.Frame(self.content)
        self.stats_bar.pack(side="top", fill="x", pady=(0, 12))
        self._build_stats_bar()

        # Reference text card
        self.ref_card = tk.Frame(self.content)
        self.ref_card.pack(side="top", fill="x", pady=(0, 12))
        self._build_reference_card()

        # Input card
        self.input_card = tk.Frame(self.content)
        self.input_card.pack(side="top", fill="x", pady=(0, 12))
        self._build_input_card()

        # Analytics dashboard
        self.dash_card = tk.Frame(self.content)
        self.dash_card.pack(side="top", fill="both", expand=True)
        self._build_dashboard()

    def _build_controls(self):
        tk.Label(self.ctrl, text="Duration:", font=self.f_body).pack(side="left", padx=(4, 6))

        self.duration_var = tk.StringVar(value="60 seconds")
        self.duration_box = ttk.Combobox(self.ctrl, textvariable=self.duration_var,
                                         values=[d[0] for d in self.DURATIONS],
                                         state="readonly", width=14, font=self.f_body)
        self.duration_box.pack(side="left", padx=(0, 18))
        self.duration_box.bind("<<ComboboxSelected>>", self._on_settings_change)

        tk.Label(self.ctrl, text="Difficulty:", font=self.f_body).pack(side="left", padx=(4, 6))

        self.diff_var = tk.StringVar(value="Easy")
        self.diff_box = ttk.Combobox(self.ctrl, textvariable=self.diff_var,
                                     values=self.DIFFICULTIES, state="readonly",
                                     width=12, font=self.f_body)
        self.diff_box.pack(side="left", padx=(0, 18))
        self.diff_box.bind("<<ComboboxSelected>>", self._on_settings_change)

        self.start_btn = tk.Button(self.ctrl, text="▶  Start", font=self.f_h,
                                   relief="flat", padx=18, pady=6, cursor="hand2",
                                   command=self._start_test)
        self.start_btn.pack(side="left", padx=(8, 4))

        self.stop_btn = tk.Button(self.ctrl, text="⏹  Stop", font=self.f_h,
                                  relief="flat", padx=18, pady=6, cursor="hand2",
                                  command=self._stop_test, state="disabled")
        self.stop_btn.pack(side="left", padx=(0, 8))

        self.reset_btn = tk.Button(self.ctrl, text="↻  Reset", font=self.f_body,
                                   relief="flat", padx=14, pady=6, cursor="hand2",
                                   command=self._reset)
        self.reset_btn.pack(side="left", padx=4)

        self.new_text_btn = tk.Button(self.ctrl, text="🎲 New Text", font=self.f_body,
                                      relief="flat", padx=14, pady=6, cursor="hand2",
                                      command=self._new_text)
        self.new_text_btn.pack(side="left", padx=4)

    def _build_stats_bar(self):
        cells = [
            ("TIME", "time_val", "s"),
            ("WPM", "wpm_val", ""),
            ("ACCURACY", "acc_val", "%"),
            ("PROGRESS", "prog_val", "%"),
        ]
        for label, attr, suffix in cells:
            card = tk.Frame(self.stats_bar)
            card.pack(side="left", expand=True, fill="x", padx=6, pady=4)
            lbl = tk.Label(card, text=label, font=self.f_stat_label)
            lbl.pack(side="top", pady=(6, 0))
            val = tk.Label(card, text="--", font=self.f_stat)
            val.pack(side="top", pady=(0, 8))
            setattr(self, attr, val)
            setattr(self, attr + "_card", card)
            setattr(self, attr + "_suffix", suffix)

    def _build_reference_card(self):
        self.ref_title = tk.Label(self.ref_card, text="Reference Text", font=self.f_h,
                                  anchor="w", padx=14, pady=8)
        self.ref_title.pack(fill="x")

        self.ref_inner = tk.Frame(self.ref_card)
        self.ref_inner.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.ref_text = tk.Text(self.ref_inner, height=7, wrap="word", font=self.f_mono,
                                relief="flat", padx=16, pady=14, spacing1=4, spacing3=4,
                                cursor="arrow", takefocus=False)
        self.ref_text.pack(fill="both", expand=True)
        self.ref_text.configure(state="disabled")

        # Tags configured in _apply_theme
        self.ref_text.tag_configure("correct")
        self.ref_text.tag_configure("incorrect")
        self.ref_text.tag_configure("pending")
        self.ref_text.tag_configure("current")

    def _build_input_card(self):
        self.input_title = tk.Label(self.input_card, text="Your Input (start typing after pressing Start)",
                                    font=self.f_h, anchor="w", padx=14, pady=8)
        self.input_title.pack(fill="x")

        self.input_inner = tk.Frame(self.input_card)
        self.input_inner.pack(fill="x", padx=12, pady=(0, 12))

        self.input_text = tk.Text(self.input_inner, height=3, wrap="word", font=self.f_mono,
                                  relief="flat", padx=16, pady=12, spacing1=3, spacing3=3,
                                  insertwidth=2)
        self.input_text.pack(fill="x")
        self.input_text.configure(state="disabled")

        self.input_text.bind("<KeyPress>", self._on_key_press)
        self.input_text.bind("<KeyRelease>", self._on_key_release)
        # Prevent pasting / newlines
        self.input_text.bind("<<Paste>>", lambda e: "break")
        self.input_text.bind("<Return>", lambda e: "break")

    def _build_dashboard(self):
        self.dash_title = tk.Label(self.dash_card, text="Performance Analytics",
                                   font=self.f_h, anchor="w", padx=14, pady=8)
        self.dash_title.pack(fill="x")

        self.dash_inner = tk.Frame(self.dash_card)
        self.dash_inner.pack(fill="x", padx=12, pady=(0, 12))

        self.placeholder = tk.Label(self.dash_inner,
                                    text="Complete a test to see detailed performance analytics, "
                                         "WPM breakdown, and error analysis.",
                                    font=self.f_body, justify="left", padx=16, pady=18,
                                    anchor="w")
        self.placeholder.pack(fill="x")

        # Hidden containers populated on finish
        self.metrics_frame = tk.Frame(self.dash_inner)
        self.error_frame = tk.Frame(self.dash_inner)

    # -------------------------------------------------------------- Theme
    def _apply_theme(self):
        t = self.theme
        self.root.configure(bg=t["bg"])
        self.header.configure(bg=t["header"])
        self.title_lbl.configure(bg=t["header"], fg=t["fg"])
        self.theme_btn.configure(bg=t["card_alt"], fg=t["fg"], activebackground=t["card"],
                                 activeforeground=t["fg"])
        self.history_btn.configure(bg=t["card_alt"], fg=t["fg"], activebackground=t["card"],
                                   activeforeground=t["fg"])

        self.ctrl.configure(bg=t["bg"])
        for w in self.ctrl.winfo_children():
            if isinstance(w, tk.Label):
                w.configure(bg=t["bg"], fg=t["muted"])

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TCombobox", fieldbackground=t["card_alt"], background=t["card_alt"],
                        foreground=t["fg"], arrowcolor=t["fg"], bordercolor=t["border"],
                        lightcolor=t["border"], darkcolor=t["border"])
        style.map("TCombobox", fieldbackground=[("readonly", t["card_alt"])],
                  foreground=[("readonly", t["fg"])])
        style.configure("TComboboxListbox", background=t["card_alt"], foreground=t["fg"],
                        selectbackground=t["accent"], selectforeground="#ffffff")
        style.configure("TEntry", fieldbackground=t["card_alt"], foreground=t["fg"],
                        bordercolor=t["border"])

        for btn, accent in [(self.start_btn, t["accent"]), (self.stop_btn, t["bad"]),
                            (self.reset_btn, t["card_alt"]),
                            (self.new_text_btn, t["card_alt"])]:
            btn.configure(bg=accent, fg="#ffffff" if accent == t["accent"] else t["fg"],
                          activebackground=t["card"], activeforeground=t["fg"],
                          highlightthickness=0)

        # Stats bar
        self.stats_bar.configure(bg=t["bg"])
        for attr in ("time_val", "wpm_val", "acc_val", "prog_val"):
            card = getattr(self, attr + "_card")
            card.configure(bg=t["card"], highlightbackground=t["border"],
                           highlightthickness=1, bd=0)
            for child in card.winfo_children():
                child.configure(bg=t["card"])
            val_lbl = getattr(self, attr)
            val_lbl.configure(fg=t["accent"])
            # label child stays muted
            card.winfo_children()[0].configure(fg=t["muted"])

        # Reference card
        self._style_card(self.ref_card, self.ref_title, self.ref_inner)
        self.ref_text.configure(bg=t["card"], fg=t["fg"], highlightbackground=t["border"],
                                highlightthickness=1, bd=0)
        self.ref_text.tag_configure("correct", background=t["correct_bg"], foreground=t["correct_fg"])
        self.ref_text.tag_configure("incorrect", background=t["wrong_bg"], foreground=t["wrong_fg"])
        self.ref_text.tag_configure("pending", background=t["pending_bg"], foreground=t["pending_fg"])
        self.ref_text.tag_configure("current", background=t["accent"], foreground="#ffffff")

        # Input card
        self._style_card(self.input_card, self.input_title, self.input_inner)
        self.input_text.configure(bg=t["card_alt"], fg=t["fg"], insertbackground=t["accent"],
                                  highlightbackground=t["border"], highlightthickness=1, bd=0)

        # Dashboard
        self._style_card(self.dash_card, self.dash_title, self.dash_inner)
        self.placeholder.configure(bg=t["card"], fg=t["muted"])
        self.metrics_frame.configure(bg=t["card"])
        self.error_frame.configure(bg=t["card"])

        btn_label = "☀ Light" if t["name"] == "dark" else "🌙 Dark"
        self.theme_btn.configure(text=btn_label)

    def _style_card(self, card, title, inner):
        t = self.theme
        card.configure(bg=t["bg"])
        title.configure(bg=t["card"], fg=t["muted"])
        inner.configure(bg=t["card"], highlightbackground=t["border"], highlightthickness=1, bd=0)

    def _toggle_theme(self):
        self.theme_name = "light" if self.theme_name == "dark" else "dark"
        self.theme = Theme.get(self.theme_name)
        self._apply_theme()

    # -------------------------------------------------------------- Settings
    def _on_settings_change(self, _event=None):
        for label, secs in self.DURATIONS:
            if self.duration_var.get() == label:
                self.duration = secs
                break
        self.difficulty = self.diff_var.get()
        if not self.test_active:
            self.time_left = self.duration
            self._update_stat("time_val", self.duration)
            self._new_test()

    # -------------------------------------------------------------- Test flow
    def _new_text(self):
        if self.test_active:
            return
        self.reference_text = TextBank.get_text(self.difficulty)
        self._render_reference()
        self._clear_input()
        self._reset_live_stats()
        self.test_finished = False
        self._clear_dashboard()

    def _new_test(self, load=False):
        for label, secs in self.DURATIONS:
            if self.duration_var.get() == label:
                self.duration = secs
                break
        self.difficulty = self.diff_var.get()
        self.reference_text = TextBank.get_text(self.difficulty)
        self._render_reference()
        self._clear_input()
        self._reset_live_stats()
        self.test_finished = False
        self._clear_dashboard()

    def _render_reference(self):
        self.ref_text.configure(state="normal")
        self.ref_text.delete("1.0", "end")
        self.ref_text.insert("1.0", self.reference_text)
        self.ref_text.tag_add("pending", "1.0", "end")
        self.ref_text.configure(state="disabled")

    def _clear_input(self):
        self.input_text.configure(state="normal")
        self.input_text.delete("1.0", "end")
        self.input_text.configure(state="disabled")

    def _reset_live_stats(self):
        self.time_left = self.duration
        self._update_stat("time_val", self.duration)
        self._update_stat("wpm_val", 0)
        self._update_stat("acc_val", 100)
        self._update_stat("prog_val", 0)
        self.key_hits = 0
        self.backspaces = 0
        self.start_time = 0.0
        self.test_active = False

    def _start_test(self):
        # Refresh settings
        for label, secs in self.DURATIONS:
            if self.duration_var.get() == label:
                self.duration = secs
                break
        self.difficulty = self.diff_var.get()

        self.reference_text = TextBank.get_text(self.difficulty)
        self._render_reference()
        self._clear_input()
        self._reset_live_stats()
        self._clear_dashboard()
        self.test_finished = False

        self.input_text.configure(state="normal")
        self.input_text.focus_set()
        self.input_title.configure(text="Type the reference text below — timer starts on first key!")
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")

    def _stop_test(self):
        if not self.test_active and not self.test_finished:
            return
        if self._timer_id is not None:
            self.root.after_cancel(self._timer_id)
            self._timer_id = None
        self.test_active = False
        self.test_finished = True
        self.input_text.configure(state="disabled")
        self.input_title.configure(text="Test stopped by user.")
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")

    def _reset(self):
        if self._timer_id is not None:
            self.root.after_cancel(self._timer_id)
            self._timer_id = None
        self.test_active = False
        self.test_finished = False
        self.input_text.configure(state="disabled")
        self.input_title.configure(text="Your Input (start typing after pressing Start)")
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self._new_test()

    # -------------------------------------------------------------- Keys
    def _on_key_press(self, event):
        if not self.test_active and not self.test_finished:
            # Start on first meaningful key
            if event.keysym in ("BackSpace", "Return", "Tab", "Escape", "Shift_L", "Shift_R",
                                "Control_L", "Control_R", "Alt_L", "Alt_R", "Left", "Right",
                                "Up", "Down", "Caps_Lock"):
                return
            self._begin_timer()

        if self.test_finished:
            return "break"

        # Count keys
        if event.keysym == "BackSpace":
            self.backspaces += 1
        elif event.keysym == "Return":
            return "break"
        elif len(event.char) == 1 and event.char.isprintable():
            self.key_hits += 1

    def _on_key_release(self, _event):
        if self.test_finished:
            return
        self._update_highlighting()
        self._update_live_stats()
        if self._check_complete():
            self._finish_test()

    def _begin_timer(self):
        self.test_active = True
        self.start_time = time.time()
        self.time_left = self.duration
        self._tick_timer()

    def _tick_timer(self):
        if not self.test_active or self.test_finished:
            return
        elapsed = time.time() - self.start_time
        self.time_left = max(0, self.duration - elapsed)
        self._update_stat("time_val", int(self.time_left))
        self._update_live_stats()
        if self.time_left <= 0:
            self._finish_test()
            return
        self._timer_id = self.root.after(200, self._tick_timer)

    # -------------------------------------------------------------- Highlighting
    def _get_typed(self):
        raw = self.input_text.get("1.0", "end-1c")
        return raw.replace("\n", " ")

    def _update_highlighting(self):
        typed = self._get_typed()
        ref = self.reference_text
        self.ref_text.configure(state="normal")
        self.ref_text.tag_remove("correct", "1.0", "end")
        self.ref_text.tag_remove("incorrect", "1.0", "end")
        self.ref_text.tag_remove("current", "1.0", "end")

        n = len(ref)
        for i in range(min(len(typed), n)):
            start = self.ref_text.index(f"1.0 + {i} chars")
            end = self.ref_text.index(f"1.0 + {i+1} chars")
            tag = "correct" if typed[i] == ref[i] else "incorrect"
            self.ref_text.tag_add(tag, start, end)

        # Current cursor marker
        idx = len(typed)
        if idx < n:
            start = self.ref_text.index(f"1.0 + {idx} chars")
            end = self.ref_text.index(f"1.0 + {idx+1} chars")
            self.ref_text.tag_add("current", start, end)

        self.ref_text.configure(state="disabled")

    def _update_live_stats(self):
        typed = self._get_typed()
        ref = self.reference_text
        elapsed = time.time() - self.start_time if self.start_time else 0

        correct = 0
        for i in range(min(len(typed), len(ref))):
            if typed[i] == ref[i]:
                correct += 1

        total = len(typed)
        acc = (correct / total * 100) if total > 0 else 100.0
        words_typed = len(typed.split()) if typed.strip() else 0
        wpm = (words_typed / elapsed * 60) if elapsed > 0 else 0
        progress = (len(typed) / len(ref) * 100) if ref else 0

        self._update_stat("wpm_val", int(wpm))
        self._update_stat("acc_val", int(acc))
        self._update_stat("prog_val", int(min(progress, 100)))

    def _check_complete(self):
        typed = self._get_typed()
        return len(typed) >= len(self.reference_text)

    # -------------------------------------------------------------- Finish
    def _finish_test(self):
        if self.test_finished:
            return
        self.test_finished = True
        self.test_active = False
        if self._timer_id is not None:
            self.root.after_cancel(self._timer_id)
            self._timer_id = None

        self.input_text.configure(state="disabled")
        self.input_title.configure(text="Test complete — see analytics below.")
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")

        typed = self._get_typed()
        ref = self.reference_text
        elapsed = time.time() - self.start_time if self.start_time else self.duration
        elapsed = max(elapsed, 0.001)

        correct = 0
        for i in range(min(len(typed), len(ref))):
            if typed[i] == ref[i]:
                correct += 1
        total = len(typed)
        errors = total - correct

        raw_wpm = (total / 5) / (elapsed / 60)
        net_wpm = max(0, raw_wpm - (errors / (elapsed / 60)))
        accuracy = (correct / total * 100) if total > 0 else 0.0

        self._update_stat("time_val", 0)
        self._update_stat("wpm_val", int(net_wpm))
        self._update_stat("acc_val", int(accuracy))
        self._update_stat("prog_val", 100 if total >= len(ref) else int(total / len(ref) * 100))

        # Build error table (word-level)
        error_rows = self._build_error_rows(ref, typed)

        self._render_dashboard({
            "raw_wpm": raw_wpm,
            "net_wpm": net_wpm,
            "accuracy": accuracy,
            "elapsed": elapsed,
            "key_hits": self.key_hits,
            "backspaces": self.backspaces,
            "correct": correct,
            "errors": errors,
            "total": total,
            "error_rows": error_rows,
        })

        # Save history
        now = dt.datetime.now()
        record = {
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "difficulty": self.difficulty,
            "duration": self.duration,
            "raw_wpm": round(raw_wpm, 1),
            "net_wpm": round(net_wpm, 1),
            "accuracy": round(accuracy, 1),
            "key_hits": self.key_hits,
            "backspaces": self.backspaces,
            "errors": errors,
        }
        self.history.add(record)

    def _build_error_rows(self, ref, typed):
        ref_words = ref.split()
        typed_words = typed.split()
        rows = []
        for i in range(max(len(ref_words), len(typed_words))):
            expected = ref_words[i] if i < len(ref_words) else ""
            actual = typed_words[i] if i < len(typed_words) else ""
            if expected != actual:
                rows.append((i + 1, expected, actual))
        return rows

    # -------------------------------------------------------------- Dashboard
    def _clear_dashboard(self):
        for w in self.metrics_frame.winfo_children():
            w.destroy()
        for w in self.error_frame.winfo_children():
            w.destroy()
        self.metrics_frame.pack_forget()
        self.error_frame.pack_forget()
        self.placeholder.pack(fill="x")

    def _render_dashboard(self, m):
        self.placeholder.pack_forget()
        t = self.theme

        self.metrics_frame.configure(bg=t["card"])
        self.metrics_frame.pack(fill="x", padx=0, pady=(0, 10))

        items = [
            ("Raw WPM", f"{m['raw_wpm']:.1f}", t["accent"]),
            ("Net WPM", f"{m['net_wpm']:.1f}", t["good"]),
            ("Accuracy", f"{m['accuracy']:.1f}%", t["good"] if m["accuracy"] >= 90 else t["warn"]),
            ("Time Used", f"{m['elapsed']:.1f}s", t["fg"]),
            ("Key Hits", f"{m['key_hits']}", t["fg"]),
            ("Backspaces", f"{m['backspaces']}", t["bad"]),
            ("Correct Chars", f"{m['correct']}", t["good"]),
            ("Errors", f"{m['errors']}", t["bad"]),
        ]
        for i, (label, value, color) in enumerate(items):
            cell = tk.Frame(self.metrics_frame, bg=t["card"])
            cell.grid(row=0, column=i, padx=6, pady=10, sticky="nsew")
            self.metrics_frame.grid_columnconfigure(i, weight=1, uniform="m")
            tk.Label(cell, text=label, font=self.f_stat_label, bg=t["card"],
                     fg=t["muted"]).pack(pady=(4, 0))
            tk.Label(cell, text=value, font=("Segoe UI Semibold", 20, "bold"),
                     bg=t["card"], fg=color).pack(pady=(0, 8))

        # Error table
        self.error_frame.configure(bg=t["card"])
        self.error_frame.pack(fill="x")

        header = tk.Frame(self.error_frame, bg=t["card"])
        header.pack(fill="x", padx=10, pady=(8, 4))
        tk.Label(header, text="Error Analysis — Expected vs Typed Words",
                 font=self.f_h, bg=t["card"], fg=t["fg"]).pack(side="left")

        if not m["error_rows"]:
            tk.Label(self.error_frame, text="No word-level errors. Great job!",
                     font=self.f_body, bg=t["card"], fg=t["good"], padx=10,
                     pady=10, anchor="w").pack(fill="x")
            return

        tree_frame = tk.Frame(self.error_frame, bg=t["card"])
        tree_frame.pack(fill="x", padx=10, pady=(0, 12))

        tree = ttk.Treeview(tree_frame, columns=("idx", "expected", "typed"),
                            show="headings", height=min(len(m["error_rows"]), 8))
        tree.heading("idx", text="#")
        tree.heading("expected", text="Expected Word")
        tree.heading("typed", text="Your Typed Word")
        tree.column("idx", width=50, anchor="center", stretch=False)
        tree.column("expected", width=260, anchor="w")
        tree.column("typed", width=260, anchor="w")

        style = ttk.Style()
        style.configure("Err.Treeview", background=t["card_alt"], foreground=t["fg"],
                        fieldbackground=t["card_alt"], bordercolor=t["border"],
                        rowheight=26, font=self.f_body)
        style.configure("Err.Treeview.Heading", background=t["card"], foreground=t["muted"],
                        font=self.f_stat_label, bordercolor=t["border"])
        style.map("Err.Treeview", background=[("selected", t["accent"])],
                  foreground=[("selected", "#ffffff")])
        tree.configure(style="Err.Treeview")

        for idx, expected, actual in m["error_rows"]:
            tree.insert("", "end", values=(idx, expected, actual if actual else "(missing)"))
        tree.pack(fill="x")

    # -------------------------------------------------------------- History
    def _open_history(self):
        HistoryWindow(self.root, self.history, self.theme, self.f_title, self.f_h,
                      self.f_body, self.f_small)

    # -------------------------------------------------------------- Helpers
    def _update_stat(self, attr, value):
        suffix = getattr(self, attr + "_suffix", "")
        lbl = getattr(self, attr)
        lbl.configure(text=f"{value}{suffix}")


# ---------------------------------------------------------------------------
# History / Leaderboard popup window
# ---------------------------------------------------------------------------
class HistoryWindow:
    def __init__(self, parent, history, theme, f_title, f_h, f_body, f_small):
        self.history = history
        self.theme = theme
        t = theme

        self.win = tk.Toplevel(parent)
        self.win.title("History & Leaderboard")
        self.win.geometry("820x600")
        self.win.configure(bg=t["bg"])
        self.win.transient(parent)
        self.win.grab_set()

        header = tk.Frame(self.win, bg=t["header"])
        header.pack(fill="x")
        tk.Label(header, text="🏆 History & Leaderboard", font=f_title, bg=t["header"],
                 fg=t["fg"], padx=20, pady=14).pack(side="left")

        btn_frame = tk.Frame(self.win, bg=t["bg"])
        btn_frame.pack(fill="x", padx=20, pady=(10, 4))

        self.tab_var = tk.StringVar(value="leaderboard")
        for label, val in [("Leaderboard", "leaderboard"), ("Recent Tests", "recent")]:
            b = tk.Radiobutton(btn_frame, text=label, variable=self.tab_var, value=val,
                               font=f_body, bg=t["bg"], fg=t["muted"],
                               selectcolor=t["card_alt"], activebackground=t["bg"],
                               activeforeground=t["fg"], indicatoron=False,
                               relief="flat", padx=16, pady=6, cursor="hand2",
                               command=self._refresh)
            b.pack(side="left", padx=4)

        clear_btn = tk.Button(btn_frame, text="🗑 Clear History", font=f_body,
                              relief="flat", padx=14, pady=6, cursor="hand2",
                              bg=t["bad"], fg="#ffffff",
                              activebackground=t["card"], activeforeground=t["fg"],
                              command=self._clear)
        clear_btn.pack(side="right")

        self.tree_frame = tk.Frame(self.win, bg=t["bg"])
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=(4, 16))

        self._build_tree()
        self._refresh()

    def _build_tree(self):
        t = self.theme
        cols = ("date", "time", "diff", "dur", "raw", "net", "acc", "hits", "back", "err")
        self.tree = ttk.Treeview(self.tree_frame, columns=cols, show="headings")
        headers = [("date", "Date", 90), ("time", "Time", 80), ("diff", "Difficulty", 90),
                   ("dur", "Dur(s)", 60), ("raw", "Raw WPM", 80), ("net", "Net WPM", 80),
                   ("acc", "Accuracy", 80), ("hits", "Keys", 60), ("back", "Back", 60),
                   ("err", "Errors", 60)]
        for c, text, w in headers:
            self.tree.heading(c, text=text)
            self.tree.column(c, width=w, anchor="center", stretch=False)

        style = ttk.Style()
        style.configure("Hist.Treeview", background=t["card_alt"], foreground=t["fg"],
                        fieldbackground=t["card_alt"], rowheight=26,
                        font=("Segoe UI", 11))
        style.configure("Hist.Treeview.Heading", background=t["card"], foreground=t["muted"],
                        font=("Segoe UI", 10, "bold"))
        style.map("Hist.Treeview", background=[("selected", t["accent"])],
                  foreground=[("selected", "#ffffff")])
        self.tree.configure(style="Hist.Treeview")

        scroll = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def _refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        if self.tab_var.get() == "leaderboard":
            records = self.history.top_scores(50)
        else:
            records = self.history.recent(50)
        if not records:
            return
        for r in records:
            self.tree.insert("", "end", values=(
                r.get("date", ""), r.get("time", ""), r.get("difficulty", ""),
                r.get("duration", ""), r.get("raw_wpm", 0), r.get("net_wpm", 0),
                r.get("accuracy", 0), r.get("key_hits", 0), r.get("backspaces", 0),
                r.get("errors", 0),
            ))

    def _clear(self):
        if messagebox.askyesno("Confirm", "Delete all history records? This cannot be undone.",
                               parent=self.win):
            self.history.clear()
            self._refresh()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    root = tk.Tk()
    app = TypingTestApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()