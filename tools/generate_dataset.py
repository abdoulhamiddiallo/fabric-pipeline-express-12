"""Génère deux semaines de trajets BIXI à Montréal, 14 au 27 septembre 2026 (données fictives).

Un fichier CSV par semaine : bixi_week1.csv et bixi_week2.csv.
Les jours de pluie, les Montréalais laissent le vélo au support : c'est ce que le pipeline va mesurer.
"""
import csv, random
from datetime import date, datetime, timedelta
from pathlib import Path

random.seed(1212)
OUT = Path(__file__).resolve().parent.parent / "data" / "inbox"
OUT.mkdir(parents=True, exist_ok=True)

STATIONS = [  # station, poids au départ
    ("Métro Mont-Royal", 15), ("Parc La Fontaine", 12), ("Métro Berri-UQAM", 13), ("Vieux-Port", 9),
    ("Marché Jean-Talon", 10), ("Canal de Lachine", 8), ("Université McGill", 11), ("Métro Atwater", 7),
    ("Parc Jarry", 6), ("Rue Saint-Denis", 9),
]
RAIN = {date(2026, 9, 17): 12.4, date(2026, 9, 23): 8.1, date(2026, 9, 26): 21.6}
names = [s for s, _ in STATIONS]; weights = [w for _, w in STATIONS]
trip_id = 500000
for week in (1, 2):
    start = date(2026, 9, 14) + timedelta(days=7 * (week - 1))
    rows = []
    for k in range(7):
        d = start + timedelta(days=k)
        base = 300 if d.weekday() == 5 else 285 if d.weekday() == 6 else 270
        n = int(base * random.uniform(0.92, 1.08) * (random.uniform(0.40, 0.52) if d in RAIN else 1))
        times = sorted(random.uniform(6, 23.5) for _ in range(n))
        for h in times:
            trip_id += 1
            s = random.choices(names, weights)[0]
            e = random.choice([x for x in names if x != s])
            dur = max(3, int(random.gauss(17 if d.weekday() >= 5 else 13, 6)))
            ts = datetime(d.year, d.month, d.day) + timedelta(hours=h)
            rows.append([trip_id, ts.strftime("%Y-%m-%d %H:%M:%S"), s, e, dur, 1 if random.random() < 0.38 else 0])
    with open(OUT / f"bixi_week{week}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["trip_id", "started_at", "start_station", "end_station", "duration_min", "ebike"]); w.writerows(rows)
    print(f"semaine {week} : {len(rows)} trajets")
