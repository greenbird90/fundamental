import yfinance as yf
import pandas as pd
import numpy as np
import requests
import datetime
import ta
import os
import time

# =========================
# CONFIG
# =========================
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# =========================
# LIST SAHAM
# =========================
stocks = [# ===== JII =====
"ADRO.JK","AALI.JK","ANTM.JK","ASII.JK","BRIS.JK",
"BRMS.JK","BRPT.JK","BUMI.JK","CPIN.JK","DSSA.JK",
"EXCL.JK","ICBP.JK","INCO.JK","INDF.JK","INKP.JK",
"ISAT.JK","JPFA.JK","KLBF.JK","MDKA.JK","MDKP.JK",
"MEDC.JK","PGAS.JK","PGEO.JK","PANI.JK","PTBA.JK",
"RAJA.JK","TLKM.JK","TPIA.JK","UNTR.JK","UNVR.JK",

# ===== ISSI =====
"AIMS.JK","AISA.JK","AKRA.JK","AKSI.JK","ALDO.JK",
"ALKA.JK","ALMI.JK","AMAG.JK","AMFG.JK","AMIN.JK",
"AMMN.JK","ANDI.JK","ANJT.JK","APEX.JK","APIC.JK",
"APLI.JK","APLN.JK","ARCI.JK","ARGO.JK","ARII.JK",
"ARKO.JK","ARNA.JK","ARTA.JK","ASGR.JK","ASLC.JK",
"ASPI.JK","ASRI.JK","ASSA.JK","ATAP.JK","AUTO.JK",
"AWAN.JK",

"BABY.JK","BAIK.JK","BALI.JK","BAPA.JK","BATA.JK",
"BAYU.JK","BBHI.JK","BBKP.JK","BBMD.JK","BBNI.JK",
"BBRI.JK","BBTN.JK","BCAP.JK","BCIC.JK","BDKR.JK",
"BDMN.JK","BEST.JK","BFIN.JK","BGTG.JK","BHAT.JK",
"BHTN.JK","BIPP.JK","BIRD.JK","BISR.JK","BJBR.JK",
"BJTM.JK","BKDP.JK","BKSL.JK","BMAS.JK","BMRI.JK",
"BMTR.JK","BNA.JK","BNBA.JK","BNGA.JK","BNII.JK",
"BNLI.JK","BOGA.JK","BOLT.JK","BPFI.JK","BPII.JK",
"BRAM.JK","BREN.JK","BRNA.JK","BSDE.JK","BSIM.JK",
"BSSR.JK","BSWD.JK","BTEL.JK","BTON.JK","BUDI.JK",
"BUKA.JK","BUKK.JK","BULL.JK","BUVA.JK","BYAN.JK",

"CAMP.JK","CANI.JK","CARE.JK","CARS.JK","CASA.JK",
"CASS.JK","CBDK.JK","CEKA.JK","CENT.JK","CFIN.JK",
"CGAS.JK","CINT.JK","CITA.JK","CITY.JK","CKRA.JK",
"CLEO.JK","CLPI.JK","CMNP.JK","CMRY.JK","CNKO.JK",
"CNTX.JK","COCO.JK","COWL.JK","CPRO.JK","CSAP.JK",
"CSIS.JK","CTBN.JK","CTRA.JK","CUAN.JK",

"DART.JK","DAYA.JK","DCII.JK","DECK.JK","DEEP.JK",
"DEWA.JK","DGIK.JK","DIGI.JK","DILD.JK","DIVA.JK",
"DKFT.JK","DLTA.JK","DMAS.JK","DMND.JK","DNET.JK",
"DOID.JK","DPNS.JK","DPUM.JK","DSFI.JK","DUCK.JK",
"DWGL.JK","DYAN.JK",

"EAST.JK","ECII.JK","EDGE.JK","EKAD.JK","ELPI.JK",
"ELSA.JK","EMTK.JK","ENAK.JK","ENRG.JK","ENVY.JK",
"EPAC.JK","EPMT.JK","ERAA.JK","ERTX.JK","ESSA.JK",
"ESTA.JK","ESTI.JK","ETWA.JK",

"FAPA.JK","FASW.JK","FAST.JK","FIMP.JK","FIRE.JK",
"FISH.JK","FMII.JK","FORU.JK","FPNI.JK","FREN.JK",
"GAMA.JK","GGRM.JK","GJTL.JK","GLOB.JK","GMFI.JK",
"GOOD.JK","GPRA.JK","GSMF.JK","GTBO.JK","GWSA.JK",

"HADE.JK","HATM.JK","HEAL.JK","HEXA.JK","HITS.JK",
"HKMU.JK","HMSP.JK","HOKI.JK","HRME.JK","HRTA.JK",
"HRUM.JK","IATA.JK","ICON.JK","IDPR.JK","IFII.JK",
"IFSH.JK","IGAR.JK","IIKP.JK","IKAI.JK","IKAN.JK",
"IMAS.JK","IMJS.JK","IMPC.JK","INAF.JK","INAI.JK",
"INCF.JK","INCI.JK","INDX.JK","INDY.JK","INPP.JK",
"INPS.JK","INRU.JK","INTD.JK","INTP.JK","IPCC.JK",
"IPOL.JK","ISPL.JK","ITMA.JK","ITMG.JK",

"JAWA.JK","JECC.JK","JGLE.JK","JHAS.JK","JIIPE.JK",
"JKSW.JK","JPMA.JK","JRPT.JK","JSMR.JK","JSPT.JK",

"KAEF.JK","KARW.JK","KBLI.JK","KBLM.JK","KBMF.JK",
"KBRI.JK","KDSI.JK","KEEN.JK","KIAS.JK","KIJA.JK",
"KINO.JK","KARV.JK","KKES.JK","KKGI.JK","KMTR.JK",
"KOIN.JK","KONI.JK","KPAL.JK","KPIG.JK","KRAS.JK",
"KRAH.JK","KREN.JK","KRYA.JK","KTIN.JK","KUAS.JK",

"LAPD.JK","LATF.JK","LCGP.JK","LCKM.JK","LEAD.JK",
"LIFE.JK","LINK.JK","LION.JK","LMAS.JK","LMSH.JK",
"LPCK.JK","LPIN.JK","LPKR.JK","LPPF.JK","LPPS.JK",
"LSIP.JK","LTLS.JK","LYC.JK",

"MABA.JK","MAIN.JK","MAMI.JK","MAPA.JK","MAPI.JK",
"MARI.JK","MARK.JK","MASA.JK","MAYA.JK","MBAP.JK",
"MBSS.JK","MBTO.JK","MCAS.JK","MCOL.JK","MCOR.JK",
"MDIA.JK","MDLN.JK","MDRN.JK","MEGA.JK","MERK.JK",
"META.JK","MFMI.JK","MGNA.JK","MICE.JK","MIDI.JK",
"MIKA.JK","MIRA.JK","MITI.JK","MKNT.JK","MKPI.JK",
"MLBI.JK","MLIA.JK","MLPL.JK","MLPT.JK","MNCN.JK",
"MOLI.JK","MPOW.JK","MPPA.JK","MPXL.JK","MRAT.JK",
"MSIE.JK","MSIN.JK","MTDL.JK","MTEL.JK","MTLA.JK",
"MTMH.JK","MTSM.JK","MTWI.JK","MYOR.JK","MYRX.JK",
"MYOH.JK",

"NANO.JK","NATO.JK","NELY.JK","NETV.JK","NICK.JK",
"NIKL.JK","NISP.JK","NIRO.JK","NRCA.JK","NUSA.JK",

"OASA.JK","OCAP.JK","OKAS.JK","OMED.JK",

"PACK.JK","PADI.JK","PALM.JK","PAMG.JK","PANR.JK",
"PANS.JK","PAPA.JK","PBRX.JK","PBID.JK","PDES.JK",
"PDGR.JK","PDSI.JK","PEGE.JK","PGLI.JK","PGUN.JK",
"PICO.JK","PIDRA.JK","PINS.JK","PJAA.JK","PKPK.JK",
"PLAN.JK","PLAS.JK","PLIN.JK","PNBS.JK","PNIN.JK",
"PNLF.JK","PNSE.JK","POLL.JK","POLU.JK","POLY.JK",
"PORT.JK","POSA.JK","POWR.JK","PPGL.JK","PPRE.JK",
"PPRO.JK","PRAS.JK","PRAY.JK","PRDA.JK","PRIM.JK",
"PRIN.JK","PSAB.JK","PSDN.JK","PSSI.JK","PTDU.JK",
"PTPP.JK","PTRO.JK","PTSN.JK","PUDP.JK","PURA.JK",
"PWON.JK","PYFA.JK",

"RALS.JK","RANC.JK","RBMS.JK","RDTX.JK","REAL.JK",
"RELI.JK","RIMO.JK","RKES.JK","RODA.JK","ROTI.JK",
"RSCH.JK",

"SAFE.JK","SAME.JK","SAMF.JK","SAPX.JK","SATU.JK",
"SCCO.JK","SCMA.JK","SDMU.JK","SDPC.JK","SDRA.JK",
"SEAN.JK","SGRO.JK","SHID.JK","SIAP.JK","SIDO.JK",
"SILO.JK","SIMA.JK","SIMP.JK","SINI.JK","SIPD.JK",
"SKBM.JK","SKLT.JK","SKRN.JK","SMAR.JK","SMDR.JK",
"SMGR.JK","SMKL.JK","SMMT.JK","SMRA.JK","SMSM.JK",
"SOCI.JK","SONA.JK","SPMA.JK","SPTO.JK","SRIL.JK",
"SRSN.JK","SSIA.JK","SSMS.JK","SSTM.JK","STAA.JK",
"STAR.JK","STTP.JK","SULI.JK","SUPJ.JK","SUPR.JK",
"SURI.JK",

"TALF.JK","TAMA.JK","TAPG.JK","TARA.JK","TBIG.JK",
"TBLA.JK","TCPI.JK","TDPM.JK","TEBE.JK","TIFA.JK",
"TINS.JK","TIRA.JK","TKIM.JK","TOBA.JK","TOTL.JK",
"TOWR.JK","TPMA.JK","TRAM.JK","TRIO.JK","TRIS.JK",
"TRST.JK","TRUS.JK","TSPC.JK","TURI.JK",

"UGMO.JK","ULTJ.JK","UMBU.JK","UNIC.JK","URBN.JK",

"VINS.JK","VOKS.JK",

"WAPO.JK","WEGE.JK","WEHA.JK","WICO.JK","WIIM.JK",
"WIKA.JK","WINS.JK","WINR.JK","WMUU.JK","WOOD.JK",
"WSBP.JK","WSKT.JK","WTON.JK",

"YELO.JK","YULE.JK","ZBRA.JK","ZUCO.JK"
]

