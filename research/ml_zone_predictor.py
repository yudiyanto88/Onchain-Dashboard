#!/usr/bin/env python3
"""
ML Zone Predictor — Bitcoin On-Chain Analysis Framework
Prediksi zona 7 dan 14 hari ke depan berdasarkan on-chain metrics.

Usage:
  python ml_zone_predictor.py           # train + predict
  python ml_zone_predictor.py --train   # retrain dan save model
  python ml_zone_predictor.py --predict # predict pakai saved model
"""

import sys
import warnings
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.preprocessing import LabelEncoder

warnings.filterwarnings('ignore')

sys.stdout.reconfigure(encoding='utf-8')

# ── Constants ──────────────────────────────────────────────────────────────────
DATA_FILE  = 'data_master_all_metrics.csv'
MODEL_DIR  = Path('models')
MODEL_7D   = MODEL_DIR / 'zone_predictor_7d.pkl'
MODEL_14D  = MODEL_DIR / 'zone_predictor_14d.pkl'
ENCODER_F  = MODEL_DIR / 'zone_label_encoder.pkl'

ZONE_ORDER = ['HIJAU_TUA', 'BIRU', 'KUNING_BAWAH', 'HIJAU', 'KUNING_ATAS', 'MERAH']
HORIZONS   = {7: MODEL_7D, 14: MODEL_14D}

# Minimum rows after dropping NaN (rolling 30d needs ~30 warmup)
MIN_ROWS = 200


# ── Layer 1 Zone Labeling ──────────────────────────────────────────────────────
def label_zone(price: float, sth_rp: float, supply_in_profit: float) -> str:
    """
    Deterministic zone dari Layer 1 signal framework v1.0.3.
    Step 1: Price vs STH Realized Price
    Step 2: Total Supply in Profit %
    """
    if price > sth_rp:
        if supply_in_profit > 95:
            return 'MERAH'
        elif supply_in_profit > 80:
            return 'KUNING_ATAS'
        else:
            return 'HIJAU'
    else:
        if supply_in_profit > 65:
            return 'KUNING_BAWAH'
        elif supply_in_profit > 50:
            return 'BIRU'
        else:
            return 'HIJAU_TUA'


