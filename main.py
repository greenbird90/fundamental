import yfinance as yf
import pandas as pd
import numpy as np
import requests
import datetime
import ta
import os
import time

# =========================
# CONFIG (GITHUB SECRETS)
# =========================
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# =========================
# LIST SAHAM SYARIAH (CURATED)
# =========================
stocks = [

# CONSUMER
"INDF.JK","ICBP.JK","UNVR.JK","MYOR.JK","ROTI.JK",
"SIDO.JK","KLBF.JK","HMSP.JK","GGRM.JK",

# RETAIL
"MAPI.JK","ERAA.JK","ACES.JK","RALS.JK",
"LPPF.JK","AMRT.JK","MIDI.JK","MAPA.JK",

# ENERGY
"ADRO.JK","ITMG.JK","PTBA.JK","HRUM.JK",
"INDY.JK","MBAP.JK","BSSR.JK","TOBA.JK",

# MINING
"ANTM.JK","INCO.JK","MDKA.JK","TINS.JK","NCKL.JK",

# TELEKOMUNIKASI
"TLKM.JK","EXCL.JK","ISAT.JK","MTEL.JK",
"TOWR.JK","TBIG.JK",

# INDUSTRI
"ASII.JK","AUTO.JK","IMAS.JK","UNTR.JK","HEXA.JK",

# PROPERTY
"SMGR.JK","INTP.JK","WSKT.JK","WIKA.JK",
"PTPP.JK","ADHI.JK","BSDE.JK","PWON.JK","CTRA.JK",

# AGRI
"AALI.JK","LSIP.JK","SGRO.JK","TBLA.JK",
"CPIN.JK","JPFA.JK",

# HEALTH
"MIKA.JK","SILO.JK","HEAL.JK","CARE.JK",

# TECH
"GOTO.JK","BUKA.JK","DCII.JK",

# LOGISTIC
"AKRA.JK","SMDR.JK","WINS.JK","ASSA.JK",

# ENERGY GAS
"PGAS.JK","MEDC.JK","ELSA.JK","ESSA.JK","RAJA.JK",

# HIGH RISK
"CUAN.JK","BREN.JK","ARKO.JK"
]

# =========================
# TELEGRAM
# =========================
def send_telegram(msg):
    if not TOKEN or not CHAT_ID:
        print("❌ Token / Chat ID belum diset")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except Exception as e:
        print("Error Telegram:", e)

# =========================
# NORMALISASI DATA
# =========================
def normalize_ratio(val):
    try:
        if val is None:
            return 0
        if val > 1:
            return val / 100
        return val
    except:
        return 0

def normalize_freefloat(ff):
    try:
        if ff > 1:
            ff = ff / 100
        if ff > 1:
            ff = 1
        return ff
    except:
        return 0

# =========================
# DETEKSI
# =========================
def detect_accumulation(hist):
    try:
        vol_avg = hist["Volume"].rolling(20).mean()
        return hist["Volume"].iloc[-1] > vol_avg.iloc[-1] * 1.5
    except:
        return False

def detect_multibagger(growth, roe):
    return growth > 0.2 and roe > 0.2

def classify_freefloat(ff):
    if ff < 0.2:
        return "Low Float 🚀"
    elif ff < 0.5:
        return "Medium Float"
    else:
        return "High Float"

# =========================
# MAIN
# =========================
results = []

print("🚀 Start Screener...")

