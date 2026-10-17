r"""Registra il testo di ogni riquadro delle lezioni con DUE voci naturali (edge-tts, neurali):
le spiegazioni in italiano con la voce di Geografia, le parole marcate lang="de" con una voce tedesca vera,
cosi' Irene sente la pronuncia giusta. Copiato da geografia-irene\strumenti\genera-audio.py (04/10/2026)
e aggiunta la voce tedesca.
Ogni riquadro con un titolo <h2> diventa audio/<pagina>-<n>.mp3 (n = ordine dei titoli nella pagina,
lo stesso che usa app.js per il tasto Ascolta). Si rilancia dopo ogni modifica al testo di una lezione.
Uso:  py strumenti\genera-audio.py            (rifa' solo gli audio il cui testo e' cambiato)
      py strumenti\genera-audio.py --tutto    (li rifa' tutti)
"""
import asyncio, hashlib, json, re, sys
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
import edge_tts

R = Path(__file__).resolve().parent.parent
AUDIO = R / "audio"
VOCI = {
    # stessa voce di Geografia ("ragazzina bella sveglia"), ma a velocita' normale:
    # a +20% Marco l'ha trovata "troppo veloce" qui, accanto al tedesco lento (04/10/2026)
    "it": ("it-IT-ElsaNeural", "+0%", "+15Hz"),
    # il tedesco un po' piu' lento del normale: e' una lingua che Irene sta imparando
    "de": ("de-DE-KatjaNeural", "-10%", "+0Hz"),
}
LEZIONI = ["schulalltag", "interrogazione"]
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿⬀-⯿️‍]")


def pulisci(t):
    t = EMOJI.sub(" ", t)
    t = t.replace("=", ",").replace("→", " ").replace("➜", " ")   # "=" si leggeva "uguale".replace("–", " - ").replace("…", " ... ")
    t = re.sub(r"\s+", " ", t)
    return t


def segmenti_card(card):
    """Restituisce [(lingua, testo), ...] nell'ordine in cui si legge il riquadro."""
    for n in card.select(".solbtn, .sol, script, figure, pre, button"):
        n.decompose()
    for td in card.select("td, th"):          # le celle di tabella si leggono separate
        td.append(". ")
    for li in card.select("li"):
        li.append(". ")
    for p in card.select("p, h2, div, tr"):   # fine di titolo/riga/riquadro = una pausa
        p.append(". ")
    seg = []
    for nodo in card.descendants:
        if not isinstance(nodo, NavigableString):
            continue
        lingua = "it"
        for g in nodo.parents:
            if g.has_attr("lang"):
                lingua = "de" if g["lang"].startswith("de") else "it"
                break
        t = pulisci(str(nodo))
        if not t.strip():
            if seg:
                seg[-1] = (seg[-1][0], seg[-1][1] + " ")
            continue
        if seg and seg[-1][0] == lingua:
            seg[-1] = (lingua, seg[-1][1] + t)
        else:
            seg.append((lingua, t))
    pul = []
    for lingua, t in seg:
        t = re.sub(r"\s*\.\s*(\.\s*)+", ". ", t)
        t = re.sub(r"\s+", " ", t).strip()
        t = re.sub(r"^[.,;:\s]+", "", t)
        if re.search(r"\w", t):
            pul.append((lingua, t))
    return pul


async def registra(segmenti, file):
    pezzi = []
    for lingua, testo in segmenti:
        voce, rate, pitch = VOCI[lingua]
        dati = b""
        async for c in edge_tts.Communicate(testo, voce, rate=rate, pitch=pitch).stream():
            if c["type"] == "audio":
                dati += c["data"]
        pezzi.append(dati)
    if not all(pezzi):   # 10/10/2026: un pezzo senza audio non deve diventare un mp3 vuoto
        raise RuntimeError(f"{file.name}: il servizio voci ha restituito un pezzo vuoto")
    # stesso formato (mp3 24 kHz mono) per tutte e due le voci: i pezzi si accodano
    file.write_bytes(b"".join(pezzi))


async def main():
    tutto = "--tutto" in sys.argv
    AUDIO.mkdir(exist_ok=True)
    indice_f = AUDIO / "indice.json"
    vecchio = json.loads(indice_f.read_text(encoding="utf-8")) if indice_f.exists() else {}
    nuovo = {}
    fatti = saltati = 0
    for slug in LEZIONI:
        soup = BeautifulSoup((R / f"{slug}.html").read_text(encoding="utf-8"), "html.parser")
        cards = [h.find_parent(class_="card") for h in soup.select(".card h2")]
        for i, card in enumerate(cards):
            if card.has_attr("data-no-voce"):
                continue
            seg = segmenti_card(card)
            nome = f"{slug}-{i}.mp3"
            impronta = hashlib.sha1(json.dumps([VOCI, seg], ensure_ascii=False).encode()).hexdigest()
            nuovo[nome] = impronta
            if not tutto and vecchio.get(nome) == impronta and (AUDIO / nome).exists():
                saltati += 1
                continue
            await registra(seg, AUDIO / nome)
            fatti += 1
            n_de = sum(1 for l, _ in seg if l == "de")
            print(f"  {nome}: {len(seg)} pezzi ({n_de} in tedesco)")
    for f in AUDIO.glob("*.mp3"):
        # 17/10/2026: gli audio dell'allenamento in coppia sono di genera-coppie.py, non si toccano
        if f.name not in nuovo and not f.name.startswith("coppia-"):
            f.unlink()
            print("  tolto", f.name)
    indice_f.write_text(json.dumps(nuovo, indent=1), encoding="utf-8")
    print(f"audio registrati: {fatti} · gia' a posto: {saltati} · totale: {len(nuovo)}")

if __name__ == "__main__":
    if "--mostra" in sys.argv:          # stampa i pezzi senza registrare, per controllare le lingue
        for slug in LEZIONI:
            soup = BeautifulSoup((R / f"{slug}.html").read_text(encoding="utf-8"), "html.parser")
            for i, h in enumerate(soup.select(".card h2")):
                card = h.find_parent(class_="card")
                if card.has_attr("data-no-voce"):
                    continue
                print(f"--- {slug}-{i}")
                for l, t in segmenti_card(card):
                    print(f"   [{l}] {t}")
    else:
        asyncio.run(main())
