"""Util bersama: path, klien HTTP Kalshi dengan throttle + backoff. Semua waktu UTC."""
import time
import threading
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
for _p in (RAW, PROC):
    _p.mkdir(parents=True, exist_ok=True)

KALSHI = "https://api.elections.kalshi.com/trade-api/v2"
SERIES = "KXFEDDECISION"
WINDOW_DAYS = 28  # jendela sebelum rapat (parameter)

# Batas efektif dari mesin ini lebih rendah dari 10 rps (kena 429 di ~1 rps),
# jadi throttle konservatif + backoff eksponensial pada 429/5xx.
MIN_INTERVAL = 0.25


class Kalshi:
    def __init__(self, min_interval=MIN_INTERVAL):
        self.s = requests.Session()
        self.min_interval = min_interval
        self._last = 0.0
        self._lock = threading.Lock()
        self.n_calls = 0
        self.n_429 = 0

    def get(self, path, params=None, retries=8):
        delay = 1.0
        for attempt in range(retries):
            with self._lock:
                wait = self._last + self.min_interval - time.time()
                if wait > 0:
                    time.sleep(wait)
                self._last = time.time()
            self.n_calls += 1
            try:
                r = self.s.get(KALSHI + path, params=params, timeout=60)
            except requests.RequestException:
                time.sleep(delay)
                delay = min(delay * 2, 30)
                continue
            if r.status_code == 200:
                return r.json()
            if r.status_code == 429 or r.status_code >= 500:
                if r.status_code == 429:
                    self.n_429 += 1
                time.sleep(delay)
                delay = min(delay * 2, 30)
                continue
            raise RuntimeError(f"{r.status_code} {path} {params}: {r.text[:300]}")
        raise RuntimeError(f"gagal setelah {retries} percobaan: {path} {params}")