for stock in stocks:
    try:
        ticker = yf.Ticker(stock)
        time.sleep(1)

        info = ticker.info
        hist = ticker.history(period="6mo")

        if hist.empty:
            continue

        price = hist["Close"].iloc[-1]

        # FUNDAMENTAL
        pe = info.get("trailingPE", 0)
        roe = normalize_ratio(info.get("returnOnEquity", 0))
        growth = normalize_ratio(info.get("revenueGrowth", 0))
        div = normalize_ratio(info.get("dividendYield", 0))

        float_shares = info.get("floatShares", 0)
        shares = info.get("sharesOutstanding", 1)
        ff = normalize_freefloat(float_shares / shares if shares else 0)

        # TEKNIKAL
        hist["rsi"] = ta.momentum.RSIIndicator(hist["Close"]).rsi()
        hist["ma50"] = hist["Close"].rolling(50).mean()
        hist["vol_avg"] = hist["Volume"].rolling(20).mean()

        rsi = hist["rsi"].iloc[-1]
        ma50 = hist["ma50"].iloc[-1]
        volume = hist["Volume"].iloc[-1]
        vol_avg = hist["vol_avg"].iloc[-1]
        low = hist["Low"].min()

        # DETEKSI
        accumulation = detect_accumulation(hist)
        multibagger = detect_multibagger(growth, roe)
        ff_label = classify_freefloat(ff)

        # SCORING
        score = 0
        labels = []

        if pe and pe < 15:
            score += 1
            labels.append("Value")

        if roe > 0.15:
            score += 1

        if growth > 0.1:
            score += 1
            labels.append("Growth")

        if 0.03 < div < 0.1:
            score += 1
            labels.append("Dividen")

        if div >= 0.1:
            labels.append("⚠️ DividendTrap")
            score -= 1

        if ff < 0.2:
            score -= 2
            labels.append("Gorengan")

        if price <= low * 1.2:
            score += 1
            labels.append("Diskon")

        if rsi < 40:
            labels.append("Oversold")

        if price > ma50:
            score += 1

        if volume > vol_avg * 2:
            labels.append("VolumeSpike")

        if accumulation:
            score += 1
            labels.append("Bandar")

        if multibagger:
            score += 2
            labels.append("Multibagger")

        # STATUS
        if score >= 7:
            status = "🟢 Strong Buy"
        elif score >= 5:
            status = "🟡 Menarik"
        elif score >= 3:
            status = "⚠️ Spekulatif"
        else:
            status = "❌ Hindari"

        # ICON
        icon = ""
        if 0.04 < div < 0.1:
            icon += "💰"
        if growth > 0.2:
            icon += "🔥"
        if pe and pe < 10:
            icon += "🧊"
        if accumulation:
            icon += "🏦"

        results.append({
            "stock": stock.replace(".JK",""),
            "price": round(price,2),
            "pe": pe,
            "roe": roe,
            "growth": growth,
            "div": div,
            "ff": ff,
            "ff_label": ff_label,
            "rsi": rsi,
            "score": score,
            "status": status,
            "labels": ", ".join(labels),
            "icon": icon
        })

    except Exception as e:
        print("❌ Error:", stock, e)

# SORT
results = sorted(results, key=lambda x: x["score"], reverse=True)

# =========================
# TELEGRAM OUTPUT
# =========================
today = datetime.date.today()

msg = f"🤖 ULTIMATE AI SCREENER\n{today}\n\n"

msg += """==============================
📘 LEGEND
==============================
🟢 Strong Buy  : Layak entry
🟡 Menarik     : Watchlist
⚠️ Spekulatif  : Risiko tinggi
❌ Hindari     : Abaikan

🏦 Bandar      : Akumulasi volume
🚀 Multibagger : Potensi 3–10x

Free Float:
Low   = Mudah digerakkan
High  = Stabil
==============================
"""

msg += "\n🏆 TOP PICKS\n"
for i, t in enumerate(results[:3]):
    msg += f"{i+1}. {t['stock']} → {t['labels']}\n"

msg += "\n==============================\n📈 HASIL\n==============================\n"

for r in results[:7]:
    msg += f"""
📈 {r['stock']} {r['icon']}

Harga : {r['price']}
PER : {round(r['pe'],2) if r['pe'] else '-'}
ROE : {round(r['roe']*100,2)}%
Growth : {round(r['growth']*100,2)}%
Dividen : {round(r['div']*100,2)}%
Free Float : {round(r['ff']*100,2)}% ({r['ff_label']})
RSI : {round(r['rsi'],2)}

Score : {r['score']}
Status : {r['status']}
Label : {r['labels']}
"""

# MARKET
msg += "\n==============================\n📊 MARKET INSIGHT\n==============================\n"

avg_rsi = np.mean([r["rsi"] for r in results if not np.isnan(r["rsi"])]) if results else 50

if avg_rsi < 40:
    msg += "📉 Market oversold → Potensi rebound\n"
elif avg_rsi > 60:
    msg += "📈 Market overbought → Waspada koreksi\n"
else:
    msg += "📊 Market sideways → Fokus stock picking\n"

send_telegram(msg)

print("✅ DONE")