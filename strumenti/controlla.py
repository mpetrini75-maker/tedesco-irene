r"""Cancello di collaudo dell'app Tedesco di Irene (copiato da Geografia).
Controlla: ogni file citato nelle pagine esiste; ogni immagine e' usata; il service worker
elenca tutti i file e nessuno che manchi. Uscita 0 = tutto a posto.
Uso:  py strumenti\controlla.py
"""
import re, sys
from pathlib import Path

R = Path(__file__).resolve().parent.parent
errori = []
pagine = sorted(R.glob("*.html"))
citati = set()
for p in pagine:
    t = p.read_text(encoding="utf-8")
    for ref in re.findall(r'(?:src|href)="([^"#:]+)"', t):
        if ref.startswith(("http", "mailto")):
            continue
        citati.add(ref)
        if not (R / ref).exists():
            errori.append(f"{p.name}: manca {ref}")

immagini = {f.relative_to(R).as_posix() for f in (R / "img").rglob("*") if f.is_file()} if (R / "img").exists() else set()
for i in sorted(immagini - citati):
    errori.append(f"immagine non usata: {i}")

sw = (R / "service-worker.js").read_text(encoding="utf-8")
in_sw = set(re.findall(r"'\./([^']+)'", sw))
for f in in_sw:
    if not (R / f).exists():
        errori.append(f"service-worker: elenca {f} che non esiste")
servono = {p.name for p in pagine} | immagini | {"style.css", "app.js", "alert.js", "allenamento.js", "manifest.json",
                                                  "icon-180.png", "icon-192.png", "icon-512.png"}
for f in sorted(servono - in_sw):
    errori.append(f"service-worker: manca {f}")

# ogni riquadro con titolo (tranne data-no-voce) delle lezioni deve avere la sua registrazione
n_audio = 0
for slug in ("schulalltag", "interrogazione"):
    t = (R / f"{slug}.html").read_text(encoding="utf-8")
    cards = re.findall(r'<div class="card"( data-no-voce)?>\s*<h2>', t)
    for n, (novoce,) in enumerate([(c,) for c in cards]):
        if novoce:
            continue
        n_audio += 1
        f = R / "audio" / f"{slug}-{n}.mp3"
        if not f.exists():
            errori.append(f"manca audio/{slug}-{n}.mp3 (rilancia strumenti/genera-audio.py)")
        elif f.stat().st_size < 2000:
            # 10/10/2026: un 403 del servizio voci aveva lasciato un mp3 da 0 byte e questo controllo
            # lo dava per buono. Un riquadro registrato pesa sempre decine di KB.
            errori.append(f"audio/{slug}-{n}.mp3 vuoto o rotto ({f.stat().st_size} byte): rilancia strumenti/genera-audio.py")

# 17/10/2026: l'allenamento in coppia ha due registrazioni per domanda (genera-coppie.py)
import json
for n in range(len(json.loads((R / "coppie.json").read_text(encoding="utf-8")))):
    for k in ("d", "r"):
        f = R / "audio" / f"coppia-{k}{n}.mp3"
        if not f.exists() or f.stat().st_size < 2000:
            errori.append(f"manca o e' vuoto audio/coppia-{k}{n}.mp3 (rilancia strumenti/genera-coppie.py)")
        n_audio += 1

print(f"audio attesi {n_audio} · ", end="")
print(f"pagine {len(pagine)} · immagini {len(immagini)} · file nel service worker {len(in_sw)}")
for e in errori:
    print("  !", e)
print("OK" if not errori else f"{len(errori)} problemi")
sys.exit(1 if errori else 0)
