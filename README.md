# 🌶️ ChilliCrop Analytics

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-4.x-FF6384?logo=chartdotjs&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-success)

> A full-stack **chilli crop monitoring & analytics dashboard** for Indian chilli-growing regions — track yields, weather impact, pest risks, and live mandi market prices in one place.

---

## ✨ Features

| Module | Description |
|---|---|
| 📊 **Overview** | KPI cards (production, price, alerts), yield-by-variety chart, live alerts feed |
| 📈 **Yield Analysis** | Region & variety comparison, yearly trends, revenue potential calculator |
| 🌦️ **Weather Impact** | 30-day temperature/humidity trends, rainfall tracking, weather KPIs |
| 🐛 **Pest Monitor** | Color-coded risk levels (Critical → Low), affected acres, recommended treatments |
| 💰 **Market Prices** | Latest mandi modal prices per variety, price history charts |
| 📋 **Reports** | Report history with status tracking |
| ⚙️ **Settings** | Notification toggles, language & refresh preferences |

**Smart data handling:** the dashboard automatically fetches live data from the Flask API — and gracefully falls back to built-in demo data if the backend is offline.

---

## 🛠️ Tech Stack

- **Backend:** Python 3, Flask, Flask-Cors
- **Database:** SQLite (auto-initialized & seeded)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Charts:** Chart.js 4 (via CDN)
- **Fonts:** Google Fonts (Inter)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/chillicrop-analytics.git
cd chillicrop-analytics

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

#4. Initialize & seed the database (first run only)
python seed_data.py

# 5. Run the app
python app.py
