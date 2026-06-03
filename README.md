
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0"/>
<meta name="apple-mobile-web-app-capable" content="yes"/>
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"/>
<meta name="theme-color" content="#080c14"/>
<title>Breakout Scanner</title>
<style>
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
body{background:#080c14;color:#e2e8f0;font-family:'Courier New',monospace;padding:16px;max-width:480px;margin:0 auto;min-height:100vh}
h1{font-size:11px;color:#475569;letter-spacing:0.15em;margin-bottom:16px;margin-top:8px}

/* SEARCH */
#search-row{display:flex;gap:8px;margin-bottom:20px}
#ticker{background:#0d1321;border:1px solid #1e293b;color:#e2e8f0;padding:14px 16px;font-family:inherit;font-size:18px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;border-radius:10px;flex:1;outline:none;-webkit-appearance:none}
#scan-btn{background:#10b981;border:none;color:#000;padding:14px 20px;font-family:inherit;font-size:15px;font-weight:700;border-radius:10px;cursor:pointer;white-space:nowrap;min-width:80px}
#loading{font-size:12px;color:#475569;text-align:center;padding:8px 0}

/* VERDICT */
#verdict{display:none;background:#0d1321;border-radius:12px;padding:16px;margin-bottom:14px;border:1px solid #1e293b}
#v-top{display:flex;align-items:center;gap:10px;margin-bottom:6px}
#v-dot{width:14px;height:14px;border-radius:50%;flex-shrink:0}
#v-ticker{font-size:24px;font-weight:700}
#v-price{font-size:20px;color:#64748b}
#v-badge{font-size:11px;font-weight:700;padding:4px 10px;border-radius:6px;margin-left:auto}
#v-text{font-size:12px;color:#94a3b8;line-height:1.6}

/* SCORE */
#score-box{display:none;background:#0d1321;border-radius:12px;padding:14px;margin-bottom:14px;border:1px solid #1e293b}
#score-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
#score-lbl{font-size:10px;color:#475569;letter-spacing:0.1em}
#score-num{font-size:20px;font-weight:700}
#score-track{height:8px;background:#1e293b;border-radius:4px;overflow:hidden;margin-bottom:10px}
#score-fill{height:100%;border-radius:4px;transition:width 0.5s}
#pills{display:flex;flex-direction:column;gap:5px}
.pill{font-size:11px;padding:5px 10px;border-radius:6px;border:1px solid;display:flex;align-items:center;gap:6px}

/* TRADE CARDS — stacked on mobile */
#trade-grid{display:none;flex-direction:column;gap:12px;margin-bottom:14px}
.trade-card{border-radius:12px;border:1px solid;padding:16px}
.tc-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:4px}
.tc-title{font-size:13px;font-weight:700;letter-spacing:0.06em}
.tc-badge{font-size:10px;font-weight:700;padding:3px 8px;border-radius:5px}
.tc-sub{font-size:11px;color:#475569;margin-bottom:14px}
.level-row{display:flex;justify-content:space-between;align-items:center;background:rgba(0,0,0,0.3);border-radius:8px;padding:12px 14px;margin-bottom:6px}
.level-left{}
.level-label{font-size:10px;letter-spacing:0.08em;opacity:0.55;margin-bottom:2px}
.level-val{font-size:20px;font-weight:700}
.level-right{text-align:right}
.level-pct{font-size:12px;opacity:0.45}
.rr-row{display:flex;align-items:center;gap:8px;background:rgba(0,0,0,0.3);border-radius:8px;padding:10px 14px;margin-top:6px}
.rr-lbl{font-size:10px;opacity:0.45;width:50px;flex-shrink:0}
.rr-track{flex:1;height:5px;background:rgba(255,255,255,0.08);border-radius:3px;overflow:hidden}
.rr-fill{height:100%;border-radius:3px}
.rr-val{font-size:13px;font-weight:700;min-width:44px;text-align:right}
.tc-rule{font-size:11px;line-height:1.6;color:#64748b;border-top:1px solid rgba(255,255,255,0.05);padding-top:12px;margin-top:12px}

/* CHART */
#chart-box{background:#0d1321;border-radius:12px;border:1px solid #1e293b;padding:14px;margin-bottom:14px}
.clbl{font-size:10px;color:#475569;letter-spacing:0.07em;margin-bottom:8px}
canvas{width:100%;height:auto;display:block;border-radius:4px}
#sub-row{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px}

/* CHECKLIST */
#checklist{background:#0d1321;border-radius:12px;border:1px solid #1e293b;padding:14px;margin-bottom:24px}
#cl-title{font-size:10px;color:#475569;letter-spacing:0.1em;margin-bottom:12px}
.ci{display:flex;gap:10px;margin-bottom:12px;align-items:flex-start}
.ci-dot{width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;flex-shrink:0;margin-top:1px}
.ci-name{font-size:12px;font-weight:700;margin-bottom:3px}
.ci-detail{font-size:11px;color:#64748b;line-height:1.5}

/* WATCHLIST */
#watchlist-box{background:#0d1321;border-radius:12px;border:1px solid #1e293b;padding:14px;margin-bottom:24px}
#wl-title{font-size:10px;color:#475569;letter-spacing:0.1em;margin-bottom:10px}
#wl-chips{display:flex;flex-wrap:wrap;gap:8px}
.wl-chip{background:#080c14;border:1px solid #1e293b;border-radius:8px;padding:8px 14px;font-family:inherit;font-size:13px;font-weight:700;color:#94a3b8;cursor:pointer;letter-spacing:0.08em;transition:all 0.15s}
.wl-chip:active{background:#1e293b}
</style>
</head>
<body>
<h1>DAY TRADE &amp; SWING TRADE SCANNER</h1>

<div id="search-row">
  <input type="text" id="ticker" placeholder="TICKER" maxlength="6" autocomplete="off" autocorrect="off" autocapitalize="characters" onkeydown="if(event.key==='Enter'){this.blur();runScan()}"/>
  <button id="scan-btn" onclick="runScan()">SCAN</button>
</div>
<div id="loading"></div>

<!-- WATCHLIST QUICK BUTTONS -->
<div id="watchlist-box">
  <div id="wl-title">YOUR WATCHLIST — TAP TO SCAN</div>
  <div id="wl-chips">
    <button class="wl-chip" onclick="quickScan('NOW')">NOW</button>
    <button class="wl-chip" onclick="quickScan('PLTR')">PLTR</button>
    <button class="wl-chip" onclick="quickScan('MP')">MP</button>
    <button class="wl-chip" onclick="quickScan('USAR')">USAR</button>
    <button class="wl-chip" onclick="quickScan('ASTS')">ASTS</button>
    <button class="wl-chip" onclick="quickScan('SPY')">SPY</button>
    <button class="wl-chip" onclick="quickScan('NVDA')">NVDA</button>
    <button class="wl-chip" onclick="quickScan('TSLA')">TSLA</button>
  </div>
</div>

<div id="verdict">
  <div id="v-top">
    <div id="v-dot"></div>
    <div id="v-ticker"></div>
    <div id="v-price"></div>
    <div id="v-badge"></div>
  </div>
  <div id="v-text"></div>
</div>

<div id="score-box">
  <div id="score-top">
    <div id="score-lbl">SETUP STRENGTH</div>
    <div id="score-num"></div>
  </div>
  <div id="score-track"><div id="score-fill"></div></div>
  <div id="pills"></div>
</div>

<div id="trade-grid">
  <div class="trade-card" id="day-card">
    <div class="tc-top">
      <div class="tc-title">DAY TRADE</div>
      <div class="tc-badge" id="d-badge">IN &amp; OUT TODAY</div>
    </div>
    <div class="tc-sub">Enter near open — exit before market close</div>
    <div class="level-row">
      <div class="level-left"><div class="level-label">ENTRY</div><div class="level-val" id="d-entry" style="color:#10b981">—</div></div>
      <div class="level-right"><div class="level-pct" id="d-entry-note"></div></div>
    </div>
    <div class="level-row">
      <div class="level-left"><div class="level-label">STOP LOSS</div><div class="level-val" id="d-stop" style="color:#ef4444">—</div></div>
      <div class="level-right"><div class="level-pct" id="d-stop-pct"></div></div>
    </div>
    <div class="level-row">
      <div class="level-left"><div class="level-label">TARGET</div><div class="level-val" id="d-target" style="color:#06b6d4">—</div></div>
      <div class="level-right"><div class="level-pct" id="d-target-pct"></div></div>
    </div>
    <div class="rr-row">
      <div class="rr-lbl">R/R</div>
      <div class="rr-track"><div class="rr-fill" id="d-rr-fill"></div></div>
      <div class="rr-val" id="d-rr-val"></div>
    </div>
    <div class="tc-rule" id="d-rule"></div>
  </div>

  <div class="trade-card" id="swing-card">
    <div class="tc-top">
      <div class="tc-title">SWING TRADE</div>
      <div class="tc-badge" style="background:rgba(139,92,246,0.2);color:#a78bfa">HOLD 3–10 DAYS</div>
    </div>
    <div class="tc-sub">Buy today — hold days to weeks for the full move</div>
    <div class="level-row">
      <div class="level-left"><div class="level-label">ENTRY</div><div class="level-val" id="s-entry" style="color:#10b981">—</div></div>
      <div class="level-right"><div class="level-pct" id="s-entry-note"></div></div>
    </div>
    <div class="level-row">
      <div class="level-left"><div class="level-label">STOP LOSS</div><div class="level-val" id="s-stop" style="color:#ef4444">—</div></div>
      <div class="level-right"><div class="level-pct" id="s-stop-pct"></div></div>
    </div>
    <div class="level-row">
      <div class="level-left"><div class="level-label">TARGET</div><div class="level-val" id="s-target" style="color:#06b6d4">—</div></div>
      <div class="level-right"><div class="level-pct" id="s-target-pct"></div></div>
    </div>
    <div class="rr-row">
      <div class="rr-lbl">R/R</div>
      <div class="rr-track"><div class="rr-fill" id="s-rr-fill"></div></div>
      <div class="rr-val" id="s-rr-val"></div>
    </div>
    <div class="tc-rule" id="s-rule"></div>
  </div>
</div>

<div id="chart-box">
  <div class="clbl">PRICE CHART + BOLLINGER BANDS</div>
  <canvas id="main-cv" width="600" height="200"></canvas>
  <div id="sub-row">
    <div><div class="clbl" style="margin-top:8px">RSI (14)</div><canvas id="rsi-cv" width="300" height="70"></canvas></div>
    <div><div class="clbl" style="margin-top:8px">VOLUME</div><canvas id="vol-cv" width="300" height="70"></canvas></div>
  </div>
</div>

<div id="checklist">
  <div id="cl-title">SIGNAL CHECKLIST</div>
  <div id="checklist-items"></div>
</div>

<script>
let candles=[],bbData=[],rsiData=[];

function quickScan(t){
  document.getElementById('ticker').value=t;
  runScan();
  window.scrollTo({top:0,behavior:'smooth'});
}

async function runScan(){
  const ticker=document.getElementById('ticker').value.trim().toUpperCase();
  if(!ticker)return;
  document.getElementById('loading').textContent='Loading '+ticker+'...';
  document.getElementById('verdict').style.display='none';
  document.getElementById('score-box').style.display='none';
  document.getElementById('trade-grid').style.display='none';
  try{
    const url='https://query1.finance.yahoo.com/v8/finance/chart/'+ticker+'?interval=1d&range=6mo';
    const res=await fetch('https://api.allorigins.win/raw?url='+encodeURIComponent(url));
    const json=await res.json();
    const result=json?.chart?.result?.[0];
    if(!result||!result.indicators?.quote?.[0]){document.getElementById('loading').textContent='Not found. Try AAPL, TSLA, SPY';return;}
    const q=result.indicators.quote[0];
    candles=[];
    for(let i=0;i<result.timestamp.length;i++){
      if(q.open[i]!=null&&q.close[i]!=null&&q.high[i]!=null&&q.low[i]!=null&&q.volume[i]!=null)
        candles.push({o:q.open[i],c:q.close[i],h:q.high[i],l:q.low[i],v:q.volume[i]});
    }
    if(candles.length<30){document.getElementById('loading').textContent='Not enough data';return;}
    bbData=computeBB(candles);
    rsiData=computeRSI(candles);
    document.getElementById('loading').textContent='';
    analyze(ticker);
    drawAll();
    setTimeout(()=>document.getElementById('verdict').scrollIntoView({behavior:'smooth'}),100);
  }catch(e){document.getElementById('loading').textContent='Error — try again';}
}

function computeBB(c,p=20){
  return c.map((_,i)=>{
    if(i<p-1)return{mid:null,upper:null,lower:null,bw:null};
    const sl=c.slice(i-p+1,i+1).map(x=>x.c);
    const mean=sl.reduce((a,b)=>a+b,0)/p;
    const std=Math.sqrt(sl.reduce((s,v)=>s+(v-mean)**2,0)/p);
    return{mid:mean,upper:mean+2*std,lower:mean-2*std,bw:std>0?(4*std)/mean:0};
  });
}

function computeRSI(c,p=14){
  const r=new Array(p).fill(null);
  for(let i=p;i<c.length;i++){
    let g=0,l=0;
    for(let j=i-p+1;j<=i;j++){const d=c[j].c-c[j-1].c;if(d>0)g+=d;else l-=d;}
    r.push(100-100/(1+(g/(l||0.0001))));
  }
  return r;
}

function calcATR(idx,period=14){
  const start=Math.max(1,idx-period+1);
  let sum=0,count=0;
  for(let i=start;i<=idx;i++){
    const c=candles[i],p=candles[i-1];
    sum+=Math.max(c.h-c.l,Math.abs(c.h-p.c),Math.abs(c.l-p.c));count++;
  }
  return count>0?sum/count:1;
}

function fmt(n){return'$'+n.toFixed(2);}
function pct(a,b){return((b-a)/Math.abs(a)*100).toFixed(1)+'%';}

function analyze(ticker){
  const n=candles.length;
  const last=candles[n-1];
  const atr=calcATR(n-1,14);
  const atrDay=atr*0.5;
  const bwNow=bbData[n-1].bw||0;
  const bwSlice=bbData.slice(Math.max(0,n-20),n-1).filter(b=>b.bw!=null);
  const bwAvg=bwSlice.length?bwSlice.reduce((s,b)=>s+b.bw,0)/bwSlice.length:bwNow;
  const squeeze=bwNow<bwAvg*0.75;
  const rsiNow=rsiData[n-1]||50;
  const rsi10=rsiData[n-10]||50;
  const rsiRising=rsiNow>rsi10;
  const rsiGood=rsiRising&&rsiNow>42&&rsiNow<72;
  const rsiOB=rsiNow>=72;
  const avgVol=candles.slice(0,Math.min(40,n)).reduce((s,c)=>s+c.v,0)/Math.min(40,n);
  const recentVol=candles.slice(n-5,n).reduce((s,c)=>s+c.v,0)/5;
  const volUp=recentVol>avgVol*1.2;
  const volRatio=recentVol/avgVol;
  const aboveMid=!!(bbData[n-1].mid&&last.c>bbData[n-1].mid);
  const lows=[candles[n-1].l,candles[n-5].l,candles[n-10].l];
  const higherLows=lows[0]>lows[1]&&lows[1]>lows[2];
  let score=0;
  if(squeeze)score+=20;if(rsiGood)score+=25;if(volUp)score+=20;if(aboveMid)score+=20;if(higherLows)score+=15;
  let color,label,summary;
  if(score>=70){color='#10b981';label='STRONG ✓';summary='Strong setup. Signals aligned. Good for a day trade today and a swing trade this week.';}
  else if(score>=45){color='#f59e0b';label='DEVELOPING';summary='Developing setup. Day trade with caution. For swing trade wait 1-2 more days for confirmation.';}
  else{color='#ef4444';label='WAIT ✗';summary='Signals not aligned. Not a good time to enter. Check back in a few days.';}

  document.getElementById('verdict').style.display='block';
  document.getElementById('v-dot').style.cssText='background:'+color+';box-shadow:0 0 8px '+color+';width:14px;height:14px;border-radius:50%;flex-shrink:0';
  document.getElementById('v-ticker').textContent=ticker;
  document.getElementById('v-ticker').style.color=color;
  document.getElementById('v-price').textContent='$'+last.c.toFixed(2);
  const badge=document.getElementById('v-badge');
  badge.textContent=label;badge.style.background=color+'22';badge.style.color=color;
  document.getElementById('v-text').textContent=summary;

  document.getElementById('score-box').style.display='block';
  document.getElementById('score-num').textContent=score+'/100';
  document.getElementById('score-num').style.color=color;
  document.getElementById('score-fill').style.cssText='width:'+score+'%;background:'+color;
  const pillsEl=document.getElementById('pills');
  pillsEl.innerHTML='';
  [{label:'BB Squeeze',pass:squeeze,val:squeeze?'Coiling':'Bands wide'},
   {label:'RSI',pass:rsiGood,val:'RSI '+Math.round(rsiNow)+(rsiOB?' — overbought':'')},
   {label:'Volume',pass:volUp,val:'×'+volRatio.toFixed(1)+' avg'},
   {label:'Above Midline',pass:aboveMid,val:aboveMid?'Yes':'No'},
   {label:'Higher Lows',pass:higherLows,val:higherLows?'Yes':'No'},
  ].forEach(p=>{
    const el=document.createElement('div');
    const c=p.pass?color:'#475569';
    el.className='pill';
    el.style.cssText='color:'+c+';border-color:'+c+'44;background:'+c+'11';
    el.innerHTML='<span style="font-size:13px">'+(p.pass?'✓':'✗')+'</span><span>'+p.label+' — '+p.val+'</span>';
    pillsEl.appendChild(el);
  });

  document.getElementById('trade-grid').style.display='flex';
  const dc=document.getElementById('day-card');
  dc.style.cssText='border-radius:12px;border:1px solid '+color+'44;padding:16px;background:'+color+'08';
  document.getElementById('d-badge').style.cssText='font-size:10px;font-weight:700;padding:3px 8px;border-radius:5px;background:'+color+'22;color:'+color;
  const dEntry=last.c+atrDay*0.08,dStop=last.l-atrDay*0.5,dTarget=dEntry+(dEntry-dStop)*1.5;
  document.getElementById('d-entry').textContent=fmt(dEntry);
  document.getElementById('d-entry-note').textContent='Buy near open';
  document.getElementById('d-stop').textContent=fmt(dStop);
  document.getElementById('d-stop-pct').textContent=pct(dEntry,dStop)+' risk';
  document.getElementById('d-target').textContent=fmt(dTarget);
  document.getElementById('d-target-pct').textContent='+'+pct(dEntry,dTarget)+' gain';
  document.getElementById('d-rr-fill').style.cssText='width:50%;background:'+color+';height:100%;border-radius:3px';
  document.getElementById('d-rr-val').style.color=color;
  document.getElementById('d-rr-val').textContent='1.5:1';
  document.getElementById('d-rule').textContent='Buy near $'+dEntry.toFixed(2)+' at open. If it drops to $'+dStop.toFixed(2)+' — sell immediately. If it hits $'+dTarget.toFixed(2)+' — take profit. Exit before 4pm no matter what.';

  const sEntry=last.c+atr*0.05,sStop=last.l-atr*0.6,sTarget=sEntry+(sEntry-sStop)*2.5;
  document.getElementById('s-entry').textContent=fmt(sEntry);
  document.getElementById('s-entry-note').textContent='Buy today or tomorrow';
  document.getElementById('s-stop').textContent=fmt(sStop);
  document.getElementById('s-stop-pct').textContent=pct(sEntry,sStop)+' risk';
  document.getElementById('s-target').textContent=fmt(sTarget);
  document.getElementById('s-target-pct').textContent='+'+pct(sEntry,sTarget)+' gain';
  document.getElementById('s-rr-fill').style.cssText='width:67%;background:#a78bfa;height:100%;border-radius:3px';
  document.getElementById('s-rr-val').style.color='#a78bfa';
  document.getElementById('s-rr-val').textContent='2.5:1';
  document.getElementById('s-rule').textContent='Buy at $'+sEntry.toFixed(2)+'. Set stop alert at $'+sStop.toFixed(2)+'. Hold until $'+sTarget.toFixed(2)+' or 10 days — whichever comes first.';

  const clEl=document.getElementById('checklist-items');
  clEl.innerHTML='';
  [{name:'BB Squeeze',pass:squeeze,detail:squeeze?'Bands tightening — volatility coiling before a move.':'Bands still wide. Wait for them to tighten.'},
   {name:'RSI Momentum',pass:rsiGood,detail:rsiGood?'RSI at '+Math.round(rsiNow)+' — rising, not overbought. Ideal zone.':rsiOB?'RSI at '+Math.round(rsiNow)+' — overbought. May pull back first.':'RSI needs to build above 45.'},
   {name:'Volume',pass:volUp,detail:volUp?'Volume '+volRatio.toFixed(1)+'x average — buyers stepping in.':'Volume below average. Wait for volume to pick up.'},
   {name:'Above Midline',pass:aboveMid,detail:aboveMid?'Holding above the BB midline — bulls in control.':'Below midline — wait for price to reclaim it.'},
   {name:'Higher Lows',pass:higherLows,detail:higherLows?'Each dip holds higher — healthy uptrend base.':'No higher lows yet — base still forming.'},
  ].forEach(item=>{
    const div=document.createElement('div');
    div.className='ci';
    const ic=item.pass?color:'#475569';
    div.innerHTML='<div class="ci-dot" style="background:'+ic+'22;color:'+ic+'">'+(item.pass?'✓':'✗')+'</div><div><div class="ci-name" style="color:'+(item.pass?'#e2e8f0':'#64748b')+'">'+item.name+'</div><div class="ci-detail">'+item.detail+'</div></div>';
    clEl.appendChild(div);
  });
}

function drawAll(){drawMain();drawRSI();drawVol();}
function drawMain(){
  const cv=document.getElementById('main-cv');
  const ctx=cv.getContext('2d');
  const W=cv.width,H=cv.height;
  ctx.clearRect(0,0,W,H);
  const pad={l:46,r:8,t:8,b:16};
  const cw=W-pad.l-pad.r,ch=H-pad.t-pad.b;
  const n=candles.length,cw2=cw/n;
  const all=[...candles.flatMap(c=>[c.h,c.l]),...bbData.flatMap(b=>b.upper?[b.upper,b.lower]:[])];
  const minP=Math.min(...all)*0.997,maxP=Math.max(...all)*1.003;
  const toY=p=>pad.t+ch-((p-minP)/(maxP-minP))*ch;
  const toX=i=>pad.l+i*cw2+cw2*0.5;
  for(let g=0;g<=3;g++){
    const y=pad.t+(g/3)*ch;
    ctx.strokeStyle='rgba(255,255,255,0.04)';ctx.lineWidth=1;
    ctx.beginPath();ctx.moveTo(pad.l,y);ctx.lineTo(W-pad.r,y);ctx.stroke();
    ctx.fillStyle='rgba(148,163,184,0.4)';ctx.font='9px monospace';ctx.textAlign='right';
    ctx.fillText((maxP-(g/3)*(maxP-minP)).toFixed(0),pad.l-2,y+3);
  }
  let s=false;
  ctx.beginPath();
  for(let i=0;i<n;i++){if(!bbData[i].upper)continue;s?ctx.lineTo(toX(i),toY(bbData[i].upper)):(ctx.moveTo(toX(i),toY(bbData[i].upper)),s=true);}
  for(let i=n-1;i>=0;i--){if(!bbData[i].lower)continue;ctx.lineTo(toX(i),toY(bbData[i].lower));}
  ctx.closePath();ctx.fillStyle='rgba(139,92,246,0.06)';ctx.fill();
  s=false;ctx.beginPath();
  bbData.forEach((b,i)=>{if(!b.upper)return;s?ctx.lineTo(toX(i),toY(b.upper)):(ctx.moveTo(toX(i),toY(b.upper)),s=true);});
  ctx.strokeStyle='rgba(139,92,246,0.5)';ctx.lineWidth=1;ctx.stroke();
  s=false;ctx.beginPath();
  bbData.forEach((b,i)=>{if(!b.lower)return;s?ctx.lineTo(toX(i),toY(b.lower)):(ctx.moveTo(toX(i),toY(b.lower)),s=true);});
  ctx.strokeStyle='rgba(139,92,246,0.5)';ctx.lineWidth=1;ctx.stroke();
  s=false;ctx.beginPath();
  bbData.forEach((b,i)=>{if(!b.mid)return;s?ctx.lineTo(toX(i),toY(b.mid)):(ctx.moveTo(toX(i),toY(b.mid)),s=true);});
  ctx.strokeStyle='rgba(139,92,246,0.2)';ctx.lineWidth=1;ctx.setLineDash([3,3]);ctx.stroke();ctx.setLineDash([]);
  candles.forEach((c,i)=>{
    const x=toX(i),bull=c.c>=c.o;
    const bt=toY(Math.max(c.o,c.c)),bb2=toY(Math.min(c.o,c.c));
    const bh=Math.max(1,bb2-bt),bw=Math.max(1,cw2*0.6);
    ctx.strokeStyle=bull?'#10b981':'#ef4444';ctx.lineWidth=0.8;
    ctx.beginPath();ctx.moveTo(x,toY(c.h));ctx.lineTo(x,toY(c.l));ctx.stroke();
    ctx.fillStyle=bull?'rgba(16,185,129,0.85)':'rgba(239,68,68,0.85)';
    ctx.fillRect(x-bw/2,bt,bw,bh);
  });
}
function drawRSI(){
  const cv=document.getElementById('rsi-cv');
  const ctx=cv.getContext('2d');
  const W=cv.width,H=cv.height;ctx.clearRect(0,0,W,H);
  const pad={l:22,r:4,t:4,b:10};
  const cw=W-pad.l-pad.r,ch=H-pad.t-pad.b;
  const n=rsiData.length,cw2=cw/n;
  const toY=v=>pad.t+ch-(v/100)*ch;
  const toX=i=>pad.l+i*cw2+cw2*0.5;
  [30,70].forEach(lv=>{
    ctx.strokeStyle=lv===70?'rgba(239,68,68,0.12)':'rgba(16,185,129,0.12)';ctx.lineWidth=1;
    ctx.beginPath();ctx.moveTo(pad.l,toY(lv));ctx.lineTo(W-pad.r,toY(lv));ctx.stroke();
    ctx.fillStyle='rgba(148,163,184,0.3)';ctx.font='8px monospace';ctx.textAlign='right';
    ctx.fillText(lv,pad.l-1,toY(lv)+3);
  });
  ctx.beginPath();let s=false;
  rsiData.forEach((v,i)=>{if(v===null)return;s?ctx.lineTo(toX(i),toY(v)):(ctx.moveTo(toX(i),toY(v)),s=true);});
  ctx.strokeStyle='#f59e0b';ctx.lineWidth=1.5;ctx.stroke();
}
function drawVol(){
  const cv=document.getElementById('vol-cv');
  const ctx=cv.getContext('2d');
  const W=cv.width,H=cv.height;ctx.clearRect(0,0,W,H);
  const pad={l:4,r:4,t:4,b:10};
  const cw=W-pad.l-pad.r,ch=H-pad.t-pad.b;
  const n=candles.length,cw2=cw/n;
  const maxV=Math.max(...candles.map(c=>c.v));
  const avgV=candles.slice(0,Math.min(40,n)).reduce((s,c)=>s+c.v,0)/Math.min(40,n);
  const avgY=pad.t+ch-(avgV/maxV)*ch;
  ctx.beginPath();ctx.moveTo(pad.l,avgY);ctx.lineTo(W-pad.r,avgY);
  ctx.strokeStyle='rgba(255,255,255,0.15)';ctx.lineWidth=1;ctx.setLineDash([2,2]);ctx.stroke();ctx.setLineDash([]);
  candles.forEach((c,i)=>{
    const bw=Math.max(1,cw2*0.7);
    const x=pad.l+i*cw2+(cw2-bw)/2;
    const barH=Math.max(1,(c.v/maxV)*ch);
    const rec=i>=n-5;
    ctx.fillStyle=c.c>=c.o?(rec?'rgba(16,185,129,0.95)':'rgba(16,185,129,0.4)'):(rec?'rgba(239,68,68,0.95)':'rgba(239,68,68,0.4)');
    ctx.fillRect(x,pad.t+ch-barH,bw,barH);
  });
}
</script>
</body>
</html>
