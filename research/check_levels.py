import pandas as pd
import sys
sys.stdout.reconfigure(encoding="utf-8")

pl = pd.read_csv("data_price_level.csv", parse_dates=["date"])
pl = pl.sort_values("date").reset_index(drop=True)
print("Columns:", [c.encode("ascii","replace").decode() for c in pl.columns.tolist()])
print()

# During known bull dips
dips = ["2024-05-01","2024-07-07","2024-08-05","2025-04-08","2023-08-26",
        "2024-01-22","2024-03-19","2024-09-06","2025-03-10"]

for d in dips:
    row = pl[pl["date"] <= d].tail(1).iloc[0]
    px   = row["btc_price"]
    sth  = row.iloc[2]   # sth_cost_basis
    mvrv = row.iloc[7]   # MVRV 0σ
    cpl  = row.iloc[12]  # cum_pl_price
    print(f"{row['date'].date()} | price=${px:>8,.0f} | STH_RP=${sth:>8,.0f} | "
          f"MVRV0s=${mvrv:>8,.0f} | CumPL=${cpl:>8,.0f} | "
          f"px/STH={px/sth:.3f} | px/MVRV0s={px/mvrv:.3f} | px/CumPL={px/cpl:.3f}")

print()
# Show 2024 May range to understand level dynamics
print("--- 2024 April-August detail ---")
sub = pl[(pl["date"] >= "2024-04-01") & (pl["date"] <= "2024-08-31")]
sub = sub.iloc[::7]  # weekly
for _, row in sub.iterrows():
    px   = row["btc_price"]
    sth  = row.iloc[2]
    mvrv = row.iloc[7]
    cpl  = row.iloc[12]
    print(f"{row['date'].date()} | px=${px:>8,.0f} | STH_RP=${sth:>8,.0f} | "
          f"MVRV0s=${mvrv:>8,.0f} | CumPL=${cpl:>8,.0f} | px/STH={px/sth:.3f}")
