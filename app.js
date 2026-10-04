/* Tedesco di Irene — utilità condivise (copiate da Geografia) */
function toggleSol(id, btn){
  var el = document.getElementById(id);
  if(!el) return;
  var open = el.classList.toggle("open");
  if(btn) btn.textContent = open ? "🙈 Nascondi soluzioni" : "🔑 Mostra soluzioni";
}

/* 🔊 Ascolta: ogni riquadro con un titolo ha la sua registrazione con voce naturale
   (audio/<pagina>-<n>.mp3, fatte con strumenti/genera-audio.py).
   Niente sintesi vocale del telefono: Marco l'ha bocciata, "estremamente robotica" (03/10/2026).
   n = posizione del titolo <h2> fra tutti i riquadri della pagina, come nello script. */
(function(){
  var pagina = (location.pathname.split("/").pop() || "index.html").replace(/\.html$/, "");
  var player = new Audio();
  var attivo = null;

  function ferma(){
    player.pause();
    if(attivo){ attivo.classList.remove("on"); attivo.textContent = "🔊 Ascolta"; attivo = null; }
  }
  player.addEventListener("ended", ferma);
  player.addEventListener("error", function(){
    if(attivo){ attivo.textContent = "🔇 Audio non disponibile"; attivo.classList.remove("on"); attivo = null; }
  });

  function aggiungi(){
    document.querySelectorAll(".card h2").forEach(function(h, n){
      var card = h.closest(".card");
      if(!card || card.hasAttribute("data-no-voce")) return;
      var b = document.createElement("button");
      b.className = "ascolta"; b.type = "button"; b.textContent = "🔊 Ascolta";
      b.addEventListener("click", function(){
        if(attivo === b){ ferma(); return; }
        ferma();
        player.src = "audio/" + pagina + "-" + n + ".mp3";
        attivo = b; b.classList.add("on"); b.textContent = "⏹ Ferma";
        player.play().catch(function(){ ferma(); });
      });
      h.parentNode.insertBefore(b, h);
    });
  }
  if(document.readyState === "loading") document.addEventListener("DOMContentLoaded", aggiungi); else aggiungi();
  window.addEventListener("pagehide", ferma);
})();
