"""Recalcule ce que le Script Rain effect doit renvoyer après l'exécution 1 (semaine 1) et l'exécution 2 (deux semaines)."""
import csv
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

IN = Path(__file__).resolve().parent.parent / "data" / "inbox"
RAIN = {"2026-09-17", "2026-09-23", "2026-09-26"}
q = lambda x, n=1: Decimal(x).quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP)
rows = []
for week in (1, 2):
    with open(IN / f"bixi_week{week}.csv", encoding="utf-8") as f:
        rows += [dict(r, week=week) for r in csv.DictReader(f)]
    t = rows
    days = Counter(r["started_at"][:10] for r in t)
    dry = [n for d, n in days.items() if d not in RAIN]; wet = [n for d, n in days.items() if d in RAIN]
    dry_avg = Decimal(sum(dry)) / len(dry); wet_avg = Decimal(sum(wet)) / len(wet)
    st = Counter(r["start_station"] for r in t).most_common(3)
    eb = Decimal(sum(int(r["ebike"]) for r in t)) * 100 / len(t)
    print(f"Exécution {week} : trajets {len(t)}  jours {len(days)}  sec {q(dry_avg)}  pluie {q(wet_avg)}  baisse {q(100 - wet_avg * 100 / dry_avg)} %  électriques {q(eb)} %  stations {st}")
print("Trajets par jour :", ", ".join(f"{d[8:]} : {n}" for d, n in sorted(days.items())))
