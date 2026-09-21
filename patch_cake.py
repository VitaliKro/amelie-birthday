from pathlib import Path
import re

p = Path("index.html")
html = p.read_text(encoding="utf-8")

# Make top candle card call the dedicated animation.
html = html.replace('onclick="toggleCandles()"', 'onclick="openCandles()"', 1)

# Replace the old emoji cake CSS with photo + candle animation CSS.
html = re.sub(
    r'\.cake\{font-size:4\.5rem;position:relative;display:flex;flex-direction:column;align-items:center;gap:8px\}\n\.candle-row\{display:grid;grid-template-columns:repeat\(7,1fr\);gap:2px;justify-items:center;max-width:220px;margin:0 auto 2px\}\n\.candle\{font-size:1\.15rem;display:inline-block;transition:\.25s;filter:drop-shadow\(0 0 8px #ffcc6b\)\}\n\.off \.candle\{opacity:\.08;transform:scale\(\.55\)\}\n\.cake-main\{line-height:1\}',
    '''.cake-scene{position:relative;width:min(230px,90%);margin:0 auto 10px}
.cake-photo{display:block;width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:24px;box-shadow:0 18px 34px rgba(62,35,92,.22);border:4px solid rgba(255,255,255,.9)}
.candle-stage{position:absolute;left:50%;top:12px;transform:translateX(-50%);width:84%;display:grid;grid-template-columns:repeat(7,1fr);grid-auto-rows:38px;justify-items:center;align-items:end;pointer-events:none}
.candle-stage .candle-unit:nth-child(n+8){transform:translateX(10px)}
.candle-unit{position:relative;width:18px;height:34px;opacity:.98}
.candle-unit img{width:100%;height:100%;object-fit:contain;display:block;clip-path:inset(9px 0 0 0);transform:translateY(9px) scale(.94);filter:saturate(.75) brightness(.95) drop-shadow(0 2px 2px rgba(0,0,0,.12));transition:.35s ease}
.candle-unit .smoke{position:absolute;left:50%;top:-5px;width:7px;height:16px;border-radius:50%;background:rgba(140,130,150,.35);filter:blur(3px);opacity:0;transform:translateX(-50%) scale(.5)}
#cakeBox.lit .candle-unit img{clip-path:inset(0);transform:translateY(0) scale(1);filter:drop-shadow(0 0 7px rgba(255,187,74,.8)) drop-shadow(0 2px 2px rgba(0,0,0,.12));animation:flicker 1.15s ease-in-out infinite}
#cakeBox.lit .candle-unit{animation:ignite .52s ease both}
#cakeBox.lit .candle-unit:nth-child(1){animation-delay:.00s}#cakeBox.lit .candle-unit:nth-child(2){animation-delay:.05s}#cakeBox.lit .candle-unit:nth-child(3){animation-delay:.10s}#cakeBox.lit .candle-unit:nth-child(4){animation-delay:.15s}#cakeBox.lit .candle-unit:nth-child(5){animation-delay:.20s}#cakeBox.lit .candle-unit:nth-child(6){animation-delay:.25s}#cakeBox.lit .candle-unit:nth-child(7){animation-delay:.30s}#cakeBox.lit .candle-unit:nth-child(8){animation-delay:.35s}#cakeBox.lit .candle-unit:nth-child(9){animation-delay:.40s}#cakeBox.lit .candle-unit:nth-child(10){animation-delay:.45s}#cakeBox.lit .candle-unit:nth-child(11){animation-delay:.50s}#cakeBox.lit .candle-unit:nth-child(12){animation-delay:.55s}#cakeBox.lit .candle-unit:nth-child(13){animation-delay:.60s}
#cakeBox.just-blown .smoke{animation:smoke 1.1s ease-out both}
#cakeBox.lit .cake-scene:after{content:"";position:absolute;inset:-8px;border-radius:28px;background:radial-gradient(circle at 50% 16%,rgba(255,215,125,.32),rgba(255,184,84,.10) 46%,transparent 70%);pointer-events:none;animation:glow 1.5s ease-in-out infinite}
@keyframes ignite{0%{transform:translateY(8px) scale(.85);opacity:.25}65%{transform:translateY(-2px) scale(1.05);opacity:1}100%{transform:translateY(0) scale(1);opacity:1}}
@keyframes flicker{0%,100%{transform:translateY(0) scale(1) rotate(-2deg)}25%{transform:translateY(-1px) scale(1.04,.97) rotate(2deg)}50%{transform:translateY(0) scale(.97,1.06) rotate(-3deg)}75%{transform:translateY(-1px) scale(1.02,.98) rotate(2deg)}}
@keyframes smoke{0%{opacity:.55;transform:translateX(-50%) translateY(0) scale(.6)}100%{opacity:0;transform:translateX(-50%) translateY(-28px) scale(1.25)}}
@keyframes glow{0%,100%{opacity:.72}50%{opacity:1}}''',
    html,
    count=1
)

# Replace the cake markup.
old = re.search(r'<div class="surprise" id="cakeBox">.*?</div>\s*\n\s*<div class="surprise" id="giftBox">', html, re.S)
if not old:
    raise SystemExit("cake block not found")

candle_url = "https://commons.wikimedia.org/wiki/Special:FilePath/Emoji_u1f56f.svg"
cake_url = "https://commons.wikimedia.org/wiki/Special:FilePath/Takano%27s%20strawberry%20shortcake.jpg"
candles = ''.join(f'<span class="candle-unit"><img src="{candle_url}" alt=""><i class="smoke"></i></span>' for _ in range(13))
cake_block = f'''<div class="surprise" id="cakeBox">
     <div class="cake-scene" id="cakeDisplay">
       <img class="cake-photo" src="{cake_url}" alt="Japanische Erdbeer-Geburtstagstorte">
       <div class="candle-stage">{candles}</div>
     </div>
     <h3>Geburtstagskuchen</h3>
     <p id="cakeText">Klicke und zünde 13 Kerzen an.</p>
     <button class="cta" id="cakeButton" onclick="toggleCandles()">Kerzen anzünden</button>
   </div>

   <div class="surprise" id="giftBox">'''
html = html[:old.start()] + cake_block + html[old.end():]

html = html.replace("let candlesOn = true;", "let candlesOn = false;")

html = re.sub(
    r'function toggleCandles\(\)\{.*?\n\}',
    '''function setCandles(on){
  const box=document.getElementById('cakeBox');
  const txt=document.getElementById('cakeText');
  const btn=document.getElementById('cakeButton');
  if(!box) return;
  box.classList.remove('just-blown');
  if(on){
    box.classList.add('lit');
    if(txt) txt.textContent='13 Kerzen brennen jetzt für Amelie.';
    if(btn) btn.textContent='Kerzen auspusten';
    confetti();
  }else{
    box.classList.remove('lit');
    box.classList.add('just-blown');
    if(txt) txt.textContent='Psst … Wunsch gemacht?';
    if(btn) btn.textContent='Kerzen anzünden';
    setTimeout(()=>box.classList.remove('just-blown'),1150);
  }
}
function toggleCandles(){
  const target=document.getElementById('cakeBox');
  centerScrollTo(target);
  setTimeout(()=>{candlesOn=!candlesOn;setCandles(candlesOn);effectAt(target)},420);
}
function openCandles(){
  const target=document.getElementById('cakeBox');
  centerScrollTo(target);
  setTimeout(()=>{if(!candlesOn){candlesOn=true;setCandles(true)}else{effectAt(target)}},420);
}''',
    html,
    count=1,
    flags=re.S
)

p.write_text(html, encoding="utf-8")
