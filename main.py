import yfinance as yf
import pandas as pd
import numpy as np
import requests
import datetime
import ta
import os
import time

# =========================
# CONFIG (AMBIL DARI GITHUB SECRETS)
# =========================
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# =========================
# LIST SAHAM (BISA UPGRADE KE 900 SAHAM)
# =========================
stocks = [

# BANK & FINANCE
"BBCA.JK","BBRI.JK","BMRI.JK","BBNI.JK",
"BRIS.JK","BNGA.JK","BNLI.JK","BJBR.JK","BJTM.JK",

# CONSUMER
"INDF.JK","ICBP.JK","UNVR.JK","MYOR.JK","ROTI.JK",
"SIDO.JK","KLBF.JK","HMSP.JK","GGRM.JK",

# RETAIL & LIFESTYLE
"MAPI.JK","ERAA.JK","ACES.JK","RALS.JK",
"LPPF.JK","AMRT.JK","MIDI.JK","MAPA.JK",

# ENERGY & COAL
"ADRO.JK","ITMG.JK","PTBA.JK","HRUM.JK",
"INDY.JK","MBAP.JK","BSSR.JK","TOBA.JK",

# MINING & METAL
"ANTM.JK","INCO.JK","MDKA.JK","TINS.JK","NCKL.JK",

# INFRA & TELEKOMUNIKASI
"TLKM.JK","EXCL.JK","ISAT.JK","MTEL.JK",
"TOWR.JK","TBIG.JK",

# INDUSTRI & OTOMOTIF
"ASII.JK","AUTO.JK","IMAS.JK",
"UNTR.JK","HEXA.JK",

# CONSTRUCTION & PROPERTY
"SMGR.JK","INTP.JK","WSKT.JK","WIKA.JK",
"PTPP.JK","ADHI.JK","BSDE.JK","PWON.JK","CTRA.JK",

# AGRI & FOOD
"AALI.JK","LSIP.JK","SGRO.JK","TBLA.JK",
"CPIN.JK","JPFA.JK",

# HEALTHCARE
"MIKA.JK","SILO.JK","HEAL.JK","CARE.JK",

# TECHNOLOGY
"GOTO.JK","BUKA.JK","DCII.JK",

# TRANSPORT & LOGISTIC
"AKRA.JK","SMDR.JK","WINS.JK","ASSA.JK",

# MISC HIGH INTEREST
"PGAS.JK","MEDC.JK","ELSA.JK","ESSA.JK",
"RAJA.JK","ARKO.JK","CUAN.JK","BREN.JK",

# DIVIDEND / DEFENSIVE
"TLKM.JK","UNVR.JK","INDF.JK","ICBP.JK",
"SIDO.JK","KLBF.JK","PGAS.JK"
]

# =========================
# TELEGRAM FUNCTION
# =========================
def send_telegram(msg):
    if not TOKEN or not CHAT_ID:
        print("❌ Token / Chat ID belum diset")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    try:
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": msg
        })
    except Exception as e:
        print("Error kirim Telegram:", e)


# =========================
# DETEKSI BANDAR AKUMULASI
# =========================
def detect_accumulation(hist):
    try:
        vol_avg = hist["Volume"].rolling(20).mean()
        return hist["Volume"].iloc[-1] > vol_avg.iloc[-1] * 1.5
    except:
        return False


# =========================
# DETEKSI MULTIBAGGER
# =========================
def detect_multibagger(growth, roe):
    try:
        return growth > 0.20 and roe > 0.20
    except:
        return False


# =========================
# FREE FLOAT
# =========================
def classify_freefloat(ff):
    if ff < 0.2:
        return "Low Float 🚀"
    elif ff < 0.5:
        return "Medium Float"
    else:
        return "High Float"


# =========================
# MAIN SCREENER
# =========================
results = []

print("🚀 Start Screener...")

