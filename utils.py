"""Shared helpers for the travel agent."""
import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def load_json(filename: str) -> list:
    """Load a JSON file from the data folder. Returns [] on any error."""
    path = os.path.join(DATA_DIR, filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[error] File not found: {path}")
    except json.JSONDecodeError as e:
        print(f"[error] Invalid JSON in {filename}: {e}")
    return []


def same_text(a: str, b: str) -> bool:
    """Case-insensitive comparison that ignores extra spaces."""
    return str(a).strip().lower() == str(b).strip().lower()