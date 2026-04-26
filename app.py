from flask import Flask, render_template, request, Response
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import time, json

app = Flask(__name__)
CORS(app)

class SafeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, np.bool_):    return bool(o)
        if isinstance(o, np.integer):  return int(o)
        if isinstance(o, np.floating): return float(o)
        if isinstance(o, np.ndarray):  return o.tolist()
        return super().default(o)

def jresp(data, status=200):
    return Response(json.dumps(data, cls=SafeEncoder), status=status, mimetype='application/json')

OPTIONS_WATCHLIST = ["SPY","QQQ","AAPL","TSLA","NVDA","AMD","MSFT","AMZN","META","GOOGL","NFLX","COIN","PLTR","MSTR","RIVN","SOFI","HOOD","UPST","RBLX","SNAP"]
PENNY_WATCHLIST   = ["SNDL","CLOV","SPCE","WKHS","CTRM","SHIP","ATER","SENS","BNGO","FFIE","MULN","BIOR","AGRX","HITI","CENN","PHUN","INPX","GFAI","VERB","NLSP"]

_cache = {}; _cache_time = {}; CACHE_TTL = 60

def calc_rsi(s, p=14):
    d=s.diff(); g=d.clip(lower=0); l=-d.clip(upper=0)
    return 100-(100/(1+g.rolling(p).mean()/l.rolling(p).mean().replace(0,np.nan)))

def calc_ema(s, p): return s.ewm(span=p, adjust=False).mean()

def calc_bb(s, p=20, std=2):
    m=s.rolling(p).mean(); sg=s.rolling(p).std(); return m+std*sg, m, m-std*sg

def scan_options(ticker):
    try:
        now=time.time()
        if ticker in _cache and now-_cache_time.get(ticker,0)<CACHE_TTL: return _cache[ticker]
        tk=yf.Ticker(ticker); hist=tk.history(period="5d",interval="5m")
        if hist.empty or len(hist)<50: return None
        c=hist["Close"]; v=hist["Volume"]
        rsi=float(calc_rsi(c).iloc[-1]); ema9=float(calc_ema(c,9).iloc[-1]); ema21=float(calc_ema(c,21).iloc[-1])
        bbu,_,bbl=calc_bb(c); price=float(c.iloc[-1]); prev=float(c.iloc[-2])
        vr=round(float(v.iloc[-1])/max(float(v.rolling(20).mean().iloc[-1]),1),1)
        chg=round((price-prev)/prev*100,2); sig=[]; sc=0
        if ema9>ema21: sig.append("EMA9 > EMA21 - Bullish"); sc+=1
        else: sig.append("EMA9 < EMA21 - Bearish")
        if rsi<35: sig.append(f"RSI Oversold {rsi:.0f}"); sc+=2
        elif rsi>65: sig.append(f"RSI Overbought {rsi:.0f}"); sc+=1
        else: sig.append(f"RSI Neutral {rsi:.0f}"); sc+=1
        if price<float(bbl.iloc[-1]): sig.append("Below BB Lower - bounce watch"); sc+=2
        elif price>float(bbu.iloc[-1]): sig.append("Above BB Upper - overbought"); sc+=1
        if vr>1.5: sig.append(f"Volume spike {vr}x avg"); sc+=1
        try: exps=tk.options; ho=bool(len(exps)>0); ne=str(exps[0]) if exps else "N/A"
        except: ho=False; ne="N/A"
        r={"ticker":str(ticker),"price":round(price,2),"change_pct":float(chg),"rsi":round(rsi,1),
           "ema9":round(ema9,2),"ema21":round(ema21,2),"vol_ratio":float(vr),
           "bb_upper":round(float(bbu.iloc[-1]),2),"bb_lower":round(float(bbl.iloc[-1]),2),
           "score":int(sc),"signals":sig,"direction":"CALL" if ema9>ema21 and rsi<65 else "PUT",
           "has_options":bool(ho),"next_exp":str(ne),"type":"options"}
        _cache[ticker]=r; _cache_time[ticker]=now; return r
    except Exception as e: print(f"[ERR] {ticker}: {e}"); return None