# =========================
# TELEGRAM
# =========================
def send_telegram(msg):
    if not TOKEN or not CHAT_ID:
        print("❌ Token belum diset")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

# =========================
# NORMALISASI
# =========================
def normalize(val):
    try:
        if val is None:
            return 0
        return val if val < 1 else val / 100
    except:
        return 0

def normalize_ff(val):
    try:
        if val > 1:
            val = val / 100
        return min(val,1)
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

def classify_ff(ff):
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

for stock in stocks:
    try:
        ticker = yf.Ticker(stock)
        time.sleep(1)

        info = ticker.info
        hist = ticker.history(period="6mo")

        if hist.empty:
            continue

        price = hist["Close"].iloc[-1]

        pe = info.get("trailingPE", 0)
        roe = normalize(info.get("returnOnEquity", 0))
        growth = normalize(info.get("revenueGrowth", 0))
        div = normalize(info.get("dividendYield", 0))

        float_shares = info.get("floatShares", 0)
        shares = info.get("sharesOutstanding", 1)
        ff = normalize_ff(float_shares / shares if shares else 0)

        # teknikal
        hist["rsi"] = ta.momentum.RSIIndicator(hist["Close"]).rsi()
        hist["ma50"] = hist["Close"].rolling(50).mean()
        hist["vol_avg"] = hist["Volume"].rolling(20).mean()

        rsi = hist["rsi"].iloc[-1]
        ma50 = hist["ma50"].iloc[-1]
        volume = hist["Volume"].iloc[-1]
        vol_avg = hist["vol_avg"].iloc[-1]
        low = hist["Low"].min()

        accumulation = detect_accumulation(hist)
        multibagger = detect_multibagger(growth, roe)
        ff_label = classify_ff(ff)

        score = 0
        labels = []

        # VALUE
        if pe and pe < 15:
            score += 1
            labels.append("Value")

        # ROE
        if roe > 0.15:
            score += 1

        # GROWTH
        if growth > 0.1:
            score += 1
            labels.append("Growth")

        # ❗ GROWTH TAPI ROE JELEK
        if growth > 0.1 and roe < 0.1:
            labels.append("⚠️ Growth Lemah")
            score -= 1

        # ❗ GROWTH NEGATIF
        if growth < 0:
            labels.append("⚠️ Declining")
            score -= 1

        # DIVIDEN NORMAL
        if 0.03 < div < 0.1:
            score += 1
            labels.append("Dividen")

        # ❗ DIVIDEND TRAP
        if div >= 0.12:
            labels.append("⚠️ Dividend Trap")
            score -= 2

        # ❗ GORENGAN
        if ff < 0.2:
            score -= 2
            labels.append("Gorengan")

        # DISKON
        if price <= low * 1.2:
            score += 1
            labels.append("Diskon")

        # RSI
        if rsi < 40:
            labels.append("Oversold")

        # TREND
        if price > ma50:
            score += 1

        # VOLUME
        if volume > vol_avg * 2:
            labels.append("VolumeSpike")

        # BANDAR
        if accumulation:
            score += 1
            labels.append("Bandar")

        # MULTIBAGGER
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
        print("Error:", stock, e)

