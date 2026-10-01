(function(){
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var root = document.documentElement;
  var main = document.getElementById('top');
  var $ = function(id){return document.getElementById(id)};
  var lerp = function(a,b,t){return a+(b-a)*t};
  var clamp = function(v,a,b){return Math.max(a,Math.min(b,v))};
  var pageOf = function(url){var p = url.pathname.split('/').pop();return p || 'index.html'};
  var here = pageOf(location);
  var parent = document.body.dataset.parent || '';

  /* ---------- scroll suave ---------- */
  var lenis = null;
  if(!reduce && window.Lenis){
    lenis = new Lenis({duration:1.25, easing:function(t){return Math.min(1,1.001-Math.pow(2,-10*t))}, smoothWheel:true});
    var raf = function(t){lenis.raf(t);requestAnimationFrame(raf)};
    requestAnimationFrame(raf);
  }
  // Al saltar a una sección, alineamos su etiqueta/título (no el borde de la sección,
  // que tiene mucho padding) justo debajo del menú. offsetTop ignora las transformaciones
  // de las animaciones de entrada, así que la posición es la final.
  var ANCHOR_GAP = 110;
  var docTop = function(node){
    var y = 0;
    while(node){y += node.offsetTop; node = node.offsetParent}
    return y;
  };
  // inicio real del contenido: el primer elemento visible dentro del .wrap de la sección
  // (título, foto o lo que quede más arriba), sin contar el padding de la sección
  var anchorY = function(el){
    var box = el.querySelector(':scope > .wrap') || el;
    var top = Infinity;
    Array.prototype.forEach.call(box.children, function(k){
      if(k.offsetParent===null || k.classList.contains('sr-only')){return}
      top = Math.min(top, docTop(k));
    });
    if(!isFinite(top)){top = docTop(el)}
    return Math.max(0, top - ANCHOR_GAP);
  };
  var scrollToTarget = function(el){
    var y = el===0 ? 0 : anchorY(el);
    if(lenis){lenis.scrollTo(y,{duration: el===0 ? 1.1 : 1.6})}
    else{window.scrollTo({top:y,behavior:reduce?'auto':'smooth'})}
  };

  // Llegada desde otra página con #ancla: corregimos el salto nativo del navegador
  // y lo repetimos cuando terminan de cargar las fuentes y las imágenes.
  var hashEl = null;
  try{hashEl = location.hash.length>1 ? document.querySelector(decodeURIComponent(location.hash)) : null}catch(err){}
  if(hashEl){
    // sin el # en la URL el navegador no vuelve a aplicar su propio salto al terminar la carga
    var hash = location.hash;
    if('scrollRestoration' in history){history.scrollRestoration = 'manual'}
    history.replaceState(null,'',location.pathname+location.search);
    var userMoved = false;
    ['wheel','touchstart','keydown'].forEach(function(ev){window.addEventListener(ev,function(){userMoved=true},{once:true,passive:true})});
    var jumpToHash = function(){
      if(userMoved){return}
      var y = anchorY(hashEl);
      if(lenis){lenis.scrollTo(y,{immediate:true,force:true})}
      else{window.scrollTo(0,y)}
    };
    jumpToHash();
    requestAnimationFrame(jumpToHash);
    if(document.fonts && document.fonts.ready){document.fonts.ready.then(jumpToHash)}
    window.addEventListener('load',function(){
      jumpToHash();
      setTimeout(function(){jumpToHash();history.replaceState(null,'',location.pathname+location.search+hash)},150);
    });
  }

  /* ---------- navegación entre páginas ---------- */
  var curtain = $('curtain');
  var leaving = false;
  document.querySelectorAll('a[href]').forEach(function(a){
    var raw = a.getAttribute('href');
    if(!raw || raw==='#' || a.target==='_blank' || /^(mailto:|tel:|https?:)/.test(raw)){return}
    var url = new URL(a.href, location.href);
    var samePage = pageOf(url)===here;

    // estado activo en el menú
    if(!samePage || raw.charAt(0)==='#'){}
    else if(a.closest('.nav-links>li')===a.parentElement || a.classList.contains('big')){a.setAttribute('aria-current','page')}
    if(parent && pageOf(url)===parent && raw===parent && (a.closest('.nav-links>li')===a.parentElement || a.classList.contains('big'))){a.setAttribute('aria-current','page')}

    a.addEventListener('click',function(e){
      if(e.metaKey || e.ctrlKey || e.shiftKey || e.button===1){return}
      if(samePage){
        var id = url.hash;
        var el = id.length>1 ? document.querySelector(id) : null;
        if(id.length>1 && !el){return}
        e.preventDefault();
        closeMenu();
        scrollToTarget(el && id!=='#top' ? el : 0);
        if(id.length>1){history.replaceState(null,'',id)}
        return;
      }
      if(!curtain || reduce || leaving){return}
      e.preventDefault();
      leaving = true;
      closeMenu();
      curtain.classList.remove('out');
      curtain.classList.add('in');
      setTimeout(function(){location.href = a.href},650);
    });
  });
  // al volver con el botón atrás (bfcache) retirar la cortina
  window.addEventListener('pageshow',function(e){
    if(e.persisted && curtain){leaving=false;curtain.classList.remove('in');curtain.classList.add('out')}
  });

  /* ---------- entrada: loader en portada, cortina en el resto ---------- */
  var loader = $('loader');
  var ready = function(){main.classList.add('ready')};
  if(curtain){curtain.classList.add('out')}
  if(loader && !reduce && !sessionStorageSeen()){
    var count = $('loaderCount'), bar = $('loaderBar');
    if(lenis){lenis.stop()}
    var t0 = performance.now(), dur = 1500;
    var tick = function(now){
      var p = clamp((now-t0)/dur,0,1);
      var e = 1-Math.pow(1-p,3);
      count.textContent = Math.round(e*100);
      bar.style.transform = 'scaleX('+e+')';
      if(p<1){requestAnimationFrame(tick);return}
      loader.classList.add('done');
      setTimeout(ready,250);
      setTimeout(function(){loader.style.display='none'},1300);
      if(lenis){lenis.start()}
    };
    requestAnimationFrame(tick);
  }else{
    if(loader){loader.style.display='none'}
    setTimeout(ready, curtain && !reduce ? 200 : 0);
  }
  // el loader largo solo se ve una vez por sesión
  function sessionStorageSeen(){
    try{
      if(sessionStorage.getItem('cm-intro')){return true}
      sessionStorage.setItem('cm-intro','1');
    }catch(err){}
    return false;
  }

  /* ---------- nav ---------- */
  var nav = $('nav');
  var burger = $('burger');
  var mmenu = $('mmenu');
  var lastY = 0;
  var onScrollNav = function(y){
    nav.classList.toggle('solid', y>40);
    var d = y-lastY;
    if(Math.abs(d)<6){return}
    nav.classList.toggle('hide', !mmenu.classList.contains('open') && d>0 && y>400);
    lastY = y;
  };
  function closeMenu(){
    if(!mmenu || !mmenu.classList.contains('open')){return}
    mmenu.classList.remove('open');burger.setAttribute('aria-expanded','false');burger.setAttribute('aria-label','Abrir menú');
    if(lenis){lenis.start()}
  }
  burger.addEventListener('click',function(){
    var open = mmenu.classList.toggle('open');
    burger.setAttribute('aria-expanded',open?'true':'false');
    burger.setAttribute('aria-label',open?'Cerrar menú':'Abrir menú');
    if(lenis){open?lenis.stop():lenis.start()}
  });
  document.addEventListener('keydown',function(e){if(e.key==='Escape'){closeMenu()}});

  /* ---------- revelados ---------- */
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(en){
      if(en.isIntersecting){
        var t = en.target;
        t.classList.add('in');io.unobserve(t);
      }
    });
  },{rootMargin:'0px 0px -12% 0px'});
  document.querySelectorAll('[data-reveal],[data-lines],[data-clip]').forEach(function(el){io.observe(el)});
  // el logotipo del footer está pegado al final de la página: se activa en cuanto asoma
  var wmIO = new IntersectionObserver(function(entries){
    entries.forEach(function(en){
      if(!en.isIntersecting){return}
      var t = en.target;
      t.classList.add('in');wmIO.unobserve(t);
      setTimeout(function(){t.classList.add('done')},1800);
    });
  },{threshold:.15});
  document.querySelectorAll('.wordmark').forEach(function(el){wmIO.observe(el)});

  /* ---------- contadores ---------- */
  var cio = new IntersectionObserver(function(entries){
    entries.forEach(function(en){
      if(!en.isIntersecting){return}
      var el = en.target, to = +el.dataset.count, t0 = performance.now(), d = 1800;
      cio.unobserve(el);
      if(reduce){el.textContent = to;return}
      (function step(now){
        var p = clamp((now-t0)/d,0,1);
        el.textContent = Math.round(to*(1-Math.pow(1-p,4)));
        if(p<1){requestAnimationFrame(step)}
      })(t0);
    });
  },{threshold:.6});
  document.querySelectorAll('[data-count]').forEach(function(el){cio.observe(el)});

  /* ---------- texto que se ilumina palabra a palabra ---------- */
  var man = $('manifesto');
  var words = [];
  if(man){
    (function split(node){
      Array.prototype.slice.call(node.childNodes).forEach(function(ch){
        if(ch.nodeType===3){
          var frag = document.createDocumentFragment();
          ch.textContent.split(/(\s+)/).forEach(function(part){
            if(!part){return}
            if(/^\s+$/.test(part)){frag.appendChild(document.createTextNode(part));return}
            var s = document.createElement('span');s.className='w';s.textContent=part;frag.appendChild(s);words.push(s);
          });
          node.replaceChild(frag,ch);
        }else if(ch.nodeType===1){split(ch)}
      });
    })(man);
  }

  /* ---------- tickers de colectivos ---------- */
  var groups = [
    ['Infancia','Jóvenes','Mayores','Género'],
    ['Migrantes','Personas vulnerables','Diversidad funcional','Personas privadas de libertad']
  ];
  var tickers = Array.prototype.slice.call(document.querySelectorAll('.ticker'));
  tickers.forEach(function(tk,i){
    var html = '';
    for(var r=0;r<3;r++){
      groups[i%2].forEach(function(w,j){
        html += '<span>'+(j%2?'<em>'+w+'</em>':w)+'<svg><use href="#sym"/></svg></span>';
      });
    }
    tk.innerHTML = html;
    tk._x = 0;
  });

  /* ---------- bucle de animación ---------- */
  var heroMedia = document.querySelector('.hero-media');
  var footer = document.getElementById('footer');
  var footInner = footer ? footer.querySelector('.foot-inner') : null;
  var footBg = footer ? footer.querySelector('.fc-bg') : null;
  var y = window.scrollY, vel = 0, prevY = y;
  var frame = function(){
    y = lenis ? lenis.scroll : window.scrollY;
    vel = lerp(vel, y-prevY, .1); prevY = y;
    var vh = window.innerHeight;

    if(heroMedia && y < vh*1.2 && !reduce){
      heroMedia.style.transform = 'translate3d(0,'+(y*.3)+'px,0)';
    }

    if(man){
      var r = man.getBoundingClientRect();
      var p = clamp((vh*.85 - r.top)/(r.height+vh*.35),0,1);
      var lit = Math.floor(p*words.length*1.05);
      for(var i=0;i<words.length;i++){words[i].classList.toggle('on',i<lit)}
    }

    if(!reduce){
      tickers.forEach(function(tk){
        var sp = +tk.dataset.speed;
        var w = tk.scrollWidth/3;
        tk._x += sp*1.2;   // velocidad constante, sin acelerones con el scroll
        if(tk._x < -w){tk._x += w}
        if(tk._x > 0){tk._x -= w}
        tk.style.transform = 'translate3d('+tk._x+'px,0,0)';
      });
    }

    // el footer asoma desde debajo del contenido
    if(footInner && !reduce){
      var fr = footer.getBoundingClientRect();
      if(fr.top < vh){
        var fp = clamp((vh - fr.top)/Math.min(fr.height,vh),0,1);
        footInner.style.transform = 'translate3d(0,'+((1-fp)*-140)+'px,0)';
        if(footBg){footBg.style.transform = 'translate3d(0,'+((1-fp)*-80)+'px,0)'}
      }
    }

    onScrollNav(y);
    requestAnimationFrame(frame);
  };
  requestAnimationFrame(frame);

  /* ---------- hero «Nadie fuera»: el símbolo hecho de personas ----------
     Cientos de puntos forman el símbolo de conecta+. Alrededor flotan puntos grises
     «fuera»; al acercar el cursor (o tocar) se conectan, se vuelven lima y se unen. */
  var hc = $('heroNet');
  if(hc){
    var hx = hc.getContext('2d');
    var heroEl = hc.parentElement;
    var hint = $('heroHint'), hintText = $('heroHintText'), hCount = $('heroCount'), hTotal = $('heroTotal');
    var HD = Math.min(window.devicePixelRatio||1,2);
    var HW=0,HH=0,S=0,CX=0,CY=0,mob=false;
    var pts=[],outs=[],connected=0,started=false,t0=0,allDone=false;
    var hmx=-9999,hmy=-9999,hsmx=0,hsmy=0,heroOn=true;
    var LIME='196,242,29',MAG='226,75,196',GREY='241,245,238';

    // dibuja el símbolo en un lienzo auxiliar y devuelve puntos muestreados
    var sampleSymbol = function(size,step){
      var c = document.createElement('canvas'); c.width = c.height = Math.ceil(size);
      var g = c.getContext('2d'), k = size/64;
      var fig = function(color){
        g.fillStyle = color;
        g.beginPath(); g.arc(21*k,15*k,8*k,0,Math.PI*2); g.fill();
        var x=8*k,y=26*k,w=26*k,h=30*k,r=13*k;
        g.beginPath(); g.moveTo(x+r,y); g.arcTo(x+w,y,x+w,y+h,r); g.arcTo(x+w,y+h,x,y+h,r); g.arcTo(x,y+h,x,y,r); g.arcTo(x,y,x+w,y,r); g.fill();
      };
      fig('#f00');
      g.save(); g.translate(32*k,32*k); g.rotate(Math.PI); g.translate(-32*k,-32*k); fig('#00f'); g.restore();
      var d = g.getImageData(0,0,c.width,c.height).data, out = [];
      for(var y=0;y<c.height;y+=step){
        for(var x=0;x<c.width;x+=step){
          var jx = x + (Math.random()-.5)*step*.6, jy = y + (Math.random()-.5)*step*.6;
          var i = (Math.floor(jy)*c.width + Math.floor(jx))*4;
          if(i<0 || i>=d.length || d[i+3]<128){continue}
          out.push({x:jx - size/2, y:jy - size/2, c: d[i]>d[i+2] ? LIME : MAG});
        }
      }
      return out;
    };

    var layout = function(){
      var r = heroEl.getBoundingClientRect();
      HW = r.width; HH = r.height; mob = HW < 900;
      hc.width = HW*HD; hc.height = HH*HD; hx.setTransform(HD,0,0,HD,0,0);
      S = mob ? Math.min(HW*.78, HH*.42) : Math.min(HH*.54, HW*.32);
      CX = mob ? HW*.5 : HW*.755;
      CY = mob ? HH*.36 : HH*.46;
      var targets = sampleSymbol(S, Math.max(5, S/(mob?34:46)));
      // reutiliza las partículas existentes al redimensionar
      var old = pts; pts = [];
      targets.forEach(function(t,i){
        var p = old[i] || {x: Math.random()*HW, y: Math.random()<.5 ? -40 : HH+40, vx:0, vy:0, z: .55 + Math.random()*.9, d: Math.random()*.9};
        p.tx = t.x; p.ty = t.y; p.c = t.c;
        pts.push(p);
      });
      // puntos «fuera»: repartidos alrededor del símbolo, sin tapar el titular
      if(!outs.length){
        var n = mob ? 18 : 30;
        for(var i=0;i<n;i++){
          var a = Math.random()*Math.PI*2, rad = .62 + Math.random()*.55;
          outs.push({a:a, rad:rad, ph: Math.random()*6.28, on:false, k:0, x:0, y:0, tgt: Math.floor(Math.random()*targets.length)});
        }
        hTotal.textContent = n;
      }
      if(hint){ hint.style.left = CX+'px'; hint.style.top = (CY + S*.5 + (mob?14:20))+'px'; }
      if(reduce){ pts.forEach(function(p){p.x = CX+p.tx; p.y = CY+p.ty}); }
    };

    var connect = function(o){
      if(o.on){return}
      o.on = true; connected++;
      hCount.textContent = connected;
      if(connected === outs.length && !allDone){
        allDone = true;
        hint.classList.add('done');
        hintText.innerHTML = '<b>Nadie fuera.</b> Así trabajamos.';
      }
    };

    var drawHero = function(now){
      var el = (now - t0)/1000;
      var sy = lenis ? lenis.scroll : window.scrollY;
      var sp = clamp(sy/(HH*.85),0,1);                       // progreso del primer scroll
      hsmx = lerp(hsmx, hmx>-999 ? (hmx-CX)/HW : 0, .06);    // parallax suave del cursor
      hsmy = lerp(hsmy, hmy>-999 ? (hmy-CY)/HH : 0, .06);
      hx.clearRect(0,0,HW,HH);

      // halo detrás del símbolo
      var glow = hx.createRadialGradient(CX,CY,0,CX,CY,S*.85);
      glow.addColorStop(0,'rgba(196,242,29,'+(.13*(1-sp))+')'); glow.addColorStop(1,'rgba(196,242,29,0)');
      hx.fillStyle = glow; hx.fillRect(0,0,HW,HH);

      var alphaAll = (mob ? .55 : 1) * (1 - sp*.9);
      // partículas del símbolo
      for(var i=0;i<pts.length;i++){
        var p = pts[i];
        var px = CX + p.tx - hsmx*40*p.z, py = CY + p.ty - hsmy*30*p.z;
        // dispersión al hacer scroll: se abren hacia fuera según su profundidad
        px += p.tx*sp*1.8*p.z; py += p.ty*sp*1.8*p.z - sp*HH*.15*p.z;
        if(reduce){ p.x = px; p.y = py; }
        else if(started && el > p.d){
          var ax = (px - p.x)*.018, ay = (py - p.y)*.018;
          var dx = p.x - hmx, dy = p.y - hmy, dd = dx*dx+dy*dy;
          if(dd < 9000){ var f = (9000-dd)/9000*1.6; var dl = Math.sqrt(dd)||1; ax += dx/dl*f; ay += dy/dl*f; }
          p.vx = p.vx*.86 + ax; p.vy = p.vy*.86 + ay;
          p.x += p.vx; p.y += p.vy;
        }
        var formed = started ? clamp((el - p.d)*1.1,0,1) : 0;
        var col = formed < 1 ? GREY : p.c;
        hx.fillStyle = 'rgba('+col+','+((.35 + .6*formed)*alphaAll)+')';
        var rr = (mob?1:1.25)*p.z + .35;
        hx.fillRect(p.x-rr, p.y-rr, rr*2, rr*2);
      }

      // puntos «fuera»
      var outA = (1 - sp) * (started ? clamp(el-1.2,0,1) : 0);
      if(outA > 0){
        for(var j=0;j<outs.length;j++){
          var o = outs[j];
          var bx = CX + Math.cos(o.a + el*.05)*S*o.rad*(mob?.62:.95), by = clamp(CY + Math.sin(o.a + el*.05)*S*o.rad*(mob?.62:.78) + Math.sin(el*.8+o.ph)*6, 110, HH-120);
          bx = clamp(bx, 16, HW-16);
          var tp = pts[o.tgt];
          if(o.on){ o.k = Math.min(1, o.k + .03); }
          // al conectarse viajan hasta su hueco junto al símbolo
          var ex = tp ? lerp(bx, (bx+tp.x)/2, o.k*.55) : bx, ey = tp ? lerp(by, (by+tp.y)/2, o.k*.55) : by;
          o.x = ex; o.y = ey;
          var mdx = hmx - ex, mdy = hmy - ey, md = Math.sqrt(mdx*mdx+mdy*mdy);
          if(!o.on && md < 170){
            hx.strokeStyle = 'rgba('+LIME+','+(.55*(1-md/170)*outA)+')'; hx.lineWidth = 1;
            hx.beginPath(); hx.moveTo(hmx,hmy); hx.lineTo(ex,ey); hx.stroke();
            if(md < 60){ connect(o); }
          }
          if(o.on && tp){
            hx.strokeStyle = 'rgba('+LIME+','+(.28*o.k*outA*alphaAll)+')'; hx.lineWidth = 1;
            hx.beginPath(); hx.moveTo(ex,ey); hx.lineTo(tp.x,tp.y); hx.stroke();
          }
          hx.fillStyle = o.on ? 'rgba('+LIME+','+outA+')' : 'rgba('+GREY+','+(.55*outA)+')';
          hx.beginPath(); hx.arc(ex,ey,o.on?3:2.6,0,Math.PI*2); hx.fill();
          if(!o.on){ hx.strokeStyle = 'rgba('+GREY+','+(.25*outA)+')'; hx.beginPath(); hx.arc(ex,ey,7+Math.sin(el*2+o.ph)*2,0,Math.PI*2); hx.stroke(); }
        }
      }
      if(hint){ hint.classList.toggle('on', started && el > 1.8 && sp < .3); }
    };

    var loopHero = function(now){ if(heroOn){drawHero(now)} requestAnimationFrame(loopHero); };
    layout();
    if(!fine){ hintText.innerHTML = 'Cada punto es una persona. <b>Toca los puntos grises</b> para conectarlos.'; }
    // arranca cuando termina la entrada (loader / cortina)
    (function waitReady(){
      if(main.classList.contains('ready')){ started = true; t0 = performance.now() - (reduce ? 10000 : 0); }
      else { setTimeout(waitReady,60); }
    })();
    requestAnimationFrame(loopHero);
    new IntersectionObserver(function(e){heroOn = e[0].isIntersecting}).observe(heroEl);
    var rT; window.addEventListener('resize',function(){clearTimeout(rT); rT = setTimeout(layout,150)});
    var setPtr = function(e){ var r = hc.getBoundingClientRect(); hmx = e.clientX - r.left; hmy = e.clientY - r.top; };
    heroEl.addEventListener('pointermove',setPtr);
    heroEl.addEventListener('pointerdown',setPtr);
    heroEl.addEventListener('pointerleave',function(e){ if(e.pointerType==='mouse'){hmx = hmy = -9999} });
  }

  /* ---------- hilo conductor: la red que recorre cada página ----------
     Se construye solo a partir de las secciones de la página que tienen etiqueta
     (.kicker) o título, así que funciona en todas las páginas, también las futuras. */
  var buildThread = function(){
    var secs = Array.prototype.filter.call(document.querySelectorAll('main > section'),function(s){
      return !s.classList.contains('hero') && !s.classList.contains('page-hero') && s.querySelector('.kicker, h2');
    });
    if(secs.length < 2){return}
    var thread = $('thread');
    if(!thread){
      thread = document.createElement('nav');
      thread.className = 'thread'; thread.id = 'thread'; thread.setAttribute('aria-label','Recorrido de la página');
      thread.innerHTML = '<span class="thread-track"><span class="thread-fill"></span></span>';
      document.body.appendChild(thread);
    }
    var tFill = thread.querySelector('.thread-fill'), tSecs = [], tStart = 0, tEnd = 1, tCur = -1;
    secs.forEach(function(el){
      var k = el.querySelector('.kicker'), h = el.querySelector('h2');
      var label = ((k && k.textContent) || (h && h.textContent) || '').replace(/\s+/g,' ').trim();
      if(!label){return}
      if(label.length > 30){label = label.slice(0,28)+'…'}
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'thread-node';
      b.innerHTML = '<i></i><span></span>'; b.querySelector('span').textContent = label;
      b.setAttribute('aria-label','Ir a '+label);
      b.addEventListener('click',function(){scrollToTarget(el)});
      thread.appendChild(b);
      tSecs.push({el:el,btn:b});
    });
    var measure = function(){
      var top = document.querySelector('.hero, .page-hero');
      tStart = top ? top.offsetHeight*.6 : 0;
      tEnd = Math.max(tStart+1, (footer ? docTop(footer) : document.documentElement.scrollHeight) - window.innerHeight);
      var last = -1;
      tSecs.forEach(function(s){
        s.at = clamp((docTop(s.el) - window.innerHeight*.4 - tStart)/(tEnd - tStart),0,1);
        s.btn.style.top = (s.at*100)+'%';
        // nodos demasiado juntos se ocultan para que no se pisen
        var tooClose = last > -1 && s.at - last < .045;
        s.btn.hidden = tooClose; if(!tooClose){last = s.at}
      });
    };
    measure();
    window.addEventListener('resize',measure);
    window.addEventListener('load',measure);
    var upd = function(){
      var y = lenis ? lenis.scroll : window.scrollY;
      var p = clamp((y - tStart)/(tEnd - tStart),0,1);
      tFill.style.transform = 'scaleY('+p+')';
      thread.classList.toggle('on', y > tStart*.8 && y < tEnd + window.innerHeight*.2);
      var cur = -1;
      tSecs.forEach(function(s,i){ var lit = p >= s.at - .002; s.btn.classList.toggle('lit',lit); if(lit && !s.btn.hidden){cur = i} });
      if(cur !== tCur){
        tSecs.forEach(function(s,i){s.btn.classList.toggle('cur',i===cur)});
        if(cur > -1){ var bb = tSecs[cur].btn; bb.classList.add('flash'); clearTimeout(bb._f); bb._f = setTimeout(function(){bb.classList.remove('flash')},1400); }
        tCur = cur;
      }
    };
    window.addEventListener('scroll',upd,{passive:true});
    upd();
  };
  buildThread();

  /* ---------- constelación internacional: resaltar cada conexión ---------- */
  document.querySelectorAll('.intl-map').forEach(function(map){
    var sec = map.closest('section') || document;
    sec.querySelectorAll('.intl-list li[data-arc]').forEach(function(li){
      var k = li.dataset.arc;
      li.addEventListener('mouseenter',function(){
        map.classList.add('hl');
        map.querySelectorAll('[data-arc]').forEach(function(n){n.classList.toggle('on',n.dataset.arc===k)});
      });
      li.addEventListener('mouseleave',function(){
        map.classList.remove('hl');
        map.querySelectorAll('[data-arc]').forEach(function(n){n.classList.remove('on')});
      });
    });
  });

  /* ---------- la red que crece: fondo de red y nodo nuevo al enviar un formulario ----------
     <canvas class="cta-net" data-theme="light|dark" data-form="idDelFormulario"> */
  var easeOut = function(x){return 1-Math.pow(1-x,3)};
  document.querySelectorAll('.cta-net').forEach(function(cn){
    var g = cn.getContext('2d'), D = Math.min(window.devicePixelRatio||1,2), W=0, H=0, nodes=[], on=false;
    var dark = cn.dataset.theme === 'dark';
    var base = dark ? '241,245,238' : '22,40,28';
    var youCol = dark ? '196,242,29' : '206,11,165';
    var size = function(){
      var r = cn.getBoundingClientRect(); W = r.width; H = r.height;
      cn.width = W*D; cn.height = H*D; g.setTransform(D,0,0,D,0,0);
      if(!nodes.length){
        var n = W < 700 ? 24 : 44;
        for(var i=0;i<n;i++){ nodes.push({fx:.52 + Math.random()*.46, fy:.08 + Math.random()*.84, ph:Math.random()*6.28, r:1.6 + Math.random()*1.8, you:false, k:1}); }
      }
    };
    var draw = function(now){
      var t = now/1000;
      g.clearRect(0,0,W,H);
      var P = nodes.map(function(n){ return {x:n.fx*W + Math.sin(t*.4+n.ph)*6, y:n.fy*H + Math.cos(t*.35+n.ph)*6, n:n}; });
      for(var i=0;i<P.length;i++){
        var pi = P[i];
        if(pi.n.you){ pi.n.k = Math.min(1, pi.n.k + .02); var e = easeOut(pi.n.k); pi.x = lerp(pi.n.sx, pi.x, e); pi.y = lerp(pi.n.sy, pi.y, e); }
      }
      for(i=0;i<P.length;i++){
        for(var j=i+1;j<P.length;j++){
          var dx = P[i].x-P[j].x, dy = P[i].y-P[j].y, d = Math.sqrt(dx*dx+dy*dy);
          if(d < 150){
            var you = P[i].n.you || P[j].n.you;
            g.strokeStyle = you ? 'rgba('+youCol+','+(.6*(1-d/150)*Math.min(P[i].n.k,P[j].n.k))+')' : 'rgba('+base+','+((dark?.1:.14)*(1-d/150))+')';
            g.lineWidth = you ? 1.4 : 1;
            g.beginPath(); g.moveTo(P[i].x,P[i].y); g.lineTo(P[j].x,P[j].y); g.stroke();
          }
        }
      }
      P.forEach(function(p){
        if(p.n.you){
          g.fillStyle = 'rgba('+youCol+',.18)'; g.beginPath(); g.arc(p.x,p.y,14+Math.sin(t*3)*3,0,Math.PI*2); g.fill();
          g.fillStyle = 'rgb('+youCol+')';
        } else { g.fillStyle = 'rgba('+base+','+(dark?.3:.35)+')'; }
        g.beginPath(); g.arc(p.x,p.y,p.n.you?5:p.n.r,0,Math.PI*2); g.fill();
      });
    };
    var loop = function(now){ if(on){draw(now)} requestAnimationFrame(loop); };
    size();
    window.addEventListener('resize',size);
    new IntersectionObserver(function(e){on = e[0].isIntersecting}).observe(cn);
    requestAnimationFrame(loop);
    var form = cn.dataset.form ? $(cn.dataset.form) : null;
    if(form){
      form.addEventListener('cm:ok',function(){
        var cr = cn.getBoundingClientRect(), fr = (form.querySelector('[type="submit"]')||form).getBoundingClientRect();
        nodes.push({fx:.55 + Math.random()*.35, fy:.2 + Math.random()*.5, ph:0, r:5, you:true, k:0,
                    sx: fr.left - cr.left + fr.width/2, sy: fr.top - cr.top + fr.height/2});
      });
    }
  });

  /* ---------- colectivos: «órbita de personas» ----------
     Los colectivos orbitan alrededor del núcleo; por hilos curvos fluyen partículas
     de luz. Al entrar en pantalla se conectan uno a uno (nadie fuera). */
  var orbit = $('orbit');
  if(orbit && getComputedStyle(orbit).display !== 'none'){
    var oc = orbit.querySelector('.orbit-canvas'), og = oc.getContext('2d');
    var oD = Math.min(window.devicePixelRatio||1,2), oW=0, oH=0;
    var core = orbit.querySelector('.orbit-core');
    var cTitle = core.querySelector('.orbit-title'), cDesc = core.querySelector('.orbit-desc'), cK = core.querySelector('.orbit-k');
    var defTitle = cTitle.innerHTML, defDesc = cDesc.textContent, defK = cK.textContent;
    var oNodes = Array.prototype.map.call(orbit.querySelectorAll('.orbit-node'),function(el,i,all){
      return {el:el, base: -Math.PI/2 + i*(Math.PI*2/all.length), x:0, y:0, s:1, conn:0, lit:false,
              parts: Array.from({length:5},function(){return Math.random()})};
    });
    var oAng = 0, oSpeed = .06, oActive = -1, oStart = 0, oVisible = false, oStarted = false;
    var omx = 0, omy = 0, osx = 0, osy = 0;
    var oSize = function(){
      var r = orbit.getBoundingClientRect(); oW = r.width; oH = r.height;
      oc.width = oW*oD; oc.height = oH*oD; og.setTransform(oD,0,0,oD,0,0);
    };
    var setCore = function(i){
      core.classList.remove('swap'); void core.offsetWidth; core.classList.add('swap');
      if(i < 0){ cTitle.innerHTML = defTitle; cDesc.textContent = defDesc; cK.textContent = defK; }
      else {
        var n = oNodes[i].el;
        cK.textContent = 'Colectivo '+String(i+1).padStart(2,'0');
        cTitle.innerHTML = n.querySelector('span').textContent.replace(/(\S+)$/,'<em>$1</em>');
        cDesc.textContent = n.dataset.desc;
      }
    };
    var activate = function(i){
      if(oActive === i){return}
      oActive = i;
      orbit.classList.toggle('has-active', i > -1);
      oNodes.forEach(function(n,k){n.el.classList.toggle('active',k===i)});
      setCore(i);
    };
    oNodes.forEach(function(n,i){
      n.el.addEventListener('mouseenter',function(){activate(i)});
      n.el.addEventListener('focus',function(){activate(i)});
      n.el.addEventListener('mouseleave',function(){activate(-1)});
      n.el.addEventListener('blur',function(){activate(-1)});
      n.el.addEventListener('click',function(){activate(i)});
    });
    orbit.addEventListener('mousemove',function(e){var r = orbit.getBoundingClientRect(); omx = (e.clientX-r.left)/oW-.5; omy = (e.clientY-r.top)/oH-.5});
    orbit.addEventListener('mouseleave',function(){omx = omy = 0});

    // punto de una curva cuadrática
    var qp = function(t,ax,ay,bx,by,cx,cy){var u = 1-t; return [u*u*ax + 2*u*t*bx + t*t*cx, u*u*ay + 2*u*t*by + t*t*cy]};

    var oLast = 0;
    var oFrame = function(now){
      requestAnimationFrame(oFrame);
      if(!oVisible){oLast = now; return}
      var dt = Math.min(.05,(now - (oLast||now))/1000); oLast = now;
      var el = oStarted ? (now - oStart)/1000 : 0;
      // la órbita se frena al mirar un colectivo
      oSpeed = lerp(oSpeed, oActive > -1 || reduce ? 0 : .06, .06);
      oAng += oSpeed*dt;
      osx = lerp(osx, omx, .05); osy = lerp(osy, omy, .05);
      var cx = oW/2 + osx*30, cy = oH/2 + osy*20;
      var rx = Math.min(oW*.39, 540), ry = oH*.36;
      og.clearRect(0,0,oW,oH);

      // halo del núcleo
      var gl = og.createRadialGradient(cx,cy,0,cx,cy,ry*1.1);
      gl.addColorStop(0,'rgba(196,242,29,.10)'); gl.addColorStop(1,'rgba(196,242,29,0)');
      og.fillStyle = gl; og.fillRect(0,0,oW,oH);

      // anillo de la órbita
      og.strokeStyle = 'rgba(241,245,238,.07)'; og.lineWidth = 1;
      og.beginPath(); og.ellipse(cx,cy,rx,ry,0,0,Math.PI*2); og.stroke();

      oNodes.forEach(function(n,i){
        // entrada: cada colectivo se conecta a su turno
        var delay = .35 + i*.22;
        var target = oStarted ? clamp((el - delay)/.7,0,1) : 0;
        if(reduce && oStarted){target = 1}
        n.conn = target;
        if(target >= 1 && !n.lit){ n.lit = true; n.el.classList.add('on'); }
        var a = n.base + oAng;
        var depth = (Math.sin(a)+1)/2;                       // 0 = al fondo, 1 = delante
        var k = n.lit ? 1 : lerp(1.14, 1.05, target);        // «fuera» hasta conectarse
        n.x = cx + Math.cos(a)*rx*k; n.y = cy + Math.sin(a)*ry*k;
        n.s = .8 + depth*.35;
        n.el.style.transform = 'translate(-50%,-50%) translate('+n.x+'px,'+n.y+'px) scale('+n.s+')';
        n.el.style.zIndex = depth > .5 ? 4 : 2;

        // hilo curvo núcleo → colectivo
        var bx = (cx+n.x)/2 + (n.y-cy)*.18, by = (cy+n.y)/2 - (n.x-cx)*.18;
        var isA = oActive === i, dim = oActive > -1 && !isA;
        var steps = 40, upto = Math.round(steps*n.conn);
        if(upto > 0){
          og.strokeStyle = 'rgba(196,242,29,'+(isA ? .7 : dim ? .06 : (n.lit ? .22 : .35))+')';
          og.lineWidth = isA ? 1.8 : 1;
          og.beginPath(); og.moveTo(cx,cy);
          for(var s=1;s<=upto;s++){ var q = qp(s/steps,cx,cy,bx,by,n.x,n.y); og.lineTo(q[0],q[1]); }
          og.stroke();
          // cabeza de luz mientras se conecta
          if(!n.lit){ var h = qp(n.conn,cx,cy,bx,by,n.x,n.y); og.fillStyle = 'rgba(196,242,29,.95)'; og.beginPath(); og.arc(h[0],h[1],3.5,0,Math.PI*2); og.fill(); }
        }
        // partículas fluyendo hacia cada colectivo conectado
        if(n.lit && !reduce){
          var cnt = isA ? n.parts.length : 3;
          for(var pI=0;pI<cnt;pI++){
            n.parts[pI] = (n.parts[pI] + dt*(isA ? .55 : .3)) % 1;
            var pt = qp(n.parts[pI],cx,cy,bx,by,n.x,n.y);
            var al = Math.sin(n.parts[pI]*Math.PI);
            og.fillStyle = (pI%3===2 ? 'rgba(226,75,196,' : 'rgba(196,242,29,')+(al*(dim ? .15 : .9))+')';
            og.beginPath(); og.arc(pt[0],pt[1],isA ? 2.4 : 1.8,0,Math.PI*2); og.fill();
          }
        }
      });
    };
    oSize();
    window.addEventListener('resize',oSize);
    new IntersectionObserver(function(e){
      oVisible = e[0].isIntersecting;
      if(oVisible && !oStarted && e[0].intersectionRatio > .35){ oStarted = true; oStart = performance.now(); }
    },{threshold:[0,.35,.6]}).observe(orbit);
    requestAnimationFrame(oFrame);
  }

  /* ---------- internacional: «el mundo conectado» ----------
     Globo de puntos (los continentes salen de world-atlas), arcos de luz desde España
     hacia Europa e Iberoamérica, giro guiado por el scroll y arrastre con el ratón.
     Si el mapa no carga, se muestra la constelación plana (.intl-map). */
  var globe = $('globe');
  if(globe){
    var gc = globe.querySelector('.globe-canvas'), gx = gc.getContext('2d');
    var GD = Math.min(window.devicePixelRatio||1,2), GS = 0;
    var RAD = Math.PI/180;
    var gFail = function(){ globe.classList.add('fail'); };
    var loadScript = function(src){ return new Promise(function(res,rej){ var s = document.createElement('script'); s.src = src; s.onload = res; s.onerror = rej; document.head.appendChild(s); }); };

    // lugares (lat, lon)
    var ES = [40.42,-3.70];
    var sedes = [[41.33,2.08],[40.42,-3.70],[37.39,-5.99],[42.88,-8.54]];
    var places = [
      {ll:[50.85,4.35], g:'eu', label:'Europa · ALL DIGITAL'},
      {ll:[52.52,13.40], g:'eu2'}, {ll:[41.90,12.50], g:'eu2'}, {ll:[53.35,-6.26], g:'eu2'}, {ll:[52.23,21.01], g:'eu2', label:'Erasmus+'},
      {ll:[4.71,-74.07], g:'latam', label:'Iberoamérica'},
      {ll:[19.43,-99.13], g:'latam'}, {ll:[-12.05,-77.04], g:'latam'}, {ll:[-34.60,-58.38], g:'latam'}, {ll:[-33.45,-70.67], g:'latam'}
    ];
    // vistas: [lat0, lon0] del centro del globo
    var views = {all:[22,-28], eu:[44,6], eu2:[46,10], latam:[2,-52]};
    var vTarget = views.all.slice(), vNow = [10,-80];   // empieza girado y se acomoda
    var focus = 'all', land = [], gReady = false, gOn = false, gStart = 0, dragging = false, dragLast = null;

    var gSize = function(){
      var r = globe.getBoundingClientRect(); GS = r.width;
      gc.width = GS*GD; gc.height = GS*GD; gx.setTransform(GD,0,0,GD,0,0);
    };
    // proyección ortográfica
    var proj = function(lat,lon,alt){
      var la = lat*RAD, lo = (lon - vNow[1])*RAD, la0 = vNow[0]*RAD;
      var cosc = Math.sin(la0)*Math.sin(la) + Math.cos(la0)*Math.cos(la)*Math.cos(lo);
      var R = GS*.44*(alt||1);
      return {x: GS/2 + R*Math.cos(la)*Math.sin(lo), y: GS/2 - R*(Math.cos(la0)*Math.sin(la) - Math.sin(la0)*Math.cos(la)*Math.cos(lo)), z: cosc};
    };
    var toV = function(ll){ var la = ll[0]*RAD, lo = ll[1]*RAD; return [Math.cos(la)*Math.cos(lo), Math.cos(la)*Math.sin(lo), Math.sin(la)]; };
    var toLL = function(v){ return [Math.asin(Math.max(-1,Math.min(1,v[2])))/RAD, Math.atan2(v[1],v[0])/RAD]; };
    var slerp = function(a,b,t){
      var d = Math.acos(Math.max(-1,Math.min(1,a[0]*b[0]+a[1]*b[1]+a[2]*b[2])));
      if(d < 1e-6){return a}
      var s = Math.sin(d), k1 = Math.sin((1-t)*d)/s, k2 = Math.sin(t*d)/s;
      return [a[0]*k1+b[0]*k2, a[1]*k1+b[1]*k2, a[2]*k1+b[2]*k2];
    };
    var angDist = function(a,b){ var A = toV(a), B = toV(b); return Math.acos(Math.max(-1,Math.min(1,A[0]*B[0]+A[1]*B[1]+A[2]*B[2])))/RAD; };

    // arcos precalculados (lat/lon a lo largo del gran círculo)
    var arcs = places.map(function(p,i){
      var A = toV(ES), B = toV(p.ll), pts = [];
      for(var k=0;k<=48;k++){ pts.push(toLL(slerp(A,B,k/48))); }
      var len = angDist(ES,p.ll);
      return {p:p, pts:pts, h: .06 + len/180*.35, ph: Math.random(), order: i};
    });

    var buildLand = function(topo){
      var feat = topojson.feature(topo, topo.objects.land);
      var W = 720, H = 360, m = document.createElement('canvas'); m.width = W; m.height = H;
      var mg = m.getContext('2d'); mg.fillStyle = '#000';
      var polys = feat.type === 'FeatureCollection' ? feat.features.map(function(f){return f.geometry}) : [feat.geometry];
      polys.forEach(function(geom){
        var list = geom.type === 'Polygon' ? [geom.coordinates] : geom.coordinates;
        list.forEach(function(poly){
          // los polígonos que cruzan el antimeridiano se «desenrollan» y se pintan también desplazados 360°
          [-360,0,360].forEach(function(shift){
            mg.beginPath();
            poly.forEach(function(ring){
              var off = 0, prev = null;
              ring.forEach(function(c,i){
                if(prev !== null){ var d = c[0] - prev; if(d > 180){off -= 360} else if(d < -180){off += 360} }
                prev = c[0];
                var x = (c[0]+off+shift+180)*2, y = (90-c[1])*2;
                i ? mg.lineTo(x,y) : mg.moveTo(x,y);
              });
              mg.closePath();
            });
            mg.fill('evenodd');
          });
        });
      });
      var data = mg.getImageData(0,0,W,H).data;
      // puntos repartidos uniformemente por la esfera (espiral de Fibonacci)
      var N = 15000, gold = Math.PI*(3-Math.sqrt(5));
      for(var i=0;i<N;i++){
        var y = 1 - (i/(N-1))*2, r = Math.sqrt(1-y*y), th = gold*i;
        var lat = Math.asin(y)/RAD, lon = ((Math.atan2(Math.sin(th)*r, Math.cos(th)*r)/RAD)+540)%360-180;
        var px = Math.min(W-1,Math.floor((lon+180)*2)), py = Math.min(H-1,Math.floor((90-lat)*2));
        if(data[(py*W+px)*4+3] > 100){ land.push({lat:lat, lon:lon, d: angDist(ES,[lat,lon])}); }
      }
    };

    var gFrame = function(now){
      requestAnimationFrame(gFrame);
      if(!gOn || !gReady){return}
      var t = (now - gStart)/1000;
      // vista: se acerca a su objetivo, con un vaivén suave en reposo
      var sway = dragging || reduce ? 0 : Math.sin(t*.25)*4;
      vNow[0] = lerp(vNow[0], vTarget[0], dragging ? .25 : .045);
      vNow[1] = lerp(vNow[1], vTarget[1] + sway, dragging ? .25 : .045);
      gx.clearRect(0,0,GS,GS);
      var cx = GS/2, R = GS*.44;
      // atmósfera
      var at = gx.createRadialGradient(cx,cx,R*.85,cx,cx,R*1.18);
      at.addColorStop(0,'rgba(196,242,29,.10)'); at.addColorStop(1,'rgba(196,242,29,0)');
      gx.fillStyle = at; gx.beginPath(); gx.arc(cx,cx,R*1.18,0,Math.PI*2); gx.fill();
      var body = gx.createRadialGradient(cx-R*.35,cx-R*.4,R*.1,cx,cx,R);
      body.addColorStop(0,'rgba(38,90,67,.55)'); body.addColorStop(1,'rgba(11,21,16,.9)');
      gx.fillStyle = body; gx.beginPath(); gx.arc(cx,cx,R,0,Math.PI*2); gx.fill();
      gx.strokeStyle = 'rgba(196,242,29,.18)'; gx.lineWidth = 1; gx.stroke();

      // continentes: se encienden en onda desde España
      var wave = reduce ? 999 : t*95;
      for(var i=0;i<land.length;i++){
        var d = land[i];
        if(d.d > wave){continue}
        var p = proj(d.lat,d.lon);
        if(p.z <= 0){continue}
        var fresh = clamp((wave - d.d)/25,0,1);
        gx.fillStyle = 'rgba(196,242,29,'+(.18 + .62*p.z)*(.4 + .6*fresh)+')';
        var s = .9 + p.z*1.1;
        gx.fillRect(p.x - s/2, p.y - s/2, s, s);
      }

      // arcos de luz
      var arcStart = reduce ? -99 : 1.6;
      arcs.forEach(function(a,k){
        var prog = clamp((t - arcStart - a.order*.18)/1.1,0,1);
        if(prog <= 0){return}
        var on = focus === 'all' || focus === a.p.g || (focus === 'eu' && a.p.g === 'eu2');
        var upto = Math.round(48*prog), lastV = null;
        gx.lineWidth = on && focus !== 'all' ? 1.8 : 1.1;
        gx.strokeStyle = 'rgba('+(a.p.g==='latam'?'226,75,196':'196,242,29')+','+(on ? .75 : .12)+')';
        gx.beginPath();
        for(var s2=0;s2<=upto;s2++){
          var ll = a.pts[s2], alt = 1 + a.h*Math.sin(Math.PI*s2/48);
          var q = proj(ll[0],ll[1],alt);
          if(q.z < -.12){ lastV = null; continue; }
          lastV ? gx.lineTo(q.x,q.y) : gx.moveTo(q.x,q.y); lastV = q;
        }
        gx.stroke();
        // pulso que viaja por el arco
        if(prog >= 1 && !reduce){
          var ph = ((t*.35 + a.ph) % 1), idx = Math.floor(ph*48), ll2 = a.pts[idx];
          var q2 = proj(ll2[0],ll2[1],1 + a.h*Math.sin(Math.PI*idx/48));
          if(q2.z > -.12){ gx.fillStyle = on ? '#fff' : 'rgba(255,255,255,.3)'; gx.beginPath(); gx.arc(q2.x,q2.y,on?2.6:1.6,0,Math.PI*2); gx.fill(); }
        }
        // destino
        if(prog >= 1){
          var e = proj(a.p.ll[0],a.p.ll[1]);
          if(e.z > 0){
            gx.fillStyle = a.p.g==='latam' ? 'rgba(226,75,196,'+(on?1:.35)+')' : 'rgba(241,245,238,'+(on?1:.35)+')';
            gx.beginPath(); gx.arc(e.x,e.y,a.p.label?4.2:2.6,0,Math.PI*2); gx.fill();
            if(a.p.label && (focus === a.p.g || (focus === 'all' && a.p.g !== 'eu2'))){
              gx.font = '600 '+Math.round(clamp(GS/38,11,14))+'px Archivo, sans-serif';
              var tw = gx.measureText(a.p.label).width;
              gx.fillStyle = 'rgba(11,21,16,.75)'; gx.beginPath(); gx.roundRect ? gx.roundRect(e.x+10,e.y-11,tw+16,22,11) : gx.rect(e.x+10,e.y-11,tw+16,22); gx.fill();
              gx.fillStyle = '#F1F5EE'; gx.fillText(a.p.label,e.x+18,e.y+4.5);
            }
          }
        }
      });

      // España y sus sedes latiendo
      sedes.forEach(function(s3,i){
        var q = proj(s3[0],s3[1]); if(q.z <= 0){return}
        var pulse = reduce ? 0 : (Math.sin(t*2.4 + i*1.3)+1)/2;
        gx.fillStyle = 'rgba(196,242,29,'+(.15 + .25*pulse)+')'; gx.beginPath(); gx.arc(q.x,q.y,5 + pulse*5,0,Math.PI*2); gx.fill();
        gx.fillStyle = '#C4F21D'; gx.beginPath(); gx.arc(q.x,q.y,2.6,0,Math.PI*2); gx.fill();
      });
      var es = proj(ES[0],ES[1]);
      if(es.z > 0){
        gx.font = '700 '+Math.round(clamp(GS/34,12,16))+'px Archivo, sans-serif';
        gx.fillStyle = '#C4F21D'; gx.fillText('España · 4 sedes', es.x - 14, es.y + 26);
      }
    };

    var setFocus = function(k){
      focus = k || 'all';
      vTarget = (views[focus] || views.all).slice();
      document.querySelectorAll('.intl-list li[data-arc]').forEach(function(li){ li.classList.toggle('focus', li.dataset.arc === k); });
    };
    // el globo gira hacia la región de la que estás leyendo
    var items = document.querySelectorAll('.intl-list li[data-arc]');
    var seen = new Map();
    var liIO = new IntersectionObserver(function(entries){
      entries.forEach(function(en){ seen.set(en.target, en.isIntersecting); });
      var cur = null;
      items.forEach(function(li){ if(seen.get(li)){cur = li} });
      if(!dragging){ setFocus(cur ? cur.dataset.arc : 'all'); }
    },{rootMargin:'-45% 0px -45% 0px'});
    items.forEach(function(li){
      liIO.observe(li);
      li.addEventListener('mouseenter',function(){setFocus(li.dataset.arc)});
    });
    // arrastrar para girar
    globe.addEventListener('pointerdown',function(e){
      if(e.pointerType !== 'mouse'){return}
      dragging = true; dragLast = [e.clientX,e.clientY]; globe.classList.add('drag','touched'); e.preventDefault();
    });
    window.addEventListener('pointermove',function(e){
      if(!dragging){return}
      var dx = e.clientX - dragLast[0], dy = e.clientY - dragLast[1]; dragLast = [e.clientX,e.clientY];
      vTarget[1] -= dx*.35; vTarget[0] = clamp(vTarget[0] + dy*.35,-60,70);
    });
    window.addEventListener('pointerup',function(){ if(dragging){dragging = false; globe.classList.remove('drag')} });

    gSize();
    window.addEventListener('resize',gSize);
    new IntersectionObserver(function(e){
      gOn = e[0].isIntersecting;
      if(gOn && !gStart && gReady){ gStart = performance.now(); }
    },{threshold:.25}).observe(globe);
    requestAnimationFrame(gFrame);

    // carga del mapa (sin bloquear la página)
    (window.topojson ? Promise.resolve() : loadScript('https://cdn.jsdelivr.net/npm/topojson-client@3/dist/topojson-client.min.js'))
      .then(function(){ return fetch('https://cdn.jsdelivr.net/npm/world-atlas@2/land-110m.json'); })
      .then(function(r){ if(!r.ok){throw new Error('mapa')} return r.json(); })
      .then(function(topo){
        buildLand(topo);
        if(!land.length){throw new Error('sin puntos')}
        gReady = true; globe.classList.add('ready');
        if(gOn){ gStart = performance.now(); }
      })
      .catch(gFail);
  }

  /* ---------- carrusel de noticias ---------- */
  var rail = $('rail');
  if(rail){
    var railBar = $('railBar');
    var step = function(){var c = rail.querySelector('.card');return c ? c.getBoundingClientRect().width + 24 : 400};
    $('railPrev').addEventListener('click',function(){rail.scrollBy({left:-step(),behavior:'smooth'})});
    $('railNext').addEventListener('click',function(){rail.scrollBy({left:step(),behavior:'smooth'})});
    var updRail = function(){
      var max = rail.scrollWidth - rail.clientWidth;
      var p = max>0 ? rail.scrollLeft/max : 0;
      railBar.style.transform = 'translateX('+(p*400)+'%)';
    };
    rail.addEventListener('scroll',updRail,{passive:true});updRail();
    // arrastre con ratón (en táctil ya lo hace el scroll nativo)
    if(fine){
      var down=false,moved=false,sx=0,sl=0,lastX=0,lastT=0,vel=0,settleT=null;
      // sin arrastre nativo de imágenes ni selección de texto
      rail.querySelectorAll('img').forEach(function(im){im.draggable = false});
      rail.addEventListener('dragstart',function(e){e.preventDefault()});
      // posiciones de encaje de cada tarjeta
      var snaps = function(){
        var first = rail.firstElementChild.offsetLeft;
        var max = rail.scrollWidth - rail.clientWidth;
        return Array.prototype.map.call(rail.children,function(c){return Math.min(c.offsetLeft - first, max)});
      };
      rail.addEventListener('pointerdown',function(e){
        if(e.pointerType!=='mouse' || e.button!==0){return}
        e.preventDefault();
        clearTimeout(settleT);
        down=true;moved=false;sx=lastX=e.clientX;sl=rail.scrollLeft;lastT=performance.now();vel=0;
        rail.classList.add('drag');
      });
      window.addEventListener('pointermove',function(e){
        if(!down){return}
        var dx = e.clientX-sx, now = performance.now();
        if(Math.abs(dx)>4){moved=true}
        rail.scrollLeft = sl-dx;
        var dt = now-lastT;
        if(dt>0){vel = lerp(vel,(lastX-e.clientX)/dt,.4)}   // px/ms en sentido del scroll
        lastX = e.clientX; lastT = now;
      });
      var release = function(){
        if(!down){return}
        down=false;
        if(performance.now()-lastT > 80){vel = 0}          // se paró antes de soltar
        // inercia: proyectamos el movimiento y encajamos en la tarjeta más cercana a esa proyección
        var cur = rail.scrollLeft, proj = cur + vel*260;
        var pts = snaps(), start = sl, target = pts[0];
        pts.forEach(function(p){if(Math.abs(p-proj) < Math.abs(target-proj)){target = p}});
        // un tirón claro siempre avanza al menos una tarjeta en esa dirección
        var dragDist = cur - start;
        if(Math.abs(dragDist) > 40 && Math.abs(target - start) < 2){
          var dir = dragDist > 0 ? 1 : -1;
          var next = pts.filter(function(p){return dir>0 ? p>start+2 : p<start-2});
          if(next.length){target = dir>0 ? next[0] : next[next.length-1]}
        }
        rail.scrollTo({left:target,behavior:reduce?'auto':'smooth'});
        settleT = setTimeout(function(){rail.classList.remove('drag')},650);
      };
      window.addEventListener('pointerup',release);
      window.addEventListener('pointercancel',release);
      window.addEventListener('blur',release);
      // tras arrastrar, el clic al soltar no activa nada de las tarjetas
      rail.addEventListener('click',function(e){if(moved){e.preventDefault();e.stopPropagation();moved=false}},true);
    }
  }

  /* ---------- filtros (página de proyectos / recursos) ---------- */
  document.querySelectorAll('[data-filter-group]').forEach(function(group){
    var target = document.querySelector(group.dataset.filterGroup);
    group.querySelectorAll('button').forEach(function(btn){
      btn.addEventListener('click',function(){
        group.querySelectorAll('button').forEach(function(b){b.setAttribute('aria-pressed',b===btn?'true':'false')});
        var f = btn.dataset.filter;
        target.querySelectorAll('[data-cat]').forEach(function(item){
          item.hidden = f!=='all' && item.dataset.cat.split(' ').indexOf(f)<0;
        });
      });
    });
  });

  /* ---------- acordeón (preguntas frecuentes) ---------- */
  document.querySelectorAll('.faq details').forEach(function(d){
    d.addEventListener('toggle',function(){
      if(!d.open){return}
      d.parentElement.querySelectorAll('details').forEach(function(o){if(o!==d){o.open=false}});
    });
  });

  /* ---------- cursor, imán y vista previa ---------- */
  if(fine && !reduce){
    root.classList.add('has-cursor');
    var cur = document.querySelector('.cursor'), dot = document.querySelector('.cursor-dot');
    var label = cur.querySelector('span');
    var mx = innerWidth/2, my = innerHeight/2, cx = mx, cy = my, px = mx, py = my;
    var preview = $('progPreview');
    var pimgs = preview ? preview.querySelectorAll('img') : [];
    var inProg = false;
    window.addEventListener('mousemove',function(e){mx=e.clientX;my=e.clientY;dot.style.transform='translate3d('+mx+'px,'+my+'px,0)'});
    document.addEventListener('mouseleave',function(){cur.classList.add('is-hidden');dot.classList.add('is-hidden')});
    document.addEventListener('mouseenter',function(){cur.classList.remove('is-hidden');dot.classList.remove('is-hidden')});
    (function loop(){
      cx = lerp(cx,mx,.16); cy = lerp(cy,my,.16);
      px = lerp(px,mx,.1); py = lerp(py,my,.1);
      cur.style.transform = 'translate3d('+cx+'px,'+cy+'px,0)';
      if(inProg){preview.style.left = px+'px';preview.style.top = py+'px'}
      requestAnimationFrame(loop);
    })();
    document.querySelectorAll('a,button,input,textarea,select,summary,.news-rail').forEach(function(el){
      el.addEventListener('mouseenter',function(){
        if(el.classList.contains('news-rail')){label.textContent='Arrastra';cur.classList.add('is-view')}
        else{cur.classList.add('is-link')}
      });
      el.addEventListener('mouseleave',function(){cur.classList.remove('is-link','is-view')});
    });
    if(preview){
      document.querySelectorAll('.prog[data-img]').forEach(function(row){
        row.addEventListener('mouseenter',function(){
          inProg = true; preview.classList.add('on');
          cur.classList.remove('is-link');cur.classList.add('is-view');label.textContent='Ver';
          pimgs.forEach(function(im,i){im.classList.toggle('on',i===+row.dataset.img)});
        });
        row.addEventListener('mouseleave',function(){inProg=false;preview.classList.remove('on');cur.classList.remove('is-view')});
      });
    }
    document.querySelectorAll('.magnetic').forEach(function(b){
      b.addEventListener('mousemove',function(e){
        var r = b.getBoundingClientRect();
        var dx = e.clientX-(r.left+r.width/2), dy = e.clientY-(r.top+r.height/2);
        b.style.transition='transform .2s ease-out';
        b.style.transform='translate('+dx*.25+'px,'+dy*.35+'px)';
      });
      b.addEventListener('mouseleave',function(){b.style.transition='transform .8s cubic-bezier(.16,1,.3,1),color .5s,border-color .5s';b.style.transform=''});
    });
  }

  /* ---------- transformación digital: red de nodos ---------- */
  var net = $('txNet');
  if(net){
    var ctx = net.getContext('2d');
    var dpr = Math.min(window.devicePixelRatio||1,2);
    var W=0,H=0,nodes=[],netOn=true,nmx=-9999,nmy=-9999;
    var sizeNet = function(){
      var r = net.getBoundingClientRect();
      W = r.width; H = r.height;
      net.width = W*dpr; net.height = H*dpr; ctx.setTransform(dpr,0,0,dpr,0,0);
      var count = Math.round(clamp(W*H/16000,30,110));
      nodes = [];
      for(var i=0;i<count;i++){
        nodes.push({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.35,vy:(Math.random()-.5)*.35,
          c:Math.random()<.14?'206,11,165':'196,242,29',r:Math.random()*1.6+.8});
      }
    };
    var drawNet = function(){
      ctx.clearRect(0,0,W,H);
      var link = Math.min(150,W/7);
      for(var i=0;i<nodes.length;i++){
        var a = nodes[i];
        if(!reduce){
          a.x += a.vx; a.y += a.vy;
          if(a.x<0||a.x>W){a.vx*=-1} if(a.y<0||a.y>H){a.vy*=-1}
          var dx = nmx-a.x, dy = nmy-a.y, dm = Math.sqrt(dx*dx+dy*dy);
          if(dm<180){a.x -= dx/dm*.6; a.y -= dy/dm*.6}
        }
        for(var j=i+1;j<nodes.length;j++){
          var b = nodes[j], ex = a.x-b.x, ey = a.y-b.y, d = Math.sqrt(ex*ex+ey*ey);
          if(d<link){ctx.strokeStyle='rgba(196,242,29,'+(.16*(1-d/link))+')';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke()}
        }
        ctx.fillStyle='rgba('+a.c+',.85)';ctx.beginPath();ctx.arc(a.x,a.y,a.r,0,Math.PI*2);ctx.fill();
      }
    };
    var loopNet = function(){ if(netOn){drawNet()} if(!reduce){requestAnimationFrame(loopNet)} };
    sizeNet(); loopNet();
    window.addEventListener('resize',function(){sizeNet(); if(reduce){drawNet()}});
    new IntersectionObserver(function(e){netOn = e[0].isIntersecting}).observe(net);
    net.parentElement.addEventListener('mousemove',function(e){var r = net.getBoundingClientRect();nmx=e.clientX-r.left;nmy=e.clientY-r.top});
    net.parentElement.addEventListener('mouseleave',function(){nmx=nmy=-9999});
  }

  /* ---------- texto que se escribe solo ---------- */
  document.querySelectorAll('[data-type]').forEach(function(el){
    var txt = el.dataset.type;
    if(reduce){el.textContent = txt;return}
    var i = 0;
    setTimeout(function type(){
      el.textContent = txt.slice(0,++i);
      if(i<txt.length){setTimeout(type,38+Math.random()*50)}
    },1400);
  });

  /* ---------- terminal de DigitalizaciONG ---------- */
  var term = $('txTerm');
  if(term){
    var tlines = JSON.parse(term.dataset.lines);
    var esc = function(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;')};
    var fmt = function(s){
      s = esc(s);
      if(s.charAt(0)==='$'){return '<span class="cmd">'+s+'</span>'}
      if(s.charAt(0)==='✓'){return '<span class="ok">'+s+'</span>'}
      return s.replace(/ ok$/,' <span class="ok">ok</span>').replace(/(\[[█░]+\])/,'<span class="ok">$1</span>');
    };
    var runTerm = function(){
      if(reduce){term.innerHTML = tlines.map(fmt).join('\n');return}
      var li = 0, ci = 0, done = [];
      (function step(){
        var line = tlines[li];
        var isCmd = line.charAt(0)==='$';
        ci = isCmd ? ci+1 : line.length;
        term.innerHTML = done.concat(fmt(line.slice(0,ci))).join('\n');
        if(ci<line.length){setTimeout(step,28);return}
        done.push(fmt(line)); li++; ci = 0;
        if(li<tlines.length){setTimeout(step,isCmd?420:260+Math.random()*260)}
      })();
    };
    new IntersectionObserver(function(e,o){if(e[0].isIntersecting){o.disconnect();runTerm()}},{threshold:.4}).observe(term);
  }

  /* ---------- foco que sigue al cursor en tarjetas ---------- */
  document.querySelectorAll('.tx-card').forEach(function(card){
    card.addEventListener('mousemove',function(e){
      var r = card.getBoundingClientRect();
      card.style.setProperty('--mx',(e.clientX-r.left)+'px');
      card.style.setProperty('--my',(e.clientY-r.top)+'px');
    });
  });

  /* ---------- footer: año y foco sobre el logotipo ---------- */
  document.querySelectorAll('[data-year]').forEach(function(el){el.textContent = new Date().getFullYear()});
  // reloj en vivo de la sede (hora peninsular)
  var clocks = document.querySelectorAll('[data-clock]');
  if(clocks.length){
    var fmtClock = new Intl.DateTimeFormat('es-ES',{hour:'2-digit',minute:'2-digit',second:'2-digit',timeZone:'Europe/Madrid'});
    var tickClock = function(){var s = fmtClock.format(new Date());clocks.forEach(function(c){c.textContent = s})};
    tickClock(); setInterval(tickClock,1000);
  }
  var wm = document.querySelector('.wordmark');
  if(wm && fine){
    wm.addEventListener('mousemove',function(e){
      var r = wm.getBoundingClientRect();
      wm.style.setProperty('--mx',(e.clientX-r.left)+'px');
      wm.style.setProperty('--my',(e.clientY-r.top)+'px');
    });
  }

  /* ---------- formularios (sin backend todavía) ----------
     Validación con mensajes claros, estado de envío y confirmación.
     Para conectarlo a un servicio real, sustituir el setTimeout por la petición. */
  var errorFor = function(field){
    var v = field.validity;
    if(field.type==='checkbox'){return 'Acepta la política de privacidad para continuar.'}
    if(v.valueMissing){return field.type==='email' ? 'Escribe tu correo electrónico.' : 'Este campo es obligatorio.'}
    if(v.typeMismatch){return 'Revisa el formato del correo (ej.: nombre@dominio.com).'}
    return 'Revisa este campo.';
  };
  document.querySelectorAll('form[data-msg]').forEach(function(form){
    var note = form.parentElement.querySelector('.form-note');
    var btn = form.querySelector('[type="submit"]');
    var say = function(msg,kind){
      if(!note){return}
      note.textContent = msg;
      note.classList.toggle('ok',kind==='ok');
      note.classList.toggle('err',kind==='err');
      note.setAttribute('role',kind==='err'?'alert':'status');
    };
    // al corregir un campo, se limpia su error
    form.addEventListener('input',function(e){
      if(e.target.getAttribute('aria-invalid')==='true' && e.target.checkValidity()){
        e.target.removeAttribute('aria-invalid');
        if(!form.querySelector('[aria-invalid="true"]')){say('','')}
      }
    });
    form.addEventListener('change',function(e){if(e.target.type==='checkbox' && e.target.checked){e.target.removeAttribute('aria-invalid')}});
    form.addEventListener('submit',function(e){
      e.preventDefault();
      var fields = Array.prototype.slice.call(form.elements).filter(function(f){return f.willValidate});
      var bad = null;
      fields.forEach(function(f){
        var ok = f.checkValidity();
        if(ok){f.removeAttribute('aria-invalid')}
        else{f.setAttribute('aria-invalid','true'); if(!bad){bad = f}}
      });
      if(bad){say(errorFor(bad),'err');bad.focus();return}
      if(btn){btn.classList.add('is-loading');btn.disabled = true;btn.setAttribute('aria-busy','true')}
      say('','');
      setTimeout(function(){
        if(btn){btn.classList.remove('is-loading');btn.disabled = false;btn.removeAttribute('aria-busy')}
        say(form.dataset.msg,'ok');
        form.reset();
        form.dispatchEvent(new CustomEvent('cm:ok'));
      },900);
    });
  });

  /* ---------- panel de cookies ----------
     La web aún no usa analítica, así que el panel no se abre solo.
     Cuando se instale, poner COOKIE_AUTO = true para pedir consentimiento en la primera visita
     y leer localStorage 'cm-cookies' ('all' | 'necessary' | 'custom:analytics') antes de cargarla. */
  var COOKIE_AUTO = false;
  var ck = $('cookies');
  if(ck){
    var ckAnalytics = $('ckAnalytics');
    var readCk = function(){try{return localStorage.getItem('cm-cookies')}catch(err){return null}};
    var saveCk = function(v){try{localStorage.setItem('cm-cookies',v)}catch(err){}};
    var lastFocus = null;
    var openCk = function(){
      var cur = readCk();
      ckAnalytics.checked = cur==='all' || cur==='custom:analytics';
      lastFocus = document.activeElement;
      ck.hidden = false;
      requestAnimationFrame(function(){ck.classList.add('on')});
      ck.querySelector('[data-cookie="all"]').focus({preventScroll:true});
    };
    var closeCk = function(){
      ck.classList.remove('on');
      setTimeout(function(){ck.hidden = true},450);
      if(lastFocus && lastFocus.focus){lastFocus.focus({preventScroll:true})}
    };
    ck.querySelectorAll('[data-cookie]').forEach(function(b){
      b.addEventListener('click',function(){
        var k = b.dataset.cookie;
        saveCk(k==='all' ? 'all' : k==='necessary' ? 'necessary' : (ckAnalytics.checked ? 'custom:analytics' : 'necessary'));
        closeCk();
      });
    });
    document.querySelectorAll('[data-cookie-open]').forEach(function(b){b.addEventListener('click',openCk)});
    document.addEventListener('keydown',function(e){if(e.key==='Escape' && !ck.hidden){closeCk()}});
    if(COOKIE_AUTO && !readCk()){setTimeout(openCk,2500)}
  }

  /* ---------- acceso rápido en móvil ----------
     Aparece tras la primera pantalla y se retira cuando el footer (que ya tiene
     estos datos) está a la vista o el menú está abierto. */
  var qb = $('quickbar');
  if(qb){
    var footVisible = false;
    if(footer){new IntersectionObserver(function(en){footVisible = en[0].isIntersecting;updQb()}).observe(footer)}
    var updQb = function(){
      var y2 = lenis ? lenis.scroll : window.scrollY;
      qb.classList.toggle('on', y2 > window.innerHeight*.6 && !footVisible && !mmenu.classList.contains('open'));
    };
    window.addEventListener('scroll',updQb,{passive:true});
    burger.addEventListener('click',updQb);
    updQb();
  }
})();