for stock in stocks:

    try:
        ticker = yf.Ticker(stock)

        # delay biar aman (hindari rate limit)
        time.sleep(1)

        info = ticker.info
        hist = ticker.history(period="6mo")

        if hist.empty:
            continue

        price = hist["Close"].iloc[-1]

        # =========================
        # FUNDAMENTAL
        # =========================
        pe = info.get("trailingPE", 0)
        roe = info.get("returnOnEquity", 0)
        growth = info.get("revenueGrowth", 0)
        div = info.get("dividendYield", 0)

        float_shares = info.get("floatShares", 0)
        shares = info.get("sharesOutstanding", 1)
        free_float = float_shares / shares if shares else 0

        # =========================
        # TEKNIKAL
        # =========================
        hist["rsi"] = ta.momentum.RSIIndicator(hist["Close"]).rsi()
        hist["ma50"] = hist["Close"].rolling(50).mean()
        hist["vol_avg"] = hist["Volume"].rolling(20).mean()

        rsi = hist["rsi"].iloc[-1]
        ma50 = hist["ma50"].iloc[-1]
        volume = hist["Volume"].iloc[-1]
        vol_avg = hist["vol_avg"].iloc[-1]

        low_52 = hist["Low"].min()

        # =========================
        # DETEKSI KHUSUS
        # =========================
        accumulation = detect_accumulation(hist)
        multibagger = detect_multibagger(growth, roe)
        ff_label = classify_freefloat(free_float)

        # =========================
        # SCORING
        # =========================
        score = 0
        labels = []

        if pe and pe < 15:
            score += 1
            labels.append("Value")

        if roe and roe > 0.15:
            score += 1

        if growth and growth > 0.1:
            score += 1
            labels.append("Growth")

        if div and div > 0.03:
            score += 1
            labels.append("Dividen")

        if free_float < 0.2:
            score -= 2
            labels.append("Gorengan")

        if price <= low_52 * 1.2:
            score += 1
            labels.append("Diskon")

        if rsi < 40:
            labels.append("Oversold")

        if price > ma50:
            score += 1

        if volume > vol_avg * 2:
            labels.append("VolumeSpike")

        # BONUS SIGNAL
        if accumulation:
            score += 1
            labels.append("Bandar")

        if multibagger:
            score += 2
            labels.append("Multibagger")

        # =========================
        # STATUS
        # =========================
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
        if div and div > 0.04:
            icon += "💰"
        if growth and growth > 0.2:
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
            "ff": free_float,
            "ff_label": ff_label,
            "rsi": rsi,
            "score": score,
            "status": status,
            "labels": ", ".join(labels),
            "icon": icon
        })

    except Exception as e:
        print("❌ Error:", stock, e)


# =========================
# SORTING
# =========================
results = sorted(results, key=lambda x: x["score"], reverse=True)

# =========================
# FORMAT TELEGRAM
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

# TOP PICKS
msg += "\n🏆 TOP PICKS\n"
for i, t in enumerate(results[:3]):
    msg += f"{i+1}. {t['stock']} → {t['labels']}\n"

msg += "\n==============================\n📈 HASIL\n==============================\n"

# DETAIL
for r in results[:7]:
    msg += f"""
📈 {r['stock']} {r['icon']}

Harga : {r['price']}
PER : {round(r['pe'],2) if r['pe'] else '-'}
ROE : {round(r['roe']*100,2) if r['roe'] else '-'}%
Growth : {round(r['growth']*100,2) if r['growth'] else '-'}%
Dividen : {round(r['div']*100,2) if r['div'] else '-'}%
Free Float : {round(r['ff']*100,2)}% ({r['ff_label']})
RSI : {round(r['rsi'],2)}

Score : {r['score']}
Status : {r['status']}
Label : {r['labels']}
"""

# MARKET INSIGHT
msg += "\n==============================\n📊 MARKET INSIGHT\n==============================\n"

if results:
    avg_rsi = np.mean([r["rsi"] for r in results if not np.isnan(r["rsi"])])
else:
    avg_rsi = 50

if avg_rsi < 40:
    msg += "📉 Market oversold → Potensi rebound\n"
elif avg_rsi > 60:
    msg += "📈 Market overbought → Waspada koreksi\n"
else:
    msg += "📊 Market sideways → Fokus stock picking\n"

# =========================
# KIRIM TELEGRAM
# =========================
send_telegram(msg)

print("✅ Selesai & terkirim ke Telegram")