def scan_penny(ticker):
    try:
        now=time.time(); ck=f"p_{ticker}"
        if ck in _cache and now-_cache_time.get(ck,0)<CACHE_TTL: return _cache[ck]
        tk=yf.Ticker(ticker); hist=tk.history(period="5d",interval="15m")
        if hist.empty or len(hist)<20: return None
        c=hist["Close"]; v=hist["Volume"]; price=float(c.iloc[-1])
        if price>5: return None
        rsi=float(calc_rsi(c).iloc[-1]); ema9=float(calc_ema(c,9).iloc[-1]); ema21=float(calc_ema(c,21).iloc[-1])
        vr=round(float(v.iloc[-1])/max(float(v.rolling(20).mean().iloc[-1]),1),1)
        chg=round((price-float(c.iloc[-2]))/float(c.iloc[-2])*100,2)
        try: h1y=tk.history(period="1y"); w52=float(h1y["High"].max()) if not h1y.empty else price
        except: w52=price
        nh=bool(price>=w52*0.95); sig=[]; sc=0
        if vr>2: sig.append(f"Volume {vr}x avg - unusual"); sc+=2
        elif vr>1.5: sig.append(f"Volume {vr}x avg"); sc+=1
        if rsi<35: sig.append(f"RSI Oversold {rsi:.0f}"); sc+=2
        elif rsi>65: sig.append(f"RSI Overbought {rsi:.0f}"); sc+=1
        if ema9>ema21: sig.append("EMA crossover bullish"); sc+=1
        if nh: sig.append("Near 52w high - breakout watch"); sc+=1
        if chg>5: sig.append(f"Up {chg}% today"); sc+=1
        elif chg<-5: sig.append(f"Down {chg}% today - bounce watch"); sc+=1
        r={"ticker":str(ticker),"price":round(price,4),"change_pct":float(chg),"rsi":round(rsi,1),
           "vol_ratio":float(vr),"score":int(sc),"signals":sig,"near_high":bool(nh),
           "week52_hi":round(float(w52),4),"type":"penny"}
        _cache[ck]=r; _cache_time[ck]=now; return r
    except Exception as e: print(f"[ERR penny] {ticker}: {e}"); return None

@app.route("/")
def index(): return render_template("index.html")

@app.route("/api/scan/options")
def api_options():
    res=[r for r in (scan_options(t) for t in OPTIONS_WATCHLIST) if r]
    res.sort(key=lambda x:x["score"],reverse=True)
    return jresp({"results":res,"scanned_at":datetime.now().strftime("%H:%M:%S")})

@app.route("/api/scan/penny")
def api_penny():
    res=[r for r in (scan_penny(t) for t in PENNY_WATCHLIST) if r]
    res.sort(key=lambda x:x["score"],reverse=True)
    return jresp({"results":res,"scanned_at":datetime.now().strftime("%H:%M:%S")})

@app.route("/api/scan/all")
def api_all():
    o=[r for r in (scan_options(t) for t in OPTIONS_WATCHLIST) if r and r["score"]>=3]
    p=[r for r in (scan_penny(t)   for t in PENNY_WATCHLIST)   if r and r["score"]>=3]
    o.sort(key=lambda x:x["score"],reverse=True); p.sort(key=lambda x:x["score"],reverse=True)
    return jresp({"options":o[:10],"penny":p[:10],"scanned_at":datetime.now().strftime("%H:%M:%S")})

@app.route("/api/quote/<ticker>")
def api_quote(ticker):
    r=scan_options(ticker.upper()) or scan_penny(ticker.upper())
    return jresp(r) if r else jresp({"error":f"Could not fetch {ticker}"},404)

@app.route("/api/watchlist", methods=["GET","POST"])
def api_watchlist():
    global OPTIONS_WATCHLIST, PENNY_WATCHLIST
    if request.method=="POST":
        d=request.json
        if "options" in d: OPTIONS_WATCHLIST=d["options"]
        if "penny" in d:   PENNY_WATCHLIST=d["penny"]
        return jresp({"status":"ok"})
    return jresp({"options":OPTIONS_WATCHLIST,"penny":PENNY_WATCHLIST})

if __name__=="__main__":
    import socket
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.connect(("8.8.8.8",80)); ip=s.getsockname()[0]; s.close()
    except: ip="127.0.0.1"
    print(f"\n{'='*50}\n  StockScan Pro running!\n  PC:     http://127.0.0.1:5000\n  iPhone: http://{ip}:5000\n{'='*50}\n")
    app.run(host="0.0.0.0", port=5000, debug=False)