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
  var scrollToTarget = function(el){
    if(lenis){lenis.scrollTo(el,{offset:-90,duration:1.6})}
    else{var y = el===0?0:el.getBoundingClientRect().top+window.scrollY-90;window.scrollTo({top:y,behavior:reduce?'auto':'smooth'})}
  };

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
      if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target)}
    });
  },{rootMargin:'0px 0px -12% 0px'});
  document.querySelectorAll('[data-reveal],[data-lines],[data-clip]').forEach(function(el){io.observe(el)});

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
        tk._x += sp*(1.2 + Math.abs(vel)*.6);
        if(tk._x < -w){tk._x += w}
        if(tk._x > 0){tk._x -= w}
        tk.style.transform = 'translate3d('+tk._x+'px,0,0)';
      });
    }

    onScrollNav(y);
    requestAnimationFrame(frame);
  };
  requestAnimationFrame(frame);

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
    if(fine){
      var down=false,sx=0,sl=0;
      rail.addEventListener('pointerdown',function(e){if(e.pointerType!=='mouse'){return}down=true;sx=e.clientX;sl=rail.scrollLeft});
      window.addEventListener('pointermove',function(e){if(!down){return}var dx=e.clientX-sx;if(Math.abs(dx)>4){rail.classList.add('drag')}rail.scrollLeft=sl-dx});
      window.addEventListener('pointerup',function(){if(!down){return}down=false;rail.classList.remove('drag')});
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

  /* ---------- formularios (sin backend todavía) ---------- */
  document.querySelectorAll('form[data-msg]').forEach(function(form){
    var note = form.parentElement.querySelector('.form-note');
    form.addEventListener('submit',function(e){
      e.preventDefault();
      if(note){note.textContent = form.dataset.msg;note.classList.add('ok')}
      form.reset();
    });
  });
})();
