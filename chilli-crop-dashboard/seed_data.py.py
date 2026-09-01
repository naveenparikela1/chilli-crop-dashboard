import random
from datetime import date, timedelta
from database import init_db, get_connection

init_db()
conn = get_connection()
cur = conn.cursor()

# ---------- Regions ----------
regions = [
    ("Guntur", "Andhra Pradesh"),
    ("Khammam", "Telangana"),
    ("Warangal", "Telangana"),
    ("Byadgi", "Karnataka"),
    ("Guntakal", "Andhra Pradesh"),
]
for r in regions:
    cur.execute("INSERT INTO regions (name, state) VALUES (?,?)", r)

# ---------- Varieties ----------
varieties = [
    ("Teja S17", 8.5, 14500, "#dc2626"),
    ("Byadgi Kaddi", 7.2, 12800, "#b91c1c"),
    ("334 Sannur", 6.8, 11200, "#991b1b"),
    ("273 Wrinkle", 7.9, 10500, "#7f1d1d"),
    ("Wonder Hot", 9.1, 13800, "#ea580c"),
]
for v in varieties:
    cur.execute(
        "INSERT INTO varieties (name, avg_yield_qpa, avg_price, color_value) VALUES (?,?,?,?)", v
    )

# ---------- Yields ----------
seasons = ["Rabi", "Kharif"]
for region_id in range(1, 6):
    for variety_id in range(1, 6):
        for year in (2023, 2024):
            cur.execute(
                "INSERT INTO yields (region_id, variety_id, season, year, yield_qpa, area_acres) VALUES (?,?,?,?,?,?)",
                (
                    region_id,
                    variety_id,
                    random.choice(seasons),
                    year,
                    round(random.uniform(5.5, 10.5), 2),
                    round(random.uniform(80, 400), 1),
                ),
            )

# ---------- Weather (last 30 days) ----------
today = date.today()
for region_id in range(1, 6):
    for d in range(30):
        day = today - timedelta(days=d)
        cur.execute(
            "INSERT INTO weather (region_id, record_date, temperature, humidity, rainfall_mm) VALUES (?,?,?,?,?)",
            (
                region_id,
                day.isoformat(),
                round(random.uniform(24, 38), 1),
                round(random.uniform(45, 85), 1),
                round(random.uniform(0, 18), 1),
            ),
        )

# ---------- Pests ----------
pests = [
    ("Thrips", "High", "Neem oil spray + blue sticky traps"),
    ("Aphids", "Medium", "Imidacloprid 17.8% SL"),
    ("Whitefly", "Low", "Yellow sticky traps"),
    ("Fruit Borer", "Critical", "Emamectin benzoate + field sanitation"),
]
for region_id in range(1, 6):
    for name, risk, treat in random.sample(pests, 3):
        cur.execute(
            "INSERT INTO pests (region_id, pest_name, risk_level, affected_acres, treatment, detected_on) VALUES (?,?,?,?,?,?)",
            (
                region_id,
                name,
                risk,
                round(random.uniform(5, 60), 1),
                treat,
                (today - timedelta(days=random.randint(1, 20))).isoformat(),
            ),
        )

# ---------- Market prices (last 20 days) ----------
mandis = ["Guntur Mirchi Yard", "Khammam Mandi", "Byadgi APMC"]
for variety_id in range(1, 6):
    base = varieties[variety_id - 1][2]
    for d in range(20):
        day = today - timedelta(days=d)
        modal = base + random.randint(-800, 800)
        cur.execute(
            "INSERT INTO market_prices (variety_id, mandi, record_date, price_min, price_max, price_modal) VALUES (?,?,?,?,?,?)",
            (
                variety_id,
                random.choice(mandis),
                day.isoformat(),
                modal - 600,
                modal + 600,
                modal,
            ),
        )

# ---------- Alerts ----------
alerts = [
    ("pest", "High", "Thrips outbreak detected in Guntur — 42 acres affected"),
    ("weather", "Medium", "Heavy rainfall expected in Warangal within 48 hours"),
    ("market", "Low", "Teja S17 prices up 4.2% this week at Guntur Mirchi Yard"),
]
for a in alerts:
    cur.execute(
        "INSERT INTO alerts (alert_type, severity, message, created_at) VALUES (?,?,?,?)",
        (*a, datetime.now().isoformat()),
    )

conn.commit()
conn.close()
print("✅ Seed data inserted successfully!")
