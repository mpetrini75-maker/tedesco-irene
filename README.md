# Tedesco di Irene 🇩🇪

App di studio per il tedesco (2BTT), **un mattoncino alla volta**, sul libro *Linear Kompakt* (Loescher). Gemella dell'app di geografia: stesso stile, stessi strumenti, copiati da `geografia-irene` il 04/10/2026.

- **Unità 6 — Schulalltag** · materie, orario (*Stundenplan*), giorni, come vai a scuola (*mit* + dativo), *es gibt*

Il mattoncino è fatto sulla scheda 06 della wiki di Irene; **non è ancora stato confrontato con le pagine del libro**.

## Voce
Il tasto **🔊 Ascolta** suona `audio/<pagina>-<n>.mp3`, registrati con `py strumenti\genera-audio.py`: le spiegazioni con la voce italiana di Geografia (Elsa), **le parole marcate `lang="de"` con una voce tedesca** (Katja, un po' più lenta). Nelle lezioni ogni parola tedesca va scritta dentro `<span lang="de">…</span>`. `py strumenti\genera-audio.py --mostra` stampa i pezzi con la loro lingua, senza registrare.

## Collaudo
`py strumenti\controlla.py` deve uscire con 0 prima di ogni pubblicazione. A ogni modifica: alzare la versione della cache in `service-worker.js`.

App installabile (PWA) su telefono e tablet. Fatto con cura per Irene 🌿
