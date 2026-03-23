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
# LIST SAHAM (PAKAI FULL LIST KAMU)
# =========================
stocks = [
"AADI.JK","AALI.JK","ABMM.JK","ACES.JK","ACST.JK","ADCP.JK","ADES.JK","ADHI.JK","ADMG.JK","ADMR.JK","ADRO.JK","AGAR.JK","AGII.JK","AIMS.JK","AISA.JK","AKKU.JK","AKPI.JK","AKRA.JK","AKSI.JK","ALDO.JK","ALKA.JK","AMAN.JK","AMFG.JK","AMIN.JK","ANDI.JK","ANJT.JK","ANTM.JK","APII.JK","APLI.JK","APLN.JK","ARCI.JK","AREA.JK","ARGO.JK","ARII.JK","ARNA.JK","ARTA.JK","ASGR.JK","ASHA.JK","ASII.JK","ASLC.JK","ASLI.JK","ASPI.JK","ASRI.JK","ASSA.JK","ATAP.JK","ATIC.JK","ATLA.JK","AUTO.JK","AVIA.JK","AWAN.JK","AXIO.JK","AYAM.JK","AYLS.JK","BABY.JK","BAIK.JK","BANK.JK","BAPI.JK","BATA.JK","BATR.JK","BAUT.JK","BAYU.JK","BBRM.JK","BBSS.JK","BCIP.JK","BDKR.JK","BEEF.JK","BELI.JK","BELL.JK","BESS.JK","BEST.JK","BIKE.JK","BINO.JK","BIPP.JK","BIRD.JK","BISI.JK","BKDP.JK","BKSL.JK","BLES.JK","BLOG.JK","BLTA.JK","BLTZ.JK","BLUE.JK","BMHS.JK","BMSR.JK","BMTR.JK","BNBR.JK","BOAT.JK","BOBA.JK","BOGA.JK","BOLA.JK","BOLT.JK","BRAM.JK","BRIS.JK","BRMS.JK","BRNA.JK","BRPT.JK","BRRC.JK","BSBK.JK","BSDE.JK","BSML.JK","BSSR.JK","BTPS.JK","BUAH.JK","BUKK.JK","BULL.JK","BUMI.JK","BUVA.JK","BYAN.JK","CAKK.JK","CAMP.JK","CANI.JK","CARE.JK","CASS.JK","CBDK.JK","CBPE.JK","CBRE.JK","CCSI.JK","CEKA.JK","CGAS.JK","CHEK.JK","CHEM.JK","CINT.JK","CITA.JK","CITY.JK","CLEO.JK","CLPI.JK","CMNP.JK","CMPP.JK","CMRY.JK","CNKO.JK","CNMA.JK","COAL.JK","CPIN.JK","CPRO.JK","CRAB.JK","CRSN.JK","CSAP.JK","CSIS.JK","CSMI.JK","CSRA.JK","CTBN.JK","CTRA.JK","CYBR.JK","DAAZ.JK","DADA.JK","DATA.JK","DAYA.JK","DCII.JK","DEFI.JK","DEPO.JK","DEWA.JK","DEWI.JK","DGIK.JK","DGNS.JK","DGWG.JK","DILD.JK","DIVA.JK","DKFT.JK","DKHH.JK","DMAS.JK","DMMX.JK","DMND.JK","DOOH.JK","DOSS.JK","DRMA.JK","DSFI.JK","DSNG.JK","DSSA.JK","DUTI.JK","DVLA.JK","DWGL.JK","DYAN.JK","EAST.JK","ECII.JK","EDGE.JK","EKAD.JK","ELIT.JK","ELPI.JK","ELSA.JK","ELTY.JK","ENRG.JK","ENVY.JK","EPAC.JK","ERAA.JK","ERCO.JK","ESSA.JK","ESTA.JK","ETWA.JK","EURO.JK","EXCL.JK","EZRA.JK","FAPA.JK","FASW.JK","FILM.JK","FIMP.JK","FIRE.JK","FITT.JK","FMII.JK","FOOD.JK","FORU.JK","FREN.JK","FUTR.JK","GAMA.JK","GDST.JK","GDYR.JK","GEMA.JK","GEMS.JK","GGRM.JK","GIDS.JK","GIHO.JK","GJTL.JK","GLOB.JK","GLVA.JK","GMGI.JK","GOLD.JK","GOOD.JK","GPRA.JK","GRPM.JK","GSLC.JK","GTBO.JK","GTSI.JK","GULA.JK","GZCO.JK","HADE.JK","HAIS.JK","HALO.JK","HATM.JK","HDIT.JK","HEAL.JK","HERO.JK","HEXA.JK","HGII.JK","HITS.JK","HOKI.JK","HOMI.JK","HOPE.JK","HRME.JK","HRUM.JK","HUMI.JK","HYGN.JK","IATA.JK","IBST.JK","ICBP.JK","ICON.JK","IDPR.JK","IFII.JK","IFSH.JK","IGAR.JK","IIKP.JK","IKAI.JK","IKAN.JK","IKBI.JK","IKPM.JK","IMPC.JK","INCI.JK","INCO.JK","INDF.JK","INDR.JK","INDS.JK","INDX.JK","INDY.JK","INET.JK","INKP.JK","INPP.JK","INTD.JK","INTP.JK","IOTF.JK","IPCC.JK","IPCM.JK","IPOL.JK","IPPE.JK","ISAT.JK","ITMA.JK","ITMG.JK","JAWA.JK","JAYA.JK","JECC.JK","JFAA.JK","JGLE.JK","JIHD.JK","JKON.JK","JKSW.JK","JMAS.JK","JPMC.JK","JPFA.JK","JRPT.JK","JSFA.JK","JSMR.JK","JSPT.JK","JTPE.JK","KAEF.JK","KARW.JK","KBAG.JK","KBAR.JK","KBLM.JK","KBLV.JK","KBNP.JK","KDSI.JK","KEEN.JK","KIAS.JK","KICI.JK","KINO.JK","KIOS.JK","KITA.JK","KJEN.JK","KKES.JK","KLBF.JK","KMDS.JK","KOBX.JK","KOIN.JK","KOKA.JK","KONI.JK","KOPI.JK","KOTA.JK","KPIG.JK","KREN.JK","KRYA.JK","KSIX.JK","KUAS.JK","LABA.JK","LABS.JK","LAJU.JK","LAND.JK","LCKM.JK","LION.JK","LIVE.JK","LMPI.JK","LMSH.JK","LPCK.JK","LPIN.JK","LPKR.JK","LPLI.JK","LPPF.JK","LRNA.JK","LSIP.JK","LTLS.JK","LUCK.JK","MAHA.JK","MAIN.JK","MAPA.JK","MAPB.JK","MAPI.JK","MARK.JK","MAXI.JK","MBAP.JK","MBMA.JK","MBTO.JK","MCAS.JK","MCOL.JK","MDIY.JK","MDKA.JK","MDKI.JK","MDLA.JK","MEDC.JK","MEDS.JK","MERI.JK","MERK.JK","META.JK","MFIN.JK","MICE.JK","MIDI.JK","MIKA.JK","MIRA.JK","MITI.JK","MKNT.JK","MMLP.JK","MNCN.JK","MPMX.JK","MREI.JK","MSIN.JK","MSJA.JK","MSKY.JK","MSOL.JK","MTEL.JK","MTFN.JK","MTLA.JK","MTMA.JK","MTSM.JK","MUAI.JK","MULIA.JK","MYOH.JK","MYOR.JK","MYTX.JK","NANO.JK","NAPK.JK","NELY.JK","NETV.JK","NGGA.JK","NICK.JK","NIPS.JK","NIRO.JK","NISP.JK","NOBU.JK","NPGF.JK","NRCA.JK","NSIT.JK","NTBK.JK","NUSA.JK","OASA.JK","OBBI.JK","OCAP.JK","OKAS.JK","OLAH.JK","OMED.JK","OMRE.JK","OPMS.JK","OVOO.JK","PACO.JK","PADA.JK","PAMG.JK","PANI.JK","PANR.JK","PBID.JK","PBKF.JK","PCAR.JK","PDES.JK","PDEV.JK","PEHA.JK","PELI.JK","PENG.JK","PERT.JK","PGAS.JK","PGEO.JK","PGJO.JK","PGLI.JK","PHMP.JK","PICO.JK","PIPE.JK","PIRA.JK","PJAA.JK","PKPK.JK","PKRE.JK","PLAS.JK","PLAU.JK","PLIN.JK","PMMP.JK","POCI.JK","POLL.JK","POLU.JK","POSE.JK","POWR.JK","PPAF.JK","PPGL.JK","PPRO.JK","PRAY.JK","PRDA.JK","PRIM.JK","PSAB.JK","PSAT.JK","PSDN.JK","PSGO.JK","PSKT.JK","PSSI.JK","PTBA.JK","PTIS.JK","PTMP.JK","PTMR.JK","PTPP.JK","PTPS.JK","PTPW.JK","PTSN.JK","PTSP.JK","PURA.JK","PURI.JK","PWON.JK","PZZA.JK","RAAM.JK","RAFI.JK","RAJA.JK","RALS.JK","RANC.JK","RATU.JK","RBMS.JK","RDTX.JK","RGAS.JK","RIGS.JK","RISE.JK","RMKE.JK","RMKO.JK","ROCK.JK","RODA.JK","RONY.JK","ROTI.JK","RSGK.JK","RUIS.JK","SAFE.JK","SAGE.JK","SAME.JK","SAMF.JK","SAPX.JK","SATU.JK","SBMA.JK","SCCO.JK","SCNP.JK","SCPI.JK","SEMA.JK","SGER.JK","SGRO.JK","SHID.JK","SHIP.JK","SICO.JK","SIDO.JK","SILO.JK","SIMP.JK","SIPD.JK","SKBM.JK","SKLT.JK","SKRN.JK","SLIS.JK","SMAR.JK","SMBR.JK","SMCB.JK","SMDM.JK","SMDR.JK","SMGA.JK","SMGR.JK","SMIL.JK","SMKL.JK","SMLE.JK","SMMT.JK","SMRA.JK","SMSM.JK","SNLK.JK","SOCI.JK","SOHO.JK","SOLA.JK","SONA.JK","SOSS.JK","SOTS.JK","SPMA.JK","SPTO.JK","SRTG.JK","SSIA.JK","SSTM.JK","STAA.JK","SULI.JK","SUNI.JK","SWAT.JK","SYST.JK","TAEL.JK","TAFI.JK","TAMU.JK","TAPG.JK","TARA.JK","TAYS.JK","TBIG.JK","TBLA.JK","TBMS.JK","TCID.JK","TCPI.JK","TEBE.JK","TECH.JK","TELE.JK","TFCO.JK","TIFA.JK","TINS.JK","TIRA.JK","TITIS.JK","TKIM.JK","TLDN.JK","TLKM.JK","TMPO.JK","TMAS.JK","TOTL.JK","TOYS.JK","TPIA.JK","TRAM.JK","TRGU.JK","TRIL.JK","TRIM.JK","TRIN.JK","TRIO.JK","TRIS.JK","TRJA.JK","TRST.JK","TRUV.JK","TRUK.JK","TRUS.JK","UCID.JK","UDIN.JK","ULTJ.JK","UNIC.JK","UNIQ.JK","UNTR.JK","UNVR.JK","UVCR.JK","VAST.JK","VERN.JK","VICI.JK","VISI.JK","VKTR.JK","VOKS.JK","WAPO.JK","WEGE.JK","WEHA.JK","WINR.JK","WINS.JK","WIRG.JK","WMUU.JK","WOOD.JK","WOWS.JK","WTON.JK","YELO.JK","YPAS.JK","YUPI.JK","ZATA.JK","ZONE.JK","ZYRX.JK"
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
# CLASSIFIER
# =========================
def classify_ff(ff):
    if ff < 0.2:
        return "Low Float 🚀"
    elif ff < 0.5:
        return "Medium Float"
    else:
        return "High Float"

def classify_der(der):
    if der < 0.5:
        return "Sehat 💪"
    elif der < 1.5:
        return "Normal"
    else:
        return "Tinggi ⚠️"


# =========================
# ELITE FILTER 🔥
# =========================
def is_elite_stock(info, hist):
    try:
        # Market Cap > 1T
        market_cap = info.get("marketCap", 0)
        if market_cap < 1_000_000_000_000:
            return False

        # Volume aktif
        avg_vol = hist["Volume"].rolling(20).mean().iloc[-1]
        if avg_vol < 1_000_000:
            return False

        # ROE minimal
        roe = normalize(info.get("returnOnEquity", 0))
        if roe < 0.05:
            return False

        # Free Float
        float_shares = info.get("floatShares", 0)
        shares = info.get("sharesOutstanding", 1)
        ff = normalize_ff(float_shares / shares if shares else 0)
        if ff < 0.2:
            return False

        # Hindari perusahaan rugi
        net_income = info.get("netIncomeToCommon", 0)
        if net_income and net_income < 0:
            return False

        return True
    except:
        return False


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


# =========================
# MAIN
# =========================
results = []

for stock in stocks:
    try:
        ticker = yf.Ticker(stock)
        time.sleep(0.3)

        info = ticker.info
        hist = ticker.history(period="6mo")

        if hist.empty:
            continue

        # 🔥 ELITE FILTER
        if not is_elite_stock(info, hist):
            continue

        price = hist["Close"].iloc[-1]

        # FUNDAMENTAL
        pe = info.get("trailingPE", 0)
        roe = normalize(info.get("returnOnEquity", 0))
        growth = normalize(info.get("revenueGrowth", 0))
        div = normalize(info.get("dividendYield", 0))
        der = normalize(info.get("debtToEquity", 0))

        # FREE FLOAT
        float_shares = info.get("floatShares", 0)
        shares = info.get("sharesOutstanding", 1)
        ff = normalize_ff(float_shares / shares if shares else 0)

        # TEKNIKAL
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
        der_label = classify_der(der)

        # =========================
        # SCORING
        # =========================
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

        if growth > 0.1 and roe < 0.1:
            labels.append("⚠️ Growth Lemah")
            score -= 1

        if growth < 0:
            labels.append("⚠️ Declining")
            score -= 1

        if 0.03 < div < 0.1:
            score += 1
            labels.append("Dividen")

        if div >= 0.12:
            labels.append("⚠️ Dividend Trap")
            score -= 2

        if ff < 0.2:
            score -= 2
            labels.append("Gorengan")

        # DER
        if der < 0.5:
            score += 1
        elif der > 1.5:
            score -= 2
            labels.append("⚠️ Hutang Tinggi")

        if growth > 0.15 and der > 1.5:
            labels.append("⚠️ Growth Berhutang")
            score -= 1

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
            "der": der,
            "der_label": der_label,
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
# TELEGRAM OUTPUT
# =========================
today = datetime.date.today()

msg = f"🤖 ULTIMATE AI SCREENER PRO (ELITE)\n{today}\n\n"

msg += """==============================
📘 LEGEND
==============================
🟢 Strong Buy  : Layak entry
🟡 Menarik     : Watchlist
⚠️ Spekulatif  : Risiko tinggi
❌ Hindari     : Abaikan

🏦 Bandar      : Akumulasi volume
🚀 Multibagger : Potensi 3–10x

📊 Fundamental:
Value   = PER < 15
Growth  = Revenue naik
Dividen = Stabil 3–10%

📊 DER:
<0.5   = Sehat 💪
0.5-1.5= Normal
>1.5   = Risiko tinggi ⚠️

📊 Free Float:
Low   = Rawan gorengan
High  = Stabil

🎯 ISSI ELITE FILTER:
✔ Market Cap > 1T
✔ Volume aktif
✔ ROE sehat
✔ Bukan gorengan
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
DER : {round(r['der'],2)} ({r['der_label']})
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