# SORT
results = sorted(results, key=lambda x: x["score"], reverse=True)

# =========================
# OUTPUT TELEGRAM
# =========================
today = datetime.date.today()

msg = f"🤖 ULTIMATE AI SCREENER PRO\n{today}\n\n"

msg += """==============================
📘 LEGEND
==============================
🟢 Strong Buy  : Layak entry
🟡 Menarik     : Watchlist
⚠️ Spekulatif  : Risiko tinggi
❌ Hindari     : Abaikan

🏦 Bandar      : Akumulasi volume
🚀 Multibagger : Potensi 3–10x

⚠️ Warning:
Growth Lemah = Growth tinggi tapi tidak efisien
Declining    = Revenue turun
Dividend Trap= Dividen tidak sehat

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

# MARKET INSIGHT
msg += "\n==============================\n📊 MARKET INSIGHT\n==============================\n"

avg_rsi = np.mean([r["rsi"] for r in results if not np.isnan(r["rsi"])])

if avg_rsi < 40:
    msg += "📉 Market oversold → Potensi rebound\n"
elif avg_rsi > 60:
    msg += "📈 Market overbought → Waspada koreksi\n"
else:
    msg += "📊 Market sideways → Fokus stock picking\n"

send_telegram(msg)

print("✅ DONE")