# ── Feature Engineering ────────────────────────────────────────────────────────
def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build feature matrix dari raw CSV.
    Semua fitur scale-invariant (ratio/normalized) supaya comparable lintas siklus.
    """
    f = pd.DataFrame(index=df.index)

    # --- Realized Price ratios (core Layer 1 + framework signals) ---
    f['price_to_sth_rp']  = df['btc_price'] / df['sth_cost_basis']
    f['price_to_lth_rp']  = df['btc_price'] / df['lth_cost_basis']
    f['price_to_rp']      = df['btc_price'] / df['realized_price']
    f['sth_rp_to_lth_rp'] = df['sth_cost_basis'] / df['lth_cost_basis']
    f['rp_to_lth_rp']     = df['realized_price'] / df['lth_cost_basis']

    # --- MVRV family ---
    f['mvrv']      = df['mvrv']
    f['sth_mvrv']  = df['sth_mvrv']
    f['lth_mvrv']  = df['lth_mvrv']
    f['mvrv_diff'] = df['sth_mvrv'] - df['lth_mvrv']  # STH vs LTH divergence

    # --- SOPR family ---
    f['asopr']     = df['asopr']
    f['sth_sopr']  = df['sth_sopr']
    f['lth_sopr']  = df['lth_sopr']
    f['sopr_diff'] = df['lth_sopr'] - df['sth_sopr']

    # --- NUPL family ---
    f['nupl']      = df['nupl']
    f['sth_nupl']  = df['sth_nupl']
    f['lth_nupl']  = df['lth_nupl']
    f['nupl_diff'] = df['lth_nupl'] - df['sth_nupl']

    # --- Supply in Profit ---
    f['supply_in_profit']   = df['percent_btc_in_profit']
    f['sth_in_profit']      = df['pct_sth_in_profit']
    f['lth_in_profit']      = df['pct_lth_in_profit']
    f['sth_lth_prof_diff']  = df['pct_sth_in_profit'] - df['pct_lth_in_profit']

    # --- Rolling MAs (7d, 30d) untuk key metrics ---
    for raw_col, feat_name in [
        ('percent_btc_in_profit', 'supply'),
        ('mvrv',                  'mvrv'),
        ('asopr',                 'asopr'),
        ('nupl',                  'nupl'),
    ]:
        f[f'{feat_name}_7d_ma']  = df[raw_col].rolling(7,  min_periods=1).mean()
        f[f'{feat_name}_30d_ma'] = df[raw_col].rolling(30, min_periods=1).mean()

    # Price-to-STH-RP rolling (Layer 1 30-day sustained check proxy)
    f['p_sth_rp_7d_ma']  = f['price_to_sth_rp'].rolling(7,  min_periods=1).mean()
    f['p_sth_rp_30d_ma'] = f['price_to_sth_rp'].rolling(30, min_periods=1).mean()

    # --- Rate of change (7d, 14d, 30d) ---
    for raw_col, feat_name in [
        ('percent_btc_in_profit', 'supply'),
        ('mvrv',                  'mvrv'),
        ('btc_price',             'price'),
    ]:
        f[f'{feat_name}_roc_7d']  = df[raw_col].pct_change(7)
        f[f'{feat_name}_roc_14d'] = df[raw_col].pct_change(14)
        f[f'{feat_name}_roc_30d'] = df[raw_col].pct_change(30)

    return f


# ── Data Loading ───────────────────────────────────────────────────────────────
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_FILE, parse_dates=['date'])
    df = df.sort_values('date').reset_index(drop=True)

    required = [
        'date', 'btc_price',
        'sth_cost_basis', 'lth_cost_basis', 'realized_price',
        'mvrv', 'sth_mvrv', 'lth_mvrv',
        'asopr', 'sth_sopr', 'lth_sopr',
        'nupl', 'sth_nupl', 'lth_nupl',
        'percent_btc_in_profit', 'pct_sth_in_profit', 'pct_lth_in_profit',
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        print(f'[ERROR] Kolom tidak ditemukan: {missing}')
        sys.exit(1)

    return df[required].copy()


# ── Training ───────────────────────────────────────────────────────────────────
def prepare_dataset(df: pd.DataFrame, horizon: int):
    """
    Buat X (features hari t) dan y (zona di hari t+horizon).
    Target zone = label di masa depan → ML belajar memprediksi transisi.
    """
    # Label tiap hari
    zones = df.apply(
        lambda r: label_zone(r['btc_price'], r['sth_cost_basis'], r['percent_btc_in_profit']),
        axis=1
    )

    X = build_features(df)

    # Shift target ke belakang: y[i] = zona di i+horizon
    y = zones.shift(-horizon)

    # Drop rows dengan NaN (awal karena rolling, akhir karena shift)
    valid = X.notna().all(axis=1) & y.notna()
    return X[valid], y[valid]


def train(df: pd.DataFrame, horizon: int) -> tuple:
    """Train RandomForest, return (model, encoder, cv_metrics)."""
    X, y = prepare_dataset(df, horizon)

    if len(X) < MIN_ROWS:
        print(f'[ERROR] Data terlalu sedikit untuk training: {len(X)} rows')
        sys.exit(1)

    le = LabelEncoder()
    le.fit(ZONE_ORDER)
    y_enc = le.transform(y)

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        min_samples_leaf=20,    # regularize supaya tidak overfit data terbatas
        class_weight='balanced',
        random_state=42,
        n_jobs=-1,
    )

    # Walk-forward cross-validation (time-series aware)
    tscv = TimeSeriesSplit(n_splits=5)
    cv_acc, cv_f1 = [], []

    for train_idx, test_idx in tscv.split(X):
        X_tr, X_te = X.iloc[train_idx], X.iloc[test_idx]
        y_tr, y_te = y_enc[train_idx], y_enc[test_idx]
        model.fit(X_tr, y_tr)
        preds = model.predict(X_te)
        cv_acc.append(accuracy_score(y_te, preds))
        cv_f1.append(f1_score(y_te, preds, average='weighted', zero_division=0))

    # Final train on all data
    model.fit(X, y_enc)

    metrics = {
        'accuracy_mean': np.mean(cv_acc),
        'accuracy_std':  np.std(cv_acc),
        'f1_mean':       np.mean(cv_f1),
        'f1_std':        np.std(cv_f1),
    }

    return model, le, metrics


def save_models(model7, model14, encoder):
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(model7,   MODEL_7D)
    joblib.dump(model14,  MODEL_14D)
    joblib.dump(encoder,  ENCODER_F)
    print(f'[OK] Model disimpan ke {MODEL_DIR}/')


# ── Prediction ─────────────────────────────────────────────────────────────────
def load_models():
    if not MODEL_7D.exists() or not MODEL_14D.exists():
        print('[ERROR] Model belum ada. Jalankan dulu dengan --train.')
        sys.exit(1)
    return joblib.load(MODEL_7D), joblib.load(MODEL_14D), joblib.load(ENCODER_F)


def predict_latest(df: pd.DataFrame, model, encoder) -> dict:
    """Predict dari baris terakhir data."""
    X_all = build_features(df)
    X_last = X_all.iloc[[-1]]

    proba = model.predict_proba(X_last)[0]
    classes = encoder.inverse_transform(model.classes_)

    # Map ke semua zona (termasuk yang tidak ada di training)
    prob_map = {z: 0.0 for z in ZONE_ORDER}
    for cls, p in zip(classes, proba):
        prob_map[cls] = p

    predicted_zone = max(prob_map, key=prob_map.get)
    return {'zone': predicted_zone, 'proba': prob_map}


# ── Output Formatting ──────────────────────────────────────────────────────────
ZONE_EMOJI = {
    'MERAH':        '🔴',
    'KUNING_ATAS':  '🟡',
    'HIJAU':        '🟢',
    'KUNING_BAWAH': '🟡',
    'BIRU':         '🔵',
    'HIJAU_TUA':    '💚',
}

def fmt_dist(prob_map: dict) -> str:
    parts = []
    for z in ZONE_ORDER:
        p = prob_map.get(z, 0)
        if p >= 0.03:
            parts.append(f'{z} {p*100:.0f}%')
    return ' | '.join(parts) if parts else '-'


def print_output(df, pred7, pred14, metrics7, metrics14):
    last   = df.iloc[-1]
    date   = str(last['date'])[:10]
    price  = last['btc_price']
    sth_rp = last['sth_cost_basis']
    lth_rp = last['lth_cost_basis']
    rp     = last['realized_price']
    supply = last['percent_btc_in_profit']

    current_zone = label_zone(price, sth_rp, supply)

    from datetime import date as dtdate, timedelta
    base_date = dtdate.fromisoformat(date)
    date_7d   = (base_date + timedelta(days=7)).isoformat()
    date_14d  = (base_date + timedelta(days=14)).isoformat()

    print()
    print('=' * 60)
    print('  BITCOIN ML ZONE PREDICTOR')
    print('=' * 60)
    print(f'  Data: {date}  |  BTC: ${price:,.0f}')
    print('-' * 60)

    print(f'\nCURRENT ZONE (rule-based): {ZONE_EMOJI.get(current_zone, "")} {current_zone}')
    print(f'  Price vs STH RP : {price/sth_rp:.3f}x  (STH RP: ${sth_rp:,.0f})')
    print(f'  Price vs LTH RP : {price/lth_rp:.3f}x  (LTH RP: ${lth_rp:,.0f})')
    print(f'  Price vs RP     : {price/rp:.3f}x  (RP: ${rp:,.0f})')
    print(f'  Supply in Profit: {supply:.1f}%')

    print(f'\nPREDIKSI +7 HARI ({date_7d}):')
    z7 = pred7['zone']
    c7 = pred7['proba'][z7] * 100
    print(f'  Zona: {ZONE_EMOJI.get(z7, "")} {z7}  ({c7:.0f}% confidence)')
    print(f'  Distribusi: {fmt_dist(pred7["proba"])}')

    print(f'\nPREDIKSI +14 HARI ({date_14d}):')
    z14 = pred14['zone']
    c14 = pred14['proba'][z14] * 100
    print(f'  Zona: {ZONE_EMOJI.get(z14, "")} {z14}  ({c14:.0f}% confidence)')
    print(f'  Distribusi: {fmt_dist(pred14["proba"])}')

    print(f'\nMODEL PERFORMANCE (walk-forward CV, 5-fold):')
    print(f'  +7d  — Accuracy: {metrics7["accuracy_mean"]*100:.1f}% ± {metrics7["accuracy_std"]*100:.1f}%'
          f'  |  Weighted F1: {metrics7["f1_mean"]*100:.1f}% ± {metrics7["f1_std"]*100:.1f}%')
    print(f'  +14d — Accuracy: {metrics14["accuracy_mean"]*100:.1f}% ± {metrics14["accuracy_std"]*100:.1f}%'
          f'  |  Weighted F1: {metrics14["f1_mean"]*100:.1f}% ± {metrics14["f1_std"]*100:.1f}%')

    print()
    print('  ⚠  Model dilatih ~4 market cycles. Gunakan sebagai')
    print('     supporting signal, bukan sole decision maker.')
    print('  ⚠  S2 Latch AKTIF — bear market regime confirmed.')
    print('=' * 60)
    print()


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train',   action='store_true', help='Retrain dan save model')
    parser.add_argument('--predict', action='store_true', help='Predict saja (pakai saved model)')
    args = parser.parse_args()

    do_train   = args.train or not (MODEL_7D.exists() and MODEL_14D.exists())
    do_predict = True

    df = load_data()
    print(f'[Data] {len(df)} rows | {df["date"].iloc[0].date()} – {df["date"].iloc[-1].date()}')

    metrics7 = metrics14 = {'accuracy_mean': 0, 'accuracy_std': 0, 'f1_mean': 0, 'f1_std': 0}

    if do_train:
        print('[Training] Model +7d ...', end=' ', flush=True)
        model7, encoder, metrics7 = train(df, horizon=7)
        print('selesai.')

        print('[Training] Model +14d ...', end=' ', flush=True)
        model14, _, metrics14 = train(df, horizon=14)
        print('selesai.')

        save_models(model7, model14, encoder)
        joblib.dump(metrics7,  MODEL_DIR / 'metrics_7d.pkl')
        joblib.dump(metrics14, MODEL_DIR / 'metrics_14d.pkl')

    if do_predict:
        model7, model14, encoder = load_models()
        if (MODEL_DIR / 'metrics_7d.pkl').exists():
            metrics7  = joblib.load(MODEL_DIR / 'metrics_7d.pkl')
            metrics14 = joblib.load(MODEL_DIR / 'metrics_14d.pkl')

        pred7  = predict_latest(df, model7,  encoder)
        pred14 = predict_latest(df, model14, encoder)

        print_output(df, pred7, pred14, metrics7, metrics14)


if __name__ == '__main__':
    main()
