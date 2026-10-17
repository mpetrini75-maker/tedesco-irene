r"""Registra le voci dell'allenamento in coppia (coppie.html), dai dati di coppie.json.
Per ogni domanda n:
  audio/coppia-d<n>.mp3 = il suggerimento in italiano (voce Elsa) + la domanda in tedesco (voce Katja)
  audio/coppia-r<n>.mp3 = la risposta in tedesco (voce Katja)
Stesse voci di genera-audio.py. Rifà solo i file il cui testo e' cambiato (indice in audio/coppie-indice.json).
Uso:  py strumenti\genera-coppie.py          (--tutto per rifarli tutti)
"""
import asyncio, hashlib, json, sys
from pathlib import Path
import edge_tts

R = Path(__file__).resolve().parent.parent
AUDIO = R / "audio"
VOCI = {
    "it": ("it-IT-ElsaNeural", "+0%", "+15Hz"),
    "de": ("de-DE-KatjaNeural", "-10%", "+0Hz"),
}


async def pezzo(lingua, testo):
    voce, rate, pitch = VOCI[lingua]
    for tentativo in range(8):          # il servizio voci a volte risponde 403: si riprova
        try:
            dati = b""
            async for c in edge_tts.Communicate(testo, voce, rate=rate, pitch=pitch).stream():
                if c["type"] == "audio":
                    dati += c["data"]
            if dati:
                return dati
        except Exception:
            pass
        await asyncio.sleep(2 + tentativo)
    raise RuntimeError(f"nessun audio per: {testo}")


async def main():
    tutto = "--tutto" in sys.argv
    dati = json.loads((R / "coppie.json").read_text(encoding="utf-8"))
    AUDIO.mkdir(exist_ok=True)
    indice_f = AUDIO / "coppie-indice.json"
    vecchio = json.loads(indice_f.read_text(encoding="utf-8")) if indice_f.exists() else {}
    nuovo, fatti = {}, 0
    for n, q in enumerate(dati):
        lavori = {
            f"coppia-d{n}.mp3": [("it", q["it"] + "."), ("de", q["d"])],
            f"coppia-r{n}.mp3": [("de", q["r"])],
        }
        for nome, seg in lavori.items():
            impronta = hashlib.sha1(json.dumps([VOCI, seg], ensure_ascii=False).encode()).hexdigest()
            nuovo[nome] = impronta
            if not tutto and vecchio.get(nome) == impronta and (AUDIO / nome).exists():
                continue
            (AUDIO / nome).write_bytes(b"".join([await pezzo(l, t) for l, t in seg]))
            fatti += 1
            indice_f.write_text(json.dumps({**vecchio, **nuovo}, indent=1), encoding="utf-8")
    for f in AUDIO.glob("coppia-*.mp3"):
        if f.name not in nuovo:
            f.unlink()
            print("  tolto", f.name)
    indice_f.write_text(json.dumps(nuovo, indent=1), encoding="utf-8")
    print(f"domande {len(dati)} · audio registrati {fatti} · totale {len(nuovo)}")

asyncio.run(main())
