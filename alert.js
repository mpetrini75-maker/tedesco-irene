/* =======================================================================
   alert.js — Avvisi email al genitore (cervello unico, condiviso da tutte
   le pagine di "Tedesco di Irene").

   Tre eventi automatici:
     • inizio-lezione      → Irene apre la pagina di un mattoncino (lezione)
     • inizio-allenamento  → apre una pagina "-allenamento"
     • fine-allenamento    → completa la Sfida (livello 4) di TUTTE le sezioni

   L'invio "inizio" parte da solo al caricamento della pagina (capisce dal
   nome del file se è lezione o allenamento).
   Il "fine" viene segnalato dal codice della pagina chiamando
   segnaSezioneAllenamento(idSezione) ogni volta che la Sfida di una sezione
   è superata: quando tutte le sezioni sono complete parte la mail "fine".

   Ogni evento viene inviato UNA SOLA volta per sessione del browser
   (sessionStorage), così riaprire la pagina non manda mail doppie.
   Tutto fire-and-forget: se non c'è rete o c'è un errore, l'app non si blocca.

   Stesso endpoint dell'app di Inglese: il campo "materia" distingue le due app.
   ======================================================================= */
(function () {
  "use strict";

  var ENDPOINT = "https://script.google.com/macros/s/AKfycbyYq0yCTaBWEd8NCl-sRj7xrnJMpU63FV4yv26MYaOL_WPrS_0ljidhJdVHxD6_47kN/exec";
  var MATERIA = "Tedesco";
  var TOT_SEZIONI = 3;                 // sezioni per allenamento (Quiz, Vero o falso, Abbina)

  var isAllenamento = /allenamento/i.test(location.pathname) ||
                      /allenamento/i.test(document.title || "");
  var sezioniComplete = {};            // id sezione -> true (per il "fine-allenamento")

  // Nome leggibile dell'unità, dal primo <h1> (senza emoji iniziali e "— Allenamento")
  function nomeUnita() {
    var h1 = document.querySelector("h1");
    var t = ((h1 ? h1.textContent : document.title) || "");
    return t.replace(/^[^A-Za-zÀ-ÿ]+/, "")
            .replace(/\s*[—–-]\s*Allenamento\s*$/i, "")
            .trim();
  }

  // true se l'evento è già stato inviato in questa sessione (e lo segna come inviato)
  function giaInviato(evento) {
    try {
      var k = "alert_" + evento + "_" + location.pathname;
      if (sessionStorage.getItem(k)) return true;
      sessionStorage.setItem(k, "1");
      return false;
    } catch (e) {
      return false; // se sessionStorage non è disponibile, invia comunque
    }
  }

  function inviaAlert(evento) {
    if (giaInviato(evento)) return;
    try {
      fetch(ENDPOINT, {
        method: "POST",
        mode: "no-cors",                                  // Apps Script: evita problemi CORS
        headers: { "Content-Type": "text/plain;charset=utf-8" },
        body: JSON.stringify({
          materia: MATERIA,
          unita: nomeUnita(),
          evento: evento,
          dispositivo: navigator.userAgent
        })
      }).catch(function () {});
    } catch (e) {}
  }
  window.inviaAlert = inviaAlert;

  // Retrocompatibilità: chiamando inviaAlertQuiz() si manda il "fine allenamento"
  window.inviaAlertQuiz = function () { inviaAlert("fine-allenamento"); };

  // Segna una sezione dell'allenamento come completata (Sfida superata).
  // Quando tutte le sezioni sono complete -> invia "fine-allenamento".
  window.segnaSezioneAllenamento = function (idSezione) {
    if (sezioniComplete[idSezione]) return;
    sezioniComplete[idSezione] = true;
    if (Object.keys(sezioniComplete).length >= TOT_SEZIONI) {
      inviaAlert("fine-allenamento");
    }
  };

  // Invio automatico dell'evento "inizio" all'apertura della pagina
  // (capisce dal nome del file se è lezione o allenamento)
  function avvio() {
    inviaAlert(isAllenamento ? "inizio-allenamento" : "inizio-lezione");
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", avvio);
  } else {
    avvio();
  }
})();
