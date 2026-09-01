from flask import Flask, jsonify, send_file
from flask_cors import CORS
from database import init_db, query

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return send_file("dashboard.html")


# ---------- Dashboard Overview ----------
@app.route("/api/overview")
def overview():
    kpis = query("""
        SELECT
            (SELECT ROUND(SUM(yield_qpa * area_acres),1) FROM yields WHERE year=2024) AS total_production,
            (SELECT ROUND(AVG(price_modal),0) FROM market_prices) AS avg_price,
            (SELECT COUNT(*) FROM pests WHERE risk_level IN ('High','Critical')) AS pest_alerts,
            (SELECT ROUND(AVG(yield_qpa),2) FROM yields WHERE year=2024) AS avg_yield
    """)[0]

    yield_by_variety = query("""
        SELECT v.name, ROUND(AVG(y.yield_qpa),2) AS avg_yield
        FROM yields y JOIN varieties v ON v.id=y.variety_id
        WHERE y.year=2024 GROUP BY v.name
    """)

    alerts = query("SELECT * FROM alerts ORDER BY created_at DESC LIMIT 5")
    return jsonify({"kpis": kpis, "yield_by_variety": yield_by_variety, "alerts": alerts})


# ---------- Yield Analysis ----------
@app.route("/api/yields")
def yields():
    by_region = query("""
        SELECT r.name AS region, ROUND(AVG(y.yield_qpa),2) AS avg_yield
        FROM yields y JOIN regions r ON r.id=y.region_id
        GROUP BY r.name
    """)
    trend = query("""
        SELECT year, ROUND(AVG(yield_qpa),2) AS avg_yield
        FROM yields GROUP BY year ORDER BY year
    """)
    return jsonify({"by_region": by_region, "trend": trend})


# ---------- Weather ----------
@app.route("/api/weather")
def weather():
    data = query("""
        SELECT record_date, ROUND(AVG(temperature),1) AS temperature,
               ROUND(AVG(humidity),1) AS humidity,
               ROUND(AVG(rainfall_mm),1) AS rainfall_mm
        FROM weather GROUP BY record_date ORDER BY record_date
    """)
    return jsonify(data)


# ---------- Pests ----------
@app.route("/api/pests")
def pests():
    return jsonify(query("""
        SELECT p.*, r.name AS region FROM pests p
        JOIN regions r ON r.id=p.region_id
        ORDER BY CASE p.risk_level
            WHEN 'Critical' THEN 1 WHEN 'High' THEN 2
            WHEN 'Medium' THEN 3 ELSE 4 END
    """))


# ---------- Market ----------
@app.route("/api/market")
def market():
    prices = query("""
        SELECT v.name AS variety, m.record_date, m.price_modal
        FROM market_prices m JOIN varieties v ON v.id=m.variety_id
        ORDER BY m.record_date
    """)
    latest = query("""
        SELECT v.name AS variety, ROUND(AVG(m.price_modal),0) AS modal_price
        FROM market_prices m JOIN varieties v ON v.id=m.variety_id
        WHERE m.record_date = (SELECT MAX(record_date) FROM market_prices)
        GROUP BY v.name
    """)
    return jsonify({"prices": prices, "latest": latest})


# ---------- Initialize DB on first run ----------
with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
