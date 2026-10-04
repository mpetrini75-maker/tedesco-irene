r"""Genera le pagine -allenamento di Tedesco di Irene da un unico modello (copiato da Geografia).
Le domande stanno qui sotto (prima opzione = quella giusta: l'app le mescola).
Uso:  py strumenti\genera-allenamenti.py
"""
import json
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent

MODELLO = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#FAF6EE">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Tedesco di Irene">
<script src="alert.js"></script>
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
<title>__TITOLO__ — Allenamento</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lexend:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:#FAF6EE; --card:#FFFFFF; --ink:#2F2A24;
    --accent:#A8402E; --accent-soft:#F6E3DC;
    --green:#3E8E5A; --green-soft:#E2F0E6;
    --red:#C2492F; --red-soft:#F6E1DB;
    --blue:#3B6EA5; --blue-soft:#E2ECF5;
  }
  *{box-sizing:border-box;}
  body{margin:0; font-family:"Lexend","Trebuchet MS",Verdana,sans-serif;
    background:var(--bg); color:var(--ink); line-height:1.7; letter-spacing:0.3px; padding:24px 14px 60px;}
  .wrap{max-width:620px;margin:0 auto;}
  .back{display:inline-block;background:var(--accent-soft);color:var(--accent);text-decoration:none;border-radius:12px;padding:8px 16px;font-size:0.98rem;font-weight:bold;margin:0 8px 14px 0;}
  h1{color:var(--accent);font-size:1.6rem;text-align:center;margin:0 0 6px;}
  .sub{text-align:center;color:#8a7f70;margin:0 0 26px;font-size:1rem;}
  .card{background:var(--card);border-radius:18px;padding:22px 20px;margin-bottom:22px;
    box-shadow:0 4px 14px rgba(0,0,0,0.06);border:1px solid #efe7da;}
  .card h2{margin:0 0 10px;font-size:1.25rem;color:var(--accent);}
  .card .lead{color:#8a7f70;margin:0 0 12px;font-size:0.97rem;}
  .levelbar{margin:0 0 12px;}
  .lvrow{display:flex;align-items:center;gap:10px;flex-wrap:wrap;font-size:0.98rem;color:var(--accent);}
  .lvdots{display:inline-flex;gap:6px;}
  .lvdot{width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;
    background:var(--bg);border:2px solid var(--accent-soft);color:#b9ad9c;font-size:0.85rem;font-weight:bold;}
  .lvdot.on{background:var(--accent-soft);border-color:var(--accent);color:var(--accent);}
  .ex{margin:14px 0;}
  .qnum{font-weight:bold;color:var(--accent);}
  .qtext{font-size:1.1rem;margin:6px 0 8px;}
  .options{display:flex;flex-direction:column;gap:10px;}
  .opt{background:var(--bg);border:2px solid var(--accent-soft);
    border-radius:12px;padding:13px 14px;font-size:1.05rem;cursor:pointer;
    text-align:left;font-family:inherit;color:var(--ink);transition:all .15s;}
  .opt:hover{border-color:var(--accent);}
  .opt.correct{background:var(--green-soft);border-color:var(--green);color:var(--green);font-weight:bold;}
  .opt.wrong{background:var(--red-soft);border-color:var(--red);color:var(--red);}
  .feedback{margin-top:10px;font-size:1.02rem;font-weight:bold;min-height:24px;}
  .feedback.ok{color:var(--green);}
  .feedback.no{color:var(--red);}
  .progress{text-align:center;font-size:1.05rem;margin:12px 0 0;color:#8a7f70;}
  .star{font-size:1.4rem;}
  .match-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:6px;}
  .match-col{display:flex;flex-direction:column;gap:10px;}
  .match-btn{background:var(--bg);border:2px solid var(--accent-soft);border-radius:12px;
    padding:12px;font-size:0.98rem;cursor:pointer;font-family:inherit;color:var(--ink);
    display:flex;align-items:center;justify-content:center;text-align:center;gap:6px;transition:all .15s;}
  .match-btn:hover{border-color:var(--accent);}
  .match-btn.sel{border-color:var(--blue);background:var(--blue-soft);color:var(--blue);font-weight:bold;}
  .match-btn.done{background:var(--green-soft);border-color:var(--green);color:var(--green);font-weight:bold;cursor:default;opacity:0.85;}
  .match-btn.flash{border-color:var(--red);background:var(--red-soft);}
  .restart{display:inline-block;margin:12px auto 0;background:var(--accent);color:#fff;border:none;
    border-radius:12px;padding:11px 22px;font-size:1rem;cursor:pointer;font-family:inherit;}
</style>
</head>
<body>
<div class="wrap">
  <a class="back" href="index.html">&larr; Indice</a><a class="back" href="__LEZIONE__.html">📖 Ripassa la lezione</a>
  <h1>🏋️ __TITOLO__ — Allenamento</h1>
  <p class="sub">Mattoncino __NUM__ · 3 sezioni · 3 livelli ciascuna 💪</p>

  <div class="card">
    <h2>🧠 1. Domande</h2>
    <p class="lead">Scegli la risposta giusta. Puoi riprovare finché non la trovi!</p>
    <div class="levelbar" id="quiz-level"></div>
    <div id="quiz-box"></div>
    <div class="progress" id="quiz-prog"></div>
  </div>

  <div class="card">
    <h2>✅ 2. Vero o falso</h2>
    <p class="lead">Leggi la frase e tocca Vero o Falso. Dopo ti dico perché.</p>
    <div class="levelbar" id="vf-level"></div>
    <div id="vf-box"></div>
    <div class="progress" id="vf-prog"></div>
  </div>

  <div class="card">
    <h2>🔗 3. Abbina</h2>
    <p class="lead">Tocca una casella a sinistra, poi la sua coppia a destra. Collega tutte le coppie!</p>
    <div class="levelbar" id="abbina-level"></div>
    <div class="match-grid" id="abbina-grid"></div>
    <div class="progress" id="abbina-prog"></div>
  </div>
</div>
<script>
window.ALLENAMENTO = __DATI__;
</script>
<script src="allenamento.js"></script>
<script>
  if ('serviceWorker' in navigator) { navigator.serviceWorker.register('./service-worker.js'); }
</script>
</body>
</html>
"""


def Q(q, *opts):
    return {"q": q, "opts": list(opts)}


def V(q, v, perche):
    return {"q": q, "v": v, "perche": perche}


def A(*coppie):
    return [{"l": l, "r": r} for l, r in coppie]


MATTONCINI = {
    "schulalltag": {
        "num": 1, "titolo": "Schulalltag: la vita a scuola",
        "quiz": [
            [Q("Come si dice \"storia\" in tedesco?", "Geschichte", "Geografie", "Kunst"),
             Q("Come si dice \"arte\"?", "Kunst", "Musik", "Sport"),
             Q("Mathe è…", "matematica", "musica", "inglese"),
             Q("Le materie in tedesco si usano…", "senza articolo", "sempre con der", "sempre con die"),
             Q("Was ist dein Lieblingsfach? vuol dire…", "Qual è la tua materia preferita?", "Che ore sono?", "Come vai a scuola?")],
            [Q("Mittwoch è…", "mercoledì", "lunedì", "domenica"),
             Q("Lunedì si dice…", "Montag", "Mittwoch", "Freitag"),
             Q("Lunedì ho tedesco:", "Am Montag habe ich Deutsch.", "Im Montag habe ich Deutsch.", "Mit Montag habe ich Deutsch."),
             Q("Lo Stundenplan è…", "l'orario delle lezioni", "la mensa", "il fine settimana"),
             Q("die Pause è…", "l'intervallo", "la prima ora", "la palestra")],
            [Q("Vado in autobus:", "Ich fahre mit dem Bus.", "Ich fahre mit der Bus.", "Ich fahre zu Bus."),
             Q("Vado in metro (die U-Bahn):", "Ich fahre mit der U-Bahn.", "Ich fahre mit dem U-Bahn.", "Ich gehe zu U-Bahn."),
             Q("Vado a piedi:", "Ich gehe zu Fuß.", "Ich fahre mit dem Fuß.", "Ich gehe mit Fuß."),
             Q("Dopo mit, das Fahrrad diventa…", "mit dem Fahrrad", "mit der Fahrrad", "mit das Fahrrad"),
             Q("Es gibt vuol dire…", "c'è, ci sono", "io vado", "mi piace")],
        ],
        "vf": [
            [V("Geschichte vuol dire storia.", True, "E Geografie vuol dire geografia."),
             V("Kunst vuol dire musica.", False, "Kunst è arte; musica è Musik."),
             V("Davanti alle materie si mette der.", False, "Le materie si usano senza articolo."),
             V("Lieblingsfach vuol dire materia preferita.", True, "Lieblings- vuol dire preferito."),
             V("Ich finde Mathe einfach vuol dire: trovo matematica facile.", True, "einfach = facile.")],
            [V("I giorni della settimana sono maschili.", True, "Per questo si dice am Montag."),
             V("Sonntag è sabato.", False, "Sonntag è domenica; sabato è Samstag."),
             V("Mittwoch viene da metà settimana.", True, "Mitte + Woche."),
             V("die erste Stunde è la prima ora.", True, "die zweite Stunde è la seconda."),
             V("das Wochenende è il lunedì.", False, "È il fine settimana.")],
            [V("Dopo mit si usa il dativo.", True, "der e das diventano dem, die diventa der."),
             V("Si dice mit der Bus.", False, "der Bus è maschile: mit dem Bus."),
             V("A piedi si dice zu Fuß.", True, "E si usa gehen, non fahren."),
             V("Con un mezzo si usa fahren.", True, "Ich fahre mit dem Zug."),
             V("Dopo es gibt, ein diventa einen al maschile.", True, "Es gibt einen Computerraum.")],
        ],
        "abbina": [
            A(("Deutsch", "tedesco"), ("Englisch", "inglese"), ("Geschichte", "storia"),
              ("Kunst", "arte 🎨"), ("Mathe", "matematica")),
            A(("Montag", "lunedì"), ("Mittwoch", "mercoledì"), ("Freitag", "venerdì"),
              ("Sonntag", "domenica"), ("Stundenplan", "orario 🗓️")),
            A(("der Bus", "mit dem Bus 🚌"), ("die U-Bahn", "mit der U-Bahn 🚇"), ("das Fahrrad", "mit dem Fahrrad 🚲"),
              ("a piedi", "zu Fuß 🚶"), ("es gibt", "c'è, ci sono")),
        ],
    },
}

for slug, m in MATTONCINI.items():
    dati = {k: m[k] for k in ("quiz", "vf", "abbina")}
    for k, livelli in dati.items():
        assert len(livelli) == 3 and all(len(x) == 5 for x in livelli), (slug, k)
    html = (MODELLO.replace("__TITOLO__", m["titolo"]).replace("__NUM__", str(m["num"]))
            .replace("__LEZIONE__", slug).replace("__DATI__", json.dumps(dati, ensure_ascii=False)))
    (RADICE / f"{slug}-allenamento.html").write_text(html, encoding="utf-8")
    print("scritto", f"{slug}-allenamento.html")
