/* Geografia di Irene — motore degli allenamenti (uguale per tutti i mattoncini).
   Ogni pagina -allenamento definisce window.ALLENAMENTO = { quiz:[livelli], vf:[livelli], abbina:[livelli] }
   e questo file costruisce le tre sezioni. Stessa meccanica di fisica: livelli che si sbloccano,
   si può riprovare quanto si vuole, niente punizioni. */
(function(){
  var D = window.ALLENAMENTO;
  var LV = ["Base","Intermedio","Sfida","Super sfida"];

  function stars(c,t){ var p=c/t; var n=p===1?5:p>=0.75?4:p>=0.5?3:p>=0.25?2:1; return "⭐".repeat(n); }
  function shuffle(a){ a=a.slice(); for(var i=a.length-1;i>0;i--){ var j=Math.floor(Math.random()*(i+1)); var x=a[i]; a[i]=a[j]; a[j]=x; } return a; }
  function levelBar(level,tot){
    var dots=""; for(var i=0;i<tot;i++) dots+='<span class="lvdot '+(i<=level?'on':'')+'">'+(i+1)+'</span>';
    return '<div class="lvrow"><b>Livello '+(level+1)+' di '+tot+' · '+LV[level]+' 🔓</b><span class="lvdots">'+dots+'</span></div>';
  }
  function levelResult(progEl, score, total, level, totLv, threshold, setFnName){
    var passed = score>=threshold;
    var html='<div class="star">'+stars(score,total)+'</div>'+score+'/'+total+' al primo colpo<br>';
    if(passed && level<totLv-1){
      html+='<b>Bravissima! Livello '+(level+2)+' sbloccato 🔓</b><br><button class="restart" onclick="'+setFnName+'('+(level+1)+')">➡️ Vai al Livello '+(level+2)+'</button>';
    } else if(passed){
      if(window.segnaSezioneAllenamento) segnaSezioneAllenamento(setFnName);
      html+='<b>🏆 Hai completato tutti i livelli!</b><br><button class="restart" onclick="'+setFnName+'(0)">🔄 Rigioca dal Livello 1</button>';
    } else {
      html+='<b>Ci sei quasi! Riprova questo livello, ce la fai 🌱</b><br><button class="restart" onclick="'+setFnName+'('+level+')">🔄 Rifai il Livello '+(level+1)+'</button>';
    }
    progEl.innerHTML=html;
  }

  /* ---------- domande a scelta (quiz e vero/falso usano lo stesso meccanismo) ---------- */
  function sezioneDomande(chiave, fnName){
    var stato={lv:0, i:0, punti:0, giusta:0, sbagliato:false};
    var dati = D[chiave];
    function set(lv){ stato.lv=lv; stato.i=0; stato.punti=0;
      document.getElementById(chiave+"-level").innerHTML=levelBar(lv, dati.length); mostra(); }
    function mostra(){
      var lista=dati[stato.lv], box=document.getElementById(chiave+"-box"), pr=document.getElementById(chiave+"-prog");
      if(stato.i>=lista.length){ box.innerHTML=""; levelResult(pr, stato.punti, lista.length, stato.lv, dati.length, Math.max(lista.length-1,1), fnName); return; }
      var it=lista[stato.i], opts, ordine;
      if(chiave==="vf"){ opts=["✅ Vero","❌ Falso"]; ordine=[0,1]; stato.giusta=it.v?0:1; }
      else { ordine=shuffle(it.opts.map(function(_,k){return k;})); opts=ordine.map(function(k){return it.opts[k];}); stato.giusta=ordine.indexOf(0); }
      stato.sbagliato=false;
      pr.textContent="Domanda "+(stato.i+1)+" di "+lista.length;
      box.innerHTML='<div class="ex"><div class="qnum">Domanda '+(stato.i+1)+'</div><div class="qtext">'+it.q+'</div><div class="options">'+
        opts.map(function(o,k){return '<button class="opt" onclick="'+fnName+'_r('+k+')">'+o+'</button>';}).join("")+
        '</div><div class="feedback" id="'+chiave+'-fb"></div></div>';
    }
    function risposta(k){
      var bott=document.querySelectorAll("#"+chiave+"-box .opt"), fb=document.getElementById(chiave+"-fb"), it=dati[stato.lv][stato.i];
      if(k===stato.giusta){
        bott[k].classList.add("correct");
        fb.innerHTML="✅ Giusto!"+(it.perche?" "+it.perche:""); fb.className="feedback ok";
        if(!stato.sbagliato) stato.punti++;
        bott.forEach(function(b){b.disabled=true;});
        setTimeout(function(){ stato.i++; mostra(); }, it.perche?2200:1100);
      } else {
        stato.sbagliato=true; bott[k].classList.add("wrong");
        fb.textContent="Riprova 🙂"; fb.className="feedback no";
      }
    }
    window[fnName]=set; window[fnName+"_r"]=risposta;
    set(0);
  }

  /* ---------- abbina ---------- */
  var m={lv:0, sel:null, fatte:0, primo:0, rovinate:null};
  function setAbbina(lv){
    m.lv=lv; m.sel=null; m.fatte=0; m.primo=0; m.rovinate=new Set();
    var coppie=D.abbina[lv];
    document.getElementById("abbina-level").innerHTML=levelBar(lv, D.abbina.length);
    var sx=coppie.map(function(p,i){return '<button class="match-btn" id="ml'+i+'" onclick="abbinaL('+i+')">'+p.l+'</button>';}).join("");
    var dx=shuffle(coppie.map(function(_,i){return i;})).map(function(i){return '<button class="match-btn" id="mr'+i+'" onclick="abbinaR('+i+')">'+coppie[i].r+'</button>';}).join("");
    document.getElementById("abbina-grid").innerHTML='<div class="match-col">'+sx+'</div><div class="match-col">'+dx+'</div>';
    document.getElementById("abbina-prog").textContent="Coppie collegate: 0 di "+coppie.length;
  }
  window.setAbbina=setAbbina;
  window.abbinaL=function(i){
    var b=document.getElementById("ml"+i); if(b.classList.contains("done")) return;
    document.querySelectorAll(".match-btn.sel").forEach(function(x){x.classList.remove("sel");});
    m.sel=i; b.classList.add("sel");
  };
  window.abbinaR=function(i){
    if(m.sel===null) return;
    var r=document.getElementById("mr"+i); if(r.classList.contains("done")) return;
    var l=document.getElementById("ml"+m.sel), coppie=D.abbina[m.lv];
    if(m.sel===i){
      l.classList.remove("sel"); l.classList.add("done"); r.classList.add("done");
      if(!m.rovinate.has(m.sel)) m.primo++;
      m.sel=null; m.fatte++;
      var pr=document.getElementById("abbina-prog");
      if(m.fatte>=coppie.length) levelResult(pr, m.primo, coppie.length, m.lv, D.abbina.length, Math.max(coppie.length-1,1), "setAbbina");
      else pr.textContent="Coppie collegate: "+m.fatte+" di "+coppie.length;
    } else {
      m.rovinate.add(m.sel); r.classList.add("flash");
      setTimeout(function(){r.classList.remove("flash");},500);
      l.classList.remove("sel"); m.sel=null;
    }
  };

  sezioneDomande("quiz","setQuiz");
  sezioneDomande("vf","setVF");
  setAbbina(0);
})();
