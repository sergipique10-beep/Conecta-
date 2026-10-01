"""Generador de las páginas de fundación conecta+.

Escribe las páginas internas (nosotros, mision, proyectos, recursos, contacto,
equipo, transformacion-digital) a partir de las plantillas de este archivo y
sustituye el menú (NAV) y el pie (FOOTER) de index.html, que comparten todas.

Uso, desde la raíz del repositorio:
    python tools/build_pages.py

Importante: las páginas internas se SOBRESCRIBEN. Si cambias su contenido,
cámbialo aquí y vuelve a ejecutar el script; no edites esos .html a mano.
index.html es la excepción: se edita a mano salvo su NAV y su FOOTER.
"""
# Genera las páginas internas de conecta+ con cabecera y pie compartidos.
import io, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HEAD = '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0B1510">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300..800&family=Fredoka:wght@500..700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<script>document.documentElement.classList.add('js')</script>
<link rel="stylesheet" href="css/site.css">
</head>
<body>
'''

CHROME = '''
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="sym" viewBox="0 0 64 64">
    <circle cx="21" cy="15" r="8" fill="var(--tec)"/>
    <rect x="8" y="26" width="26" height="30" rx="13" fill="var(--tec)"/>
    <g transform="rotate(180 32 32)">
      <circle cx="21" cy="15" r="8" fill="var(--mag-solid)"/>
      <rect x="8" y="26" width="26" height="30" rx="13" fill="var(--mag-solid)"/>
    </g>
  </symbol>
</svg>

<div class="grain" aria-hidden="true"></div>
<div class="cursor" aria-hidden="true"><span>Ver</span></div>
<div class="cursor-dot" aria-hidden="true"></div>
<div class="curtain" id="curtain" aria-hidden="true"><svg><use href="#sym"/></svg></div>
'''

NAV = '''<!-- ============ NAV ============ -->
<header class="nav" id="nav">
  <div class="nav-bar">
    <a class="logo" href="index.html" aria-label="fundación conecta+, inicio">
      <svg aria-hidden="true"><use href="#sym"/></svg>
      <span><b>conecta</b><i>+</i></span>
    </a>
    <ul class="nav-links">
      <li class="has-drop">
        <a href="nosotros.html" aria-haspopup="true">Nosotros</a>
        <div class="drop"><div class="drop-panel"><ul>
          <li><a href="nosotros.html#quienes-somos">Quiénes somos</a></li>
          <li><a href="nosotros.html#historia">Historia</a></li>
          <li><a href="equipo.html">Equipo y patronato</a></li>
          <li><a href="nosotros.html#colaboraciones">Colaboraciones</a></li>
        </ul></div></div>
      </li>
      <li class="has-drop">
        <a href="mision.html" aria-haspopup="true">Misión</a>
        <div class="drop"><div class="drop-panel"><ul>
          <li><a href="mision.html#tercer-sector">Tercer sector</a></li>
          <li><a href="transformacion-digital.html">Transformación digital e innovación</a></li>
          <li><a href="mision.html#voluntariado">Voluntariado</a></li>
          <li><a href="mision.html#justicia-educativa">Justicia educativa</a></li>
          <li><a href="mision.html#inclusion-digital">Inclusión digital</a></li>
          <li><a href="mision.html#formacion-tic">Formación TIC e inserción laboral</a></li>
          <li><a href="mision.html#liderazgo-juvenil">Participación y liderazgo juvenil</a></li>
        </ul></div></div>
      </li>
      <li class="has-drop">
        <a href="proyectos.html" aria-haspopup="true">Proyectos</a>
        <div class="drop"><div class="drop-panel">
          <ul>
            <li><a href="proyectos.html#nacionales">Proyectos nacionales</a></li>
            <li><a href="proyectos.html#internacionales">Proyectos internacionales</a></li>
          </ul>
        </div></div>
      </li>
      <li class="has-drop">
        <a href="recursos.html" aria-haspopup="true">Recursos</a>
        <div class="drop"><div class="drop-panel"><ul>
          <li><a href="recursos.html#blog">Blog y noticias</a></li>
          <li><a href="recursos.html#publicaciones">Publicaciones</a></li>
          <li><a href="recursos.html#transparencia">Transparencia</a></li>
          <li><a href="recursos.html#campus">Campus Virtual</a></li>
        </ul></div></div>
      </li>
      <li><a href="contacto.html">Contacto</a></li>
    </ul>
    <a class="btn btn-tec nav-cta magnetic" href="contacto.html#participa">Únete a la red <span class="arr">→</span></a>
    <button class="burger" id="burger" aria-expanded="false" aria-controls="mmenu" aria-label="Abrir menú"><div><span></span><span></span></div></button>
  </div>
</header>

<div class="mmenu" id="mmenu">
  <a class="big" href="nosotros.html">Nosotros</a>
  <div class="subs"><a href="nosotros.html#quienes-somos">Quiénes somos</a><a href="nosotros.html#historia">Historia</a><a href="equipo.html">Equipo y patronato</a><a href="nosotros.html#colaboraciones">Colaboraciones</a></div>
  <a class="big" href="mision.html"><em>Misión</em></a>
  <div class="subs"><a href="mision.html#tercer-sector">Tercer sector</a><a href="transformacion-digital.html">Transformación digital</a><a href="mision.html#voluntariado">Voluntariado</a><a href="mision.html#justicia-educativa">Justicia educativa</a><a href="mision.html#inclusion-digital">Inclusión digital</a><a href="mision.html#formacion-tic">Formación TIC</a><a href="mision.html#liderazgo-juvenil">Liderazgo juvenil</a></div>
  <a class="big" href="proyectos.html">Proyectos</a>
  <div class="subs"><a href="proyectos.html#nacionales">Nacionales</a><a href="proyectos.html#internacionales">Internacionales</a></div>
  <a class="big" href="recursos.html">Recursos</a>
  <div class="subs"><a href="recursos.html#blog">Blog</a><a href="recursos.html#publicaciones">Publicaciones</a><a href="recursos.html#transparencia">Transparencia</a><a href="recursos.html#campus">Campus Virtual</a></div>
  <a class="big" href="contacto.html">Contacto</a>
  <a class="btn btn-tec" href="contacto.html#participa">Únete a la red <span class="arr">→</span></a>
</div>
'''

FOOTER = '''<!-- ============ FOOTER ============ -->
<footer id="footer">
  <div class="fc-bg" aria-hidden="true"></div>
  <div class="foot-inner">
    <div class="fc-top wrap">
      <a class="fc-id" href="index.html" aria-label="fundación conecta+, inicio"><svg aria-hidden="true"><use href="#sym"/></svg><span>Fundación conecta+</span></a>
      <span class="fc-clock"><i aria-hidden="true"></i>El Prat de Llobregat <time data-clock>--:--:--</time></span>
    </div>

    <div class="fc-center wrap">
      <p class="fc-kicker">Que nadie quede fuera del mundo digital.</p>
      <a class="fc-big" href="contacto.html#escribenos">¿<em>Conectamos</em>?</a>
      <div class="fc-actions">
        <a class="btn btn-tec magnetic" href="contacto.html#escribenos">Escríbenos <span class="arr">→</span></a>
        <a class="btn btn-ghost magnetic" href="mailto:info@conectamas.org">info@conectamas.org</a>
      </div>
    </div>

    <div class="fc-panel">
      <div class="fc-brand">
        <div class="wordmark" aria-hidden="true">
          <span class="wm-base"><span>c</span><span>o</span><span>n</span><span>e</span><span>c</span><span>t</span><span>a</span><span class="plus">+</span></span>
          <span class="wm-glow">conecta+</span>
        </div>
        <p>Educación, inclusión digital y acción social desde 1995.</p>
        <address><a href="tel:+34934745546">934 745 546</a> · C/ Riu Anoia, 42-54, El Prat<br><span>Madrid · Andalucía · Galicia</span></address>
      </div>
      <div class="fc-col" role="navigation" aria-label="Organización">
        <h4>Organización</h4>
        <ul>
          <li><a class="roll" href="nosotros.html"><span class="rl"><span>Quiénes somos</span></span></a></li>
          <li><a class="roll" href="equipo.html"><span class="rl"><span>Equipo y patronato</span></span></a></li>
          <li><a class="roll" href="recursos.html#transparencia"><span class="rl"><span>Transparencia</span></span></a></li>
          <li><a class="roll" href="recursos.html#publicaciones"><span class="rl"><span>Memoria anual</span></span></a></li>
        </ul>
      </div>
      <div class="fc-col" role="navigation" aria-label="Explora">
        <h4>Explora</h4>
        <ul>
          <li><a class="roll" href="mision.html"><span class="rl"><span>Misión</span></span></a></li>
          <li><a class="roll" href="transformacion-digital.html"><span class="rl"><span>Transformación digital</span></span></a></li>
          <li><a class="roll" href="proyectos.html"><span class="rl"><span>Proyectos</span></span></a></li>
          <li><a class="roll" href="recursos.html#campus"><span class="rl"><span>Campus Virtual</span></span></a></li>
        </ul>
      </div>
      <div class="fc-news">
        <h4>Newsletter</h4>
        <form class="foot-form" novalidate data-msg="¡Gracias! Te hemos enviado un correo para confirmar la suscripción.">
          <label for="footMail" class="sr-only">Correo electrónico para la newsletter</label>
          <div class="foot-form-row">
            <input id="footMail" type="email" placeholder="tu@email.com" required autocomplete="email">
            <button type="submit" aria-label="Suscribirme">→</button>
          </div>
          <p class="foot-privacy">Un correo al mes, sin spam. Al suscribirte aceptas la <a href="#">política de privacidad</a>.</p>
        </form>
        <p class="form-note" aria-live="polite"></p>
        <div class="foot-trust">
          <a href="recursos.html#transparencia">ENS</a><a href="recursos.html#transparencia">ISO 9001</a><a href="recursos.html#transparencia">ISO 14001</a><a href="recursos.html#transparencia">ISO 27001</a><a href="proyectos.html#internacionales">ALL DIGITAL</a><a href="proyectos.html#internacionales">Erasmus+</a>
        </div>
      </div>

      <div class="fc-legal">
        <span>© <span data-year>2026</span> Fundación Conecta+</span>
        <nav aria-label="Legal"><a href="#">Aviso legal</a><a href="#">Privacidad</a><a href="#">Cookies</a><button type="button" class="link-btn" data-cookie-open>Configurar cookies</button><a href="#">Accesibilidad</a><a href="#">Canal ético</a></nav>
        <div class="foot-social">
          <a href="#" aria-label="Instagram"><svg width="15" height="15" viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="18" height="18" rx="5" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="1.6"/><circle cx="17.2" cy="6.8" r="1" fill="currentColor"/></svg></a>
          <a href="#" aria-label="LinkedIn"><svg width="15" height="15" viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="18" height="18" rx="3" stroke="currentColor" stroke-width="1.6"/><line x1="7.5" y1="10" x2="7.5" y2="17" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="7.5" cy="7" r="1" fill="currentColor"/><path d="M11.5 17v-4.2c0-1.3 1-2.3 2.3-2.3s2.2 1 2.2 2.3V17" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></a>
          <a href="#" aria-label="X / Twitter"><svg width="15" height="15" viewBox="0 0 24 24" fill="none"><path d="M4 4l16 16M20 4L4 20" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></a>
        </div>
        <a class="to-top" href="#top" aria-label="Volver arriba">
          <svg viewBox="0 0 100 100" aria-hidden="true"><defs><path id="topCircle" d="M50,50 m-37,0 a37,37 0 1,1 74,0 a37,37 0 1,1 -74,0"/></defs><text><textPath href="#topCircle" textLength="230" lengthAdjust="spacing">volver arriba · volver arriba · </textPath></text></svg>
          <b aria-hidden="true">↑</b>
        </a>
      </div>
    </div>
  </div>
</footer>

<!-- acceso rápido en móvil -->
<nav class="quickbar" id="quickbar" aria-label="Acceso rápido">
  <a href="tel:+34934745546"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>Llamar</a>
  <a href="contacto.html#escribenos"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>Escribir</a>
  <a href="https://www.google.com/maps/search/?api=1&amp;query=C%2F%20Riu%20Anoia%2042-54%2C%2008820%20El%20Prat%20de%20Llobregat" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/></svg>Cómo llegar</a>
</nav>

<!-- panel de cookies -->
<div class="cookies" id="cookies" role="dialog" aria-modal="false" aria-labelledby="cookiesTitle" hidden>
  <p class="cookies-title" id="cookiesTitle">Tu privacidad</p>
  <p>Usamos cookies técnicas necesarias para que la web funcione. Con tu permiso, usaríamos también cookies analíticas para mejorarla.</p>
  <div class="cookies-opts">
    <label class="cookie-opt"><input type="checkbox" checked disabled><span><b>Necesarias</b>Siempre activas</span></label>
    <label class="cookie-opt"><input type="checkbox" id="ckAnalytics"><span><b>Analíticas</b>Medir visitas de forma anónima</span></label>
  </div>
  <div class="cookies-actions">
    <button type="button" class="btn btn-ghost" data-cookie="necessary">Solo necesarias</button>
    <button type="button" class="btn btn-ghost" data-cookie="save">Guardar selección</button>
    <button type="button" class="btn btn-tec" data-cookie="all">Aceptar todas</button>
  </div>
</div>

'''

TAIL = '''
<script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>
<script src="js/site.js"></script>
</body>
</html>
'''

def page_hero(crumb, l1, l2, lede, img, anchors, pos='center', media=None, cls=''):
    a = ''.join('<a href="#%s">%s</a>' % (h, t) for h, t in anchors)
    media_html = media or f'    <div class="hero-media"><img src="img/{img}" alt="" fetchpriority="high" style="object-position:{pos}"></div>\n'
    return f'''  <section class="page-hero{cls}" aria-labelledby="page-h">
{media_html}    <div class="wrap">
      <nav class="crumbs fade-up" aria-label="Ruta"><a href="index.html">Inicio</a><span aria-hidden="true">/</span>{crumb if '<' in crumb else '<span>' + crumb + '</span>'}</nav>
      <h1 id="page-h"><span class="line"><span>{l1}</span></span><span class="line"><span>{l2}</span></span></h1>
      <div class="page-hero-foot fade-up">
        <p>{lede}</p>
        <div class="anchors">{a}</div>
      </div>
    </div>
  </section>
'''

def head2(kicker, l1, l2, p=None, hid=None):
    idattr = f' id="{hid}"' if hid else ''
    para = f'\n        <p data-reveal>{p}</p>' if p else ''
    return f'''      <div class="head">
        <div>
          <span class="kicker">{kicker}</span>
          <h2 class="h2"{idattr} data-lines style="margin-top:22px"><span class="line"><span>{l1}</span></span><span class="line"><span>{l2}</span></span></h2>
        </div>{para}
      </div>
'''

def next_link(href, kicker, l):
    return f'''  <a class="next" href="{href}">
    <div class="wrap">
      <span class="kicker">{kicker}</span>
      <strong>{l} <i aria-hidden="true">→</i></strong>
    </div>
  </a>
'''

def write(name, title, desc, body, parent=None, extra_head=''):
    head = HEAD.format(title=title, desc=desc)
    if extra_head:
        head = head.replace('</head>', extra_head + '\n</head>')
    if parent:  # marca la sección padre como activa en el menú
        head = head.replace('<body>', f'<body data-parent="{parent}">')
    html = head + CHROME + '\n' + NAV + '\n<main id="top">\n' + body + '</main>\n\n' + FOOTER + TAIL
    io.open(os.path.join(ROOT, name), 'w', encoding='utf-8', newline='\n').write(html)
    print('wrote', name)

# Escenas del showreel de la cabecera de Misión: (ancla de la línea, rótulo, archivo en video/ sin extensión)
REEL = [
    ('voluntariado', 'Voluntariado', 'mision-voluntariado'),
    ('transformacion-digital', 'Transformación digital', 'mision-transformacion'),
    ('justicia-educativa', 'Justicia educativa', 'mision-justicia'),
    ('inclusion-digital', 'Inclusión digital', 'mision-inclusion'),
    ('formacion-tic', 'Formación TIC', 'mision-formacion'),
    ('liderazgo-juvenil', 'Liderazgo juvenil', 'mision-liderazgo'),
]
_reel_items = ''.join(f'<li data-src="video/{v}.mp4" data-poster="video/{v}.jpg" data-href="{h}" data-label="{t}"></li>' for h, t, v in REEL)
_reel_bars = ''.join('<i><b></b></i>' for _ in REEL)
MISION_MEDIA = f'''    <div class="hero-media reel" id="reel" aria-hidden="true">
      <video class="reel-v on" muted playsinline preload="auto" poster="video/{REEL[0][2]}.jpg"></video>
      <video class="reel-v" muted playsinline preload="auto"></video>
      <span class="reel-grade"></span>
      <ul class="reel-list" hidden>{_reel_items}</ul>
    </div>
    <a class="reel-cap" id="reelCap" href="#{REEL[0][0]}">
      <span class="reel-bars" aria-hidden="true">{_reel_bars}</span>
      <span class="reel-meta"><span class="reel-n">01 / {len(REEL):02d}</span><b class="reel-t">{REEL[0][1]}</b><span class="reel-go">Ver línea →</span></span>
    </a>
'''
# Cabecera de Proyectos: vídeo de la ciudad (color de marca ya horneado en el archivo) + arcos
PROY_MEDIA = '''    <div class="hero-media city" aria-hidden="true">
      <video class="city-v" muted playsinline loop autoplay preload="auto" poster="video/proyectos-ciudad.jpg"><source src="video/proyectos-ciudad.mp4" type="video/mp4"></video>
      <span class="city-grade"></span>
      <canvas class="city-arcs" id="cityArcs"></canvas>
    </div>
'''

# ------------------------------------------------------------------ NOSOTROS
nosotros = page_hero('Nosotros', 'Somos', '<em>conecta+.</em>',
    'Una fundación que lleva desde 1995 tendiendo puentes entre la tecnología y las personas que más lo necesitan.',
    'news-internacional.jpg',
    [('quienes-somos','Quiénes somos'),('historia','Historia'),('valores','Valores'),('equipos','Equipos'),('colaboraciones','Colaboraciones')], 'center 40%')
nosotros += '''
  <section class="pad" id="quienes-somos" aria-labelledby="qs-h">
    <div class="wrap split">
      <div class="prose">
        <span class="kicker">Quiénes somos</span>
        <h2 class="h2" id="qs-h" data-lines><span class="line"><span>Tecnología con</span></span><span class="line"><span><em>propósito social.</em></span></span></h2>
        <p class="big" data-reveal>Somos una entidad sin ánimo de lucro dedicada a la educación, la inclusión digital y la acción social.</p>
        <p data-reveal>Trabajamos para que la tecnología sea una vía real de participación, aprendizaje y derechos — no una barrera más. Lo hacemos desde la proximidad: escuchando a las comunidades, diseñando con ellas y acompañándolas en el tiempo.</p>
        <p data-reveal>Nuestro trabajo se sostiene sobre tres verbos: participar, aprender y transformar.</p>
      </div>
      <div class="split-media" data-clip><img src="img/vinculo-manos.avif" alt="Dos manos digitales a punto de tocarse" loading="lazy"></div>
    </div>
  </section>

  <section aria-label="Cifras">
    <div class="stats">
      <div class="stat" data-reveal><b><span data-count="1995">0</span></b><span>año de nacimiento de la fundación</span></div>
      <div class="stat" data-reveal style="--d:.08s"><b><span data-count="4">0</span></b><span>sedes: Andalucía, Madrid, Cataluña y Galicia</span></div>
      <div class="stat" data-reveal style="--d:.16s"><b><span data-count="7">0</span></b><span>líneas de trabajo</span></div>
      <div class="stat" data-reveal style="--d:.24s"><b><span data-count="8">0</span></b><span>colectivos con los que trabajamos</span></div>
    </div>
  </section>

  <section class="pad" id="historia" aria-labelledby="hist-h">
    <div class="wrap">
''' + head2('Historia', 'Tres décadas', '<em>conectando.</em>', 'De una pequeña iniciativa a una red con presencia en cuatro comunidades autónomas y en proyectos europeos e iberoamericanos.', 'hist-h') + '''      <div class="timeline">
        <div class="tl" data-reveal><b>1995</b><h3>Nace conecta+</h3><p>La fundación arranca con una idea sencilla: que el acceso a la tecnología no dependa del lugar donde naces ni de tus recursos.</p></div>
        <div class="tl" data-reveal><b>Red</b><h3>Presencia en cuatro territorios</h3><p>Abrimos sedes en Andalucía, Madrid, Cataluña y Galicia para trabajar cerca de cada comunidad.</p></div>
        <div class="tl" data-reveal><b>Europa</b><h3>Una red que cruza fronteras</h3><p>Nos sumamos a ALL DIGITAL, a La Liga Iberoamericana y a proyectos Erasmus+ para ampliar nuestro impacto.</p></div>
        <div class="tl" data-reveal><b>Calidad</b><h3>Certificados en lo que importa</h3><p>Contamos con las normas ISO 9001, ISO 14001 e ISO 27001 y con el Esquema Nacional de Seguridad (ENS).</p></div>
        <div class="tl" data-reveal><b>Hoy</b><h3>Siete líneas, un propósito</h3><p>Seguimos trabajando para que nadie quede fuera del mundo digital.</p></div>
      </div>
    </div>
  </section>

  <section class="pad values-sec" id="valores" aria-labelledby="val-h">
    <div class="wrap">
''' + head2('Valores', 'Lo que nos', '<em>mueve.</em>', 'Seis ideas que guían cada proyecto, cada formación y cada decisión de la fundación.', 'val-h') + '''      <div class="values">
        <article class="value" data-reveal style="--d:0.00s">
          <img src="img/news-internacional.jpg" alt="" loading="lazy">
          <div class="value-top"><span class="n">01</span><svg class="sym" aria-hidden="true"><use href="#sym"/></svg></div>
          <div class="value-body"><h3>Participar</h3><p>Impulsamos el liderazgo juvenil y el voluntariado como motor de comunidades activas.</p></div>
        </article>
        <article class="value" data-reveal style="--d:0.08s">
          <img src="img/news-formacion.jpg" alt="" loading="lazy">
          <div class="value-top"><span class="n">02</span><svg class="sym" aria-hidden="true"><use href="#sym"/></svg></div>
          <div class="value-body"><h3>Aprender</h3><p>Formación TIC y digital al alcance de todas las edades y colectivos.</p></div>
        </article>
        <article class="value" data-reveal style="--d:0.16s">
          <img src="img/tech.jpg" alt="" loading="lazy">
          <div class="value-top"><span class="n">03</span><svg class="sym" aria-hidden="true"><use href="#sym"/></svg></div>
          <div class="value-body"><h3>Transformar</h3><p>Convertimos el conocimiento en oportunidades reales de inclusión y justicia educativa.</p></div>
        </article>
        <article class="value" data-reveal style="--d:0.00s">
          <img src="img/news-voluntariado.jpg" alt="" loading="lazy">
          <div class="value-top"><span class="n">04</span><svg class="sym" aria-hidden="true"><use href="#sym"/></svg></div>
          <div class="value-body"><h3>Proximidad</h3><p>Diseñamos cada programa desde la escucha a las personas con las que trabajamos.</p></div>
        </article>
        <article class="value" data-reveal style="--d:0.08s">
          <img src="img/conecta.jpg" alt="" loading="lazy">
          <div class="value-top"><span class="n">05</span><svg class="sym" aria-hidden="true"><use href="#sym"/></svg></div>
          <div class="value-body"><h3>Transparencia</h3><p>Rendimos cuentas de lo que hacemos y de cómo lo hacemos.</p></div>
        </article>
        <article class="value" data-reveal style="--d:0.16s">
          <img src="img/news-ens.jpg" alt="" loading="lazy">
          <div class="value-top"><span class="n">06</span><svg class="sym" aria-hidden="true"><use href="#sym"/></svg></div>
          <div class="value-body"><h3>Calidad</h3><p>Procesos certificados y seguros para cuidar a las personas y sus datos.</p></div>
        </article>
      </div>
    </div>
  </section>

  <section class="pad" id="equipos" aria-labelledby="eq-h">
    <div class="wrap">
''' + head2('Equipos', 'Las personas', 'detrás de <em>la red.</em>', 'Un equipo multidisciplinar que combina educación, tecnología y acción social.', 'eq-h') + '''      <div class="tiles c4">
        <div class="tile" data-reveal><span class="n">Gobierno</span><h3>Patronato</h3><p>Define la estrategia de la fundación y vela por el cumplimiento de sus fines.</p><a class="more" href="equipo.html#patronato">Conoce al patronato <span>→</span></a></div>
        <div class="tile" data-reveal style="--d:.08s"><span class="n">Gestión</span><h3>Dirección</h3><p>Coordina las sedes, los programas y las alianzas de la entidad.</p></div>
        <div class="tile" data-reveal style="--d:.16s"><span class="n">Territorio</span><h3>Equipos técnicos</h3><p>Educadores, formadores y técnicos que acompañan cada proyecto sobre el terreno.</p><a class="more" href="equipo.html#equipo">Conoce al equipo <span>→</span></a></div>
        <div class="tile" data-reveal style="--d:.24s"><span class="n">Comunidad</span><h3>Voluntariado</h3><p>Personas que multiplican nuestro impacto en cada comunidad.</p><a class="more" href="contacto.html#participa">Hazte voluntario <span>→</span></a></div>
      </div>
    </div>
  </section>

  <section class="pad" id="colaboraciones" aria-labelledby="col-h" style="padding-top:0">
    <div class="wrap split rev">
      <div class="prose">
        <span class="kicker">Colaboraciones</span>
        <h2 class="h2" id="col-h" data-lines><span class="line"><span>Mejor</span></span><span class="line"><span><em>en red.</em></span></span></h2>
        <p data-reveal>Nada de lo que hacemos sería posible sin las entidades, administraciones y empresas que caminan con nosotros.</p>
        <ul class="ticks" data-reveal>
          <li>ALL DIGITAL — red europea de inclusión y competencias digitales</li>
          <li>La Liga Iberoamericana — cooperación con América Latina</li>
          <li>Programas Erasmus+ y fondos europeos</li>
          <li>Entidades del tercer sector y administraciones públicas</li>
          <li>Empresas comprometidas con la inclusión digital</li>
        </ul>
        <div><a class="btn btn-ghost magnetic" href="contacto.html#participa">Colabora con nosotros <span class="arr">→</span></a></div>
      </div>
      <div class="split-media wide" data-clip><img src="img/conecta.jpg" alt="Figuras de personas conectadas por hilos de colores" loading="lazy"></div>
    </div>
  </section>

''' + next_link('mision.html', 'Siguiente', 'Nuestra <em>misión</em>')
write('nosotros.html', 'Nosotros · fundación conecta+', 'Quiénes somos, historia, valores, equipos y colaboraciones de la fundación conecta+.', nosotros)

# ------------------------------------------------------------------ MISIÓN
lines = [
  ('tercer-sector','Tercer sector','Asesoría y gestión del Tercer Sector','news-tercer-sector.jpg','Dos personas revisando código en un portátil',
   'Acompañamos a entidades sociales en su transformación digital y organizativa.',
   'Las entidades sociales hacen un trabajo imprescindible, pero muchas no tienen tiempo ni recursos para modernizarse. Les ofrecemos asesoría cercana y práctica.',
   ['Diagnóstico digital de la entidad','Asesoría en gestión, calidad y protección de datos','SAAD: asesoría digital gratuita para entidades','Formación para equipos y juntas directivas'],
   ['Entidades sociales','Asociaciones','Fundaciones']),
  ('transformacion-digital','Transformación digital','Transformación digital e innovación','tech.jpg','Manos en un teclado con datos luminosos',
   'Ponemos la innovación tecnológica al servicio del impacto social.',
   'Exploramos nuevas herramientas y metodologías para que la tecnología resuelva problemas reales de las personas y las comunidades.',
   ['Proyectos piloto de innovación social','Herramientas digitales seguras (ENS · ISO 27001)','Laboratorios de ideas con comunidades','Transferencia de buenas prácticas europeas'],
   ['Entidades','Administraciones','Comunidades']),
  ('voluntariado','Voluntariado','Voluntariado','news-voluntariado.jpg','Persona voluntaria con camiseta de voluntariado',
   'Personas voluntarias que multiplican nuestro impacto en cada comunidad.',
   'Creemos en la fuerza de la ciudadanía comprometida. Nuestra red de voluntariado acompaña, enseña y aprende en cada proyecto.',
   ['Acogida y formación de personas voluntarias','Acompañamiento digital a personas mayores','Mentorías para jóvenes','Voluntariado corporativo'],
   ['Ciudadanía','Jóvenes','Empresas']),
  ('justicia-educativa','Justicia educativa','Justicia educativa','news-campamentos.jpg','Niñas y niños en un aula durante una actividad',
   'Trabajamos por una educación equitativa dentro y fuera del aula.',
   'La brecha digital es también una brecha educativa. Llevamos recursos, metodologías y acompañamiento a quienes tienen menos oportunidades.',
   ['Refuerzo educativo con tecnología','Campamentos tecnológicos de verano','Educación no formal y TRIC','Trabajo con familias y centros educativos'],
   ['Infancia','Jóvenes','Familias']),
  ('inclusion-digital','Inclusión digital','Inclusión digital','vinculo-manos.avif','Dos manos digitales a punto de tocarse',
   'Acceso, competencias y acompañamiento para que nadie quede atrás en lo digital.',
   'Trámites, salud, empleo, relaciones: casi todo pasa ya por una pantalla. Ayudamos a que cada persona pueda moverse en lo digital con autonomía y seguridad.',
   ['Puntos de acceso y acompañamiento digital','Competencias digitales básicas','Seguridad y ciudadanía digital','Adaptación a la diversidad funcional'],
   ['Mayores','Migrantes','Diversidad funcional','Personas privadas de libertad']),
  ('formacion-tic','Formación TIC','Formación TIC e inserción laboral','news-formacion.jpg','Grupo de personas aprendiendo con portátiles',
   'Capacitación digital orientada a la empleabilidad real.',
   'Diseñamos itinerarios formativos conectados con lo que pide el mercado de trabajo, con acompañamiento personalizado hasta la inserción.',
   ['Itinerarios de competencias digitales','Formación en herramientas profesionales','Orientación laboral y búsqueda de empleo','Formación online en nuestro Campus Virtual'],
   ['Personas desempleadas','Jóvenes','Mujeres']),
  ('liderazgo-juvenil','Liderazgo juvenil','Participación y liderazgo juvenil','news-internacional.jpg','Grupo de jóvenes abrazados mirando al mar',
   'Espacios donde jóvenes desarrollan voz propia y capacidad de incidencia social.',
   'Las personas jóvenes no son solo destinatarias: son protagonistas. Creamos espacios para que participen, lideren y transformen su entorno.',
   ['Grupos de participación juvenil','Intercambios y movilidad europea','Proyectos de incidencia social','Formación en liderazgo y ciudadanía'],
   ['Jóvenes','Adolescentes','Género']),
]
idx = ''.join(f'<a href="#{i}"><span>0{n+1}</span><b>{short}</b></a>' for n,(i,short,*_) in enumerate(lines))
mision = page_hero('Misión', 'Que nadie', 'quede <em>fuera.</em>',
    'Siete líneas de trabajo que combinan tecnología, formación y acompañamiento para reducir la brecha digital y social.',
    'contenido.jpg', [(l[0], l[1]) for l in lines[:4]] + [('lineas','Ver todas')], media=MISION_MEDIA, cls=' hero-reel')
mision += f'''
  <section class="pad" id="lineas" aria-labelledby="mis-h" style="padding-bottom:clamp(60px,8vw,110px)">
    <div class="wrap">
      <p class="manifesto-text" id="manifesto">Nuestra misión es que la tecnología sea una <em>vía real</em> de participación, aprendizaje y derechos para todas las personas — especialmente para quienes hoy se quedan <em>fuera.</em></p>
      <h2 class="sr-only" id="mis-h">Líneas de trabajo</h2>
    </div>
  </section>
  <nav class="lines-index" aria-label="Líneas de trabajo">{idx}<a href="contacto.html#participa"><span>+</span><b>Participa en un programa →</b></a></nav>
'''
for n,(i,short,title,img,alt,lead,body,ticks,tags) in enumerate(lines):
    more = ('        <div data-reveal><a class="btn btn-tec magnetic" href="transformacion-digital.html">Ver el área de transformación digital <span class="arr">→</span></a></div>\n'
            if i == 'transformacion-digital' else '')
    rev = ' rev' if n % 2 else ''
    tk = ''.join(f'<li>{t}</li>' for t in ticks)
    tg = ''.join(f'<span>{t}</span>' for t in tags)
    mision += f'''
  <section class="mline" id="{i}" aria-labelledby="{i}-h">
    <div class="wrap split{rev}">
      <div class="prose">
        <span class="n">0{n+1} / 07</span>
        <h2 class="h2" id="{i}-h" data-lines><span class="line"><span>{title}</span></span></h2>
        <p class="big" data-reveal>{lead}</p>
        <p data-reveal>{body}</p>
        <ul class="ticks" data-reveal>{tk}</ul>
        <div class="tags" data-reveal>{tg}</div>
{more}      </div>
      <div class="split-media" data-clip><img src="img/{img}" alt="{alt}" loading="lazy"></div>
    </div>
  </section>
'''
mision += '\n' + next_link('proyectos.html', 'Siguiente', 'Ver <em>proyectos</em>')
write('mision.html', 'Misión · fundación conecta+', 'Las siete líneas de trabajo de la fundación conecta+: tercer sector, transformación digital, voluntariado, justicia educativa, inclusión digital, formación TIC y liderazgo juvenil.', mision)

# ------------------------------------------------------------------ PROYECTOS
def pcard(img, alt, tag, title, text, cat, d=''):
    style = f' style="--d:{d}"' if d else ''
    return f'''        <article class="card" data-cat="{cat}" data-reveal{style}><div class="card-img"><img src="img/{img}" alt="{alt}" loading="lazy"><span class="card-tag">{tag}</span></div><h3>{title}</h3><p>{text}</p></article>
'''
proyectos = page_hero('Proyectos', 'Proyectos que', 'dejan <em>huella.</em>',
    'Iniciativas en España y en el resto del mundo para que la tecnología abra puertas en lugar de cerrarlas.',
    'tech.jpg', [('nacionales','Nacionales'),('internacionales','Internacionales')], 'center 30%', media=PROY_MEDIA, cls=' hero-city')
proyectos += '''
  <section class="pad" id="nacionales" aria-labelledby="nac-h">
    <div class="wrap">
''' + head2('Proyectos nacionales', 'En nuestras', '<em>cuatro sedes.</em>', 'Andalucía, Madrid, Cataluña y Galicia: proyectos cercanos, diseñados con cada comunidad.', 'nac-h') + '''      <div class="filters" data-filter-group="#pgridNac" role="group" aria-label="Filtrar proyectos">
        <button type="button" data-filter="all" aria-pressed="true">Todos</button>
        <button type="button" data-filter="tercer" aria-pressed="false">Tercer sector</button>
        <button type="button" data-filter="formacion" aria-pressed="false">Formación</button>
        <button type="button" data-filter="infancia" aria-pressed="false">Infancia y juventud</button>
        <button type="button" data-filter="comunidad" aria-pressed="false">Comunidad</button>
      </div>
      <div class="pgrid" id="pgridNac">
''' + pcard('news-tercer-sector.jpg','Dos personas revisando código en un portátil','Tercer sector','SAAD: asesoría digital gratuita para entidades sociales','Acompañamiento para que las entidades sociales den el salto digital sin coste.','tercer') \
    + pcard('news-formacion.jpg','Grupo de personas aprendiendo con portátiles','Formación','Curso de TRIC aplicadas a la educación no formal','Formación en Madrid para educadores que quieren incorporar la tecnología a su trabajo.','formacion','.08s') \
    + pcard('news-campamentos.jpg','Niñas y niños en un aula durante una actividad','Infancia y juventud','Campamentos tecnológicos de verano','Programación, robótica y creatividad en Madrid y Galicia durante el verano.','infancia','.16s') \
    + pcard('news-voluntariado.jpg','Persona voluntaria con camiseta de voluntariado','Comunidad','Red de personas voluntarias','Una nueva red que acompaña a las personas que más lo necesitan en su día a día digital.','comunidad') \
    + pcard('news-ens.jpg','Placa de circuito iluminada','Calidad','Certificación en el Esquema Nacional de Seguridad','Garantizamos la seguridad de la información de las personas y entidades con las que trabajamos.','tercer','.08s') \
    + pcard('tech.jpg','Manos en un teclado con datos luminosos','Formación','Itinerarios de competencias digitales','Formación orientada a la inserción laboral, presencial y en nuestro Campus Virtual.','formacion','.16s') + '''      </div>
    </div>
  </section>

  <section class="people" aria-hidden="true" style="padding-block:0 clamp(40px,6vw,80px)">
    <div class="ticker" data-speed="-0.35"></div>
  </section>

  <section class="pad" id="internacionales" aria-labelledby="int-h" style="background:var(--bg-2)">
    <div class="wrap">
''' + head2('Proyectos internacionales', 'Una red que', '<em>cruza fronteras.</em>', 'Desde nuestras cuatro sedes en España tejemos alianzas con Europa e Iberoamérica. Pasa el cursor por cada proyecto para verlo en el mapa.', 'int-h') + '''      <div class="flatmap" id="flatmap" data-reveal>
        <canvas class="flatmap-canvas" role="img" aria-label="Mapa de proyectos internacionales: España conectada con Europa e Iberoamérica"></canvas>
      </div>
      <div class="pin-cards">
        <article class="pin-card" data-pin="eu" data-lat="50.85" data-lon="4.35" data-label="ALL DIGITAL" data-reveal style="--d:0.00s" tabindex="0">
          <span class="pin-card-top"><span class="pin-dot" aria-hidden="true"></span>01 — Europa</span>
          <h3>ALL DIGITAL</h3>
          <p>Red europea que impulsa la inclusión y las competencias digitales para todas las personas.</p>
        </article>
        <article class="pin-card" data-pin="eu2" data-lat="48.2" data-lon="16.4" data-label="Inclusión digital en Europa" data-reveal style="--d:0.07s" tabindex="0">
          <span class="pin-card-top"><span class="pin-dot" aria-hidden="true"></span>02 — Erasmus+</span>
          <h3>Inclusión digital en Europa</h3>
          <p>Nuevo proyecto Erasmus+ para compartir metodologías de inclusión digital con entidades europeas.</p>
        </article>
        <article class="pin-card" data-pin="latam" data-lat="4.7" data-lon="-74.1" data-label="La Liga Iberoamericana" data-reveal style="--d:0.14s" tabindex="0">
          <span class="pin-card-top"><span class="pin-dot" aria-hidden="true"></span>03 — Iberoamérica</span>
          <h3>La Liga Iberoamericana</h3>
          <p>Cooperación con entidades de América Latina en educación y acción social.</p>
        </article>
        <article class="pin-card" data-pin="youth" data-lat="45.4" data-lon="9.2" data-label="Movilidad juvenil" data-reveal style="--d:0.21s" tabindex="0">
          <span class="pin-card-top"><span class="pin-dot" aria-hidden="true"></span>04 — Juventud</span>
          <h3>Movilidad juvenil</h3>
          <p>Intercambios que permiten a jóvenes vivir experiencias de participación en otros países.</p>
        </article>
      </div>
    </div>
  </section>

''' + next_link('recursos.html', 'Siguiente', 'Explorar <em>recursos</em>')
write('proyectos.html', 'Proyectos · fundación conecta+', 'Proyectos nacionales e internacionales de la fundación conecta+.', proyectos)

# ------------------------------------------------------------------ RECURSOS
def ritem(tp, title, meta, cat, href='#'):
    return f'        <a class="ritem" href="{href}" data-cat="{cat}"><span class="type">{tp}</span><h3>{title}</h3><span class="meta">{meta}</span><span class="go" aria-hidden="true">→</span></a>\n'
recursos = page_hero('Recursos', 'Aprende,', 'descarga, <em>consulta.</em>',
    'Noticias, publicaciones y documentos de transparencia de la fundación, reunidos en un solo lugar.',
    'news-formacion.jpg', [('blog','Blog'),('publicaciones','Publicaciones'),('transparencia','Transparencia'),('campus','Campus Virtual')])
recursos += '''
  <section class="pad" id="blog" aria-labelledby="blog-h">
    <div class="wrap">
''' + head2('Blog y noticias', 'Lo último', 'de <em>la red.</em>', None, 'blog-h') + '''      <div class="filters" data-filter-group="#rlistBlog" role="group" aria-label="Filtrar noticias">
        <button type="button" data-filter="all" aria-pressed="true">Todo</button>
        <button type="button" data-filter="calidad" aria-pressed="false">Calidad</button>
        <button type="button" data-filter="formacion" aria-pressed="false">Formación</button>
        <button type="button" data-filter="comunidad" aria-pressed="false">Comunidad</button>
        <button type="button" data-filter="internacional" aria-pressed="false">Internacional</button>
      </div>
      <div class="rlist" id="rlistBlog">
''' + ritem('Calidad','Nos certificamos en el Esquema Nacional de Seguridad (ENS)','Noticia','calidad') \
    + ritem('Tercer sector','SAAD: asesoría digital gratuita para las entidades sociales','Noticia','comunidad') \
    + ritem('Formación','Curso de TRIC aplicadas a la educación no formal en Madrid','Noticia','formacion') \
    + ritem('Infancia','Campamentos tecnológicos de verano en Madrid y Galicia','Noticia','formacion') \
    + ritem('Voluntariado','La nueva red de personas voluntarias arranca su acompañamiento','Noticia','comunidad') \
    + ritem('Internacional','Nuevo proyecto Erasmus+ para la inclusión digital en Europa','Noticia','internacional') + '''      </div>
    </div>
  </section>

  <section class="pad values-sec" id="publicaciones" aria-labelledby="pub-h">
    <div class="wrap">
''' + head2('Publicaciones', 'Para leer', 'y <em>compartir.</em>', 'Memorias, guías y materiales que elaboramos a partir de nuestro trabajo.', 'pub-h') + '''      <div class="values">
        <a class="value" href="#" data-reveal style="--d:0.00s">
          <img src="img/pub-memoria.jpg" alt="" loading="lazy">
          <div class="value-top"><span class="n">PDF</span><svg class="sym" aria-hidden="true"><use href="#sym"/></svg></div>
          <div class="value-body"><h3>Memoria anual de actividades</h3><p>Lo que hicimos durante el año, con quién y con qué resultados.</p><span class="more">Descargar <b aria-hidden="true">→</b></span></div>
        </a>
        <a class="value" href="#" data-reveal style="--d:0.08s">
          <img src="img/pub-guia.jpg" alt="" loading="lazy">
          <div class="value-top"><span class="n">Guía</span><svg class="sym" aria-hidden="true"><use href="#sym"/></svg></div>
          <div class="value-body"><h3>Guía de competencias digitales</h3><p>Material de apoyo para formadores y personas voluntarias.</p><span class="more">Descargar <b aria-hidden="true">→</b></span></div>
        </a>
        <a class="value" href="#" data-reveal style="--d:0.16s">
          <img src="img/pub-tercer-sector.jpg" alt="" loading="lazy">
          <div class="value-top"><span class="n">Guía</span><svg class="sym" aria-hidden="true"><use href="#sym"/></svg></div>
          <div class="value-body"><h3>Digitalización del tercer sector</h3><p>Claves prácticas para que las entidades sociales den el salto digital.</p><span class="more">Descargar <b aria-hidden="true">→</b></span></div>
        </a>
      </div>
    </div>
  </section>

  <section class="pad" id="transparencia" aria-labelledby="tr-h">
    <div class="wrap">
''' + head2('Transparencia', 'Cuentas', '<em>claras.</em>', 'Rendir cuentas es parte de nuestro compromiso con las personas, las entidades y las instituciones que confían en nosotros.', 'tr-h') + '''      <div class="rlist">
''' + ritem('Documento','Estatutos de la fundación','PDF','') \
    + ritem('Documento','Composición del patronato','PDF','') \
    + ritem('Economía','Cuentas anuales e informe de auditoría','PDF','') \
    + ritem('Calidad','Política de calidad y medio ambiente (ISO 9001 · ISO 14001)','PDF','') \
    + ritem('Seguridad','Política de seguridad de la información (ENS · ISO 27001)','PDF','') \
    + ritem('Ética','Canal ético','Formulario','') + '''      </div>
    </div>
  </section>

  <section class="cta pad" id="campus" aria-labelledby="campus-h">
    <canvas class="cta-net" aria-hidden="true"></canvas>
    <div class="wrap">
      <span class="kicker">Campus Virtual</span>
      <h2 id="campus-h" data-lines><span class="line"><span>Aprende a tu</span></span><span class="line"><span><em>ritmo.</em></span></span></h2>
      <div class="cta-grid">
        <p data-reveal>Cursos online de competencias digitales y formación para la inserción laboral, con acompañamiento de nuestro equipo.</p>
        <div data-reveal style="--d:.1s"><a class="btn btn-mag magnetic" href="#">Entrar al Campus Virtual <span class="arr">→</span></a></div>
      </div>
    </div>
  </section>

''' + next_link('contacto.html', 'Siguiente', 'Ir a <em>contacto</em>')
write('recursos.html', 'Recursos · fundación conecta+', 'Blog, publicaciones, transparencia y Campus Virtual de la fundación conecta+.', recursos)

# ------------------------------------------------------------------ CONTACTO
contacto = page_hero('Contacto', 'Hablemos,', '<em>conectemos.</em>',
    '¿Quieres participar, colaborar o necesitas información? Escríbenos y te responderemos lo antes posible.',
    'news-tercer-sector.jpg', [('escribenos','Escríbenos'),('participa','Participa'),('sedes','Sedes'),('faq','Preguntas')])
contacto += '''
  <section class="pad net-sec" id="escribenos" aria-labelledby="form-h">
    <canvas class="cta-net" data-theme="dark" data-form="contactForm" aria-hidden="true"></canvas>
    <div class="wrap contact-grid">
      <div class="prose">
        <span class="kicker">Escríbenos</span>
        <h2 class="h2" id="form-h" data-lines><span class="line"><span>Cuéntanos</span></span><span class="line"><span><em>qué necesitas.</em></span></span></h2>
        <p data-reveal>También puedes llamarnos o escribirnos directamente:</p>
        <div data-reveal>
          <a class="big-link" href="mailto:info@conectamas.org">info@conectamas.org</a>
          <a class="big-link" href="tel:+34934745546">934 745 546</a>
        </div>
      </div>
      <div class="contact-form" data-reveal>
        <form id="contactForm" novalidate data-msg="¡Gracias! Hemos recibido tu mensaje y te responderemos pronto.">
          <div class="fields">
            <div class="field"><label for="cName">Nombre</label><input id="cName" name="nombre" required autocomplete="name"></div>
            <div class="field"><label for="cMail">Correo electrónico</label><input id="cMail" name="email" type="email" required autocomplete="email"></div>
            <div class="field full"><label for="cTopic">Motivo</label>
              <select id="cTopic" name="motivo">
                <option>Información general</option>
                <option>Quiero hacer voluntariado</option>
                <option>Colaborar como entidad o empresa</option>
                <option>Participar en una formación</option>
                <option>Prensa y comunicación</option>
              </select>
            </div>
            <div class="field full"><label for="cMsg">Mensaje</label><textarea id="cMsg" name="mensaje" required></textarea></div>
            <label class="check full"><input type="checkbox" required> He leído y acepto la política de privacidad.</label>
          </div>
          <button type="submit" class="btn btn-tec magnetic">Enviar mensaje <span class="arr">→</span></button>
        </form>
        <p class="form-note" aria-live="polite"></p>
      </div>
    </div>
  </section>

  <section class="pad values-sec" id="participa" aria-labelledby="part-h">
    <div class="wrap">
''' + head2('Únete a la red', 'Formas de', '<em>participar.</em>', 'Hay muchas maneras de sumarse a conecta+. Elige la tuya.', 'part-h') + '''      <div class="values four">
        <a class="value" href="#escribenos" data-reveal style="--d:0.00s">
          <img src="img/news-voluntariado.jpg" alt="" loading="lazy">
          <div class="value-top"><span class="n">01</span><svg class="sym" aria-hidden="true"><use href="#sym"/></svg></div>
          <div class="value-body"><h3>Hazte voluntario</h3><p>Dedica tu tiempo y tu talento a acompañar a otras personas.</p><span class="more">Quiero participar <b aria-hidden="true">→</b></span></div>
        </a>
        <a class="value" href="#escribenos" data-reveal style="--d:0.08s">
          <img src="img/news-tercer-sector.jpg" alt="" loading="lazy">
          <div class="value-top"><span class="n">02</span><svg class="sym" aria-hidden="true"><use href="#sym"/></svg></div>
          <div class="value-body"><h3>Colabora como entidad</h3><p>Trabajemos juntos en proyectos de inclusión y educación.</p><span class="more">Hablemos <b aria-hidden="true">→</b></span></div>
        </a>
        <a class="value" href="#escribenos" data-reveal style="--d:0.16s">
          <img src="img/news-formacion.jpg" alt="" loading="lazy">
          <div class="value-top"><span class="n">03</span><svg class="sym" aria-hidden="true"><use href="#sym"/></svg></div>
          <div class="value-body"><h3>Empresas</h3><p>Voluntariado corporativo y alianzas con impacto social.</p><span class="more">Saber más <b aria-hidden="true">→</b></span></div>
        </a>
        <a class="value" href="index.html#unete" data-reveal style="--d:0.24s">
          <img src="img/conecta.jpg" alt="" loading="lazy">
          <div class="value-top"><span class="n">04</span><svg class="sym" aria-hidden="true"><use href="#sym"/></svg></div>
          <div class="value-body"><h3>Newsletter</h3><p>Recibe cada mes novedades, convocatorias y formas de participar.</p><span class="more">Suscribirme <b aria-hidden="true">→</b></span></div>
        </a>
      </div>
    </div>
  </section>

  <section class="pad" id="sedes" aria-labelledby="sedes-h">
    <div class="wrap split">
      <div class="prose">
        <span class="kicker">Sedes</span>
        <h2 class="h2" id="sedes-h" data-lines><span class="line"><span>Cerca de</span></span><span class="line"><span><em>ti.</em></span></span></h2>
        <p data-reveal>Estamos presentes en cuatro comunidades autónomas. Escríbenos y te pondremos en contacto con la sede más cercana.</p>
      </div>
      <div class="sedes" data-reveal>
        <div class="sede"><b>Cataluña</b><span>C/ Riu Anoia, 42-54<br>08820 El Prat de Llobregat<br><a href="tel:+34934745546">934 745 546</a></span></div>
        <div class="sede"><b>Madrid</b><span>Sede territorial<br><a href="mailto:info@conectamas.org">info@conectamas.org</a></span></div>
        <div class="sede"><b>Andalucía</b><span>Sede territorial<br><a href="mailto:info@conectamas.org">info@conectamas.org</a></span></div>
        <div class="sede"><b>Galicia</b><span>Sede territorial<br><a href="mailto:info@conectamas.org">info@conectamas.org</a></span></div>
      </div>
    </div>
  </section>

  <section class="pad" id="faq" aria-labelledby="faq-h" style="padding-top:0">
    <div class="wrap">
''' + head2('Preguntas frecuentes', 'Resolvemos', 'tus <em>dudas.</em>', None, 'faq-h') + '''      <div class="faq" data-reveal>
        <details><summary>¿Cómo puedo hacerme voluntario?</summary><p>Rellena el formulario de contacto eligiendo «Quiero hacer voluntariado». Te escribiremos para conocerte y contarte los proyectos disponibles cerca de ti.</p></details>
        <details><summary>¿Las formaciones tienen coste?</summary><p>Muchas de nuestras formaciones son gratuitas para las personas participantes gracias a la financiación pública y privada. Consulta cada convocatoria.</p></details>
        <details><summary>Soy una entidad social, ¿cómo podéis ayudarnos?</summary><p>A través de nuestra línea de asesoría y gestión del tercer sector, incluido el servicio SAAD de asesoría digital gratuita. Escríbenos y valoramos juntos vuestras necesidades.</p></details>
        <details><summary>¿Dónde estáis?</summary><p>Tenemos sedes en Andalucía, Madrid, Cataluña y Galicia, y participamos en proyectos europeos e iberoamericanos.</p></details>
      </div>
    </div>
  </section>

''' + next_link('index.html', 'Volver', 'Al <em>inicio</em>')
write('contacto.html', 'Contacto · fundación conecta+', 'Contacta con la fundación conecta+: formulario, formas de participar, sedes y preguntas frecuentes.', contacto)


# ------------------------------------------------------------------ EQUIPO (subpágina de Nosotros)
# DATOS DE EJEMPLO: nombres, fotos y textos son ficticios (fotos de relleno de i.pravatar.cc).
# Sustituir por los reales antes de publicar la web definitiva.
# Formato: (nombre, cargo, foto en img/equipo/, texto breve[, sede para el filtro])
# Si la foto se deja vacía ('') se muestra el símbolo de la marca.
patronato = [
    ('Ramón Castellví Roig', 'Presidencia', 'persona-09.jpg', 'Impulsor de la fundación desde sus inicios. Vela por que conecta+ no pierda nunca su vocación comunitaria.'),
    ('Elena Ruiz Ortega', 'Vicepresidencia', 'persona-05.jpg', 'Pedagoga con largo recorrido en educación no formal y en proyectos de inclusión.'),
    ('Marta Sánchez Lloret', 'Secretaría', 'persona-11.jpg', 'Jurista especializada en entidades sin ánimo de lucro y en buen gobierno.'),
    ('Jordi Puig Ferrer', 'Tesorería', 'persona-18.jpg', 'Economista. Cuida de que cada euro llegue a donde más impacto tiene.'),
    ('Laura Vidal Ramos', 'Vocal', 'persona-13.jpg', 'Experta en políticas de juventud y participación ciudadana.'),
    ('Andrés Molina Paz', 'Vocal', 'persona-06.jpg', 'Ingeniero de telecomunicaciones comprometido con la inclusión digital.'),
]
equipo = [
    ('Clara Domènech Vila', 'Dirección general', 'persona-12.jpg', 'Coordina las cuatro sedes y la estrategia de la fundación.', 'direccion'),
    ('Pablo Herrera Luna', 'Coordinación de proyectos', 'persona-04.jpg', 'Diseña y acompaña los programas desde la idea hasta la evaluación.', 'direccion'),
    ('Núria Soler Pons', 'Coordinación · Cataluña', 'persona-01.jpg', 'Responsable de la sede de El Prat de Llobregat y de sus programas.', 'cataluna'),
    ('David Okafor Martín', 'Coordinación · Madrid', 'persona-15.jpg', 'Conecta la sede de Madrid con entidades, centros y administraciones.', 'madrid'),
    ('Lucía Moreno Cano', 'Coordinación · Andalucía', 'persona-07.jpg', 'Trabaja mano a mano con las comunidades andaluzas.', 'andalucia'),
    ('Xoán Castro Vilas', 'Coordinación · Galicia', 'persona-16.jpg', 'Lidera la sede gallega y los campamentos tecnológicos de verano.', 'galicia'),
    ('Álex Romero Sanz', 'Formación TIC', 'persona-02.jpg', 'Formador en competencias digitales e itinerarios de empleo.', 'cataluna'),
    ('Irene Navarro Gil', 'Proyectos europeos', 'persona-10.jpg', 'Gestiona los proyectos Erasmus+ y la relación con ALL DIGITAL.', 'madrid'),
    ('Sergio Gil Prieto', 'Voluntariado', 'persona-03.jpg', 'Acoge, forma y acompaña a la red de personas voluntarias.', 'andalucia'),
    ('Aitana Campos Rey', 'Comunicación', 'persona-14.jpg', 'Cuenta lo que hacemos y da voz a las personas que participan.', 'direccion'),
    ('Sara Iglesias Otero', 'Justicia educativa', 'persona-08.jpg', 'Educadora social centrada en infancia y familias.', 'galicia'),
    ('Hugo Benítez Ríos', 'Tercer sector', 'persona-17.jpg', 'Asesora a entidades sociales en su transformación digital (SAAD).', 'madrid'),
]

def person(name, role, photo, bio, cat=None, d=0):
    ph = (f'<img src="img/equipo/{photo}" alt="{name}, {role}" loading="lazy">' if photo
          else '<svg aria-hidden="true"><use href="#sym"/></svg>')
    empty = '' if photo else ' empty'
    catattr = f' data-cat="{cat}"' if cat else ''
    style = f' style="--d:{d*.06:.2f}s"' if d else ''
    return f'''        <article class="person"{catattr} data-reveal{style}>
          <div class="ph{empty}">{ph}</div>
          <span class="role">{role}</span>
          <h3>{name}</h3>
          <p>{bio}</p>
        </article>
'''

eq = page_hero('<a href="nosotros.html">Nosotros</a><span aria-hidden="true">/</span><span>Equipo</span>',
    'Las personas', 'detrás de <em>la red.</em>',
    'Un patronato comprometido y un equipo multidisciplinar que combina educación, tecnología y acción social en cuatro territorios.',
    'news-voluntariado.jpg', [('patronato', 'Patronato'), ('equipo', 'Equipo'), ('trabaja', 'Trabaja con nosotros')], 'center 30%')
eq += '''
  <section class="pad" id="patronato" aria-labelledby="pat-h">
    <div class="wrap">
''' + head2('Patronato', 'Quienes marcan', 'el <em>rumbo.</em>', 'El patronato define la estrategia de la fundación y vela por el cumplimiento de sus fines.', 'pat-h') + '''      <div class="people-grid">
''' + ''.join(person(n, r, f, b, d=i % 3) for i, (n, r, f, b) in enumerate(patronato)) + '''      </div>
    </div>
  </section>

  <section class="pad" id="equipo" aria-labelledby="team-h" style="background:var(--bg-2)">
    <div class="wrap">
''' + head2('Equipo', 'Cerca de cada', '<em>comunidad.</em>', 'Educadores, formadores y técnicos que acompañan cada proyecto sobre el terreno.', 'team-h') + '''      <div class="filters" data-filter-group="#teamGrid" role="group" aria-label="Filtrar equipo por sede">
        <button type="button" data-filter="all" aria-pressed="true">Todo el equipo</button>
        <button type="button" data-filter="direccion" aria-pressed="false">Dirección</button>
        <button type="button" data-filter="cataluna" aria-pressed="false">Cataluña</button>
        <button type="button" data-filter="madrid" aria-pressed="false">Madrid</button>
        <button type="button" data-filter="andalucia" aria-pressed="false">Andalucía</button>
        <button type="button" data-filter="galicia" aria-pressed="false">Galicia</button>
      </div>
      <div class="people-grid four" id="teamGrid">
''' + ''.join(person(n, r, f, b, c, i % 4) for i, (n, r, f, b, c) in enumerate(equipo)) + '''      </div>
    </div>
  </section>

  <section class="cta pad" id="trabaja" aria-labelledby="work-h">
    <canvas class="cta-net" aria-hidden="true"></canvas>
    <div class="wrap">
      <span class="kicker">Trabaja con nosotros</span>
      <h2 id="work-h" data-lines><span class="line"><span>¿Te sumas</span></span><span class="line"><span>al <em>equipo?</em></span></span></h2>
      <div class="cta-grid">
        <p data-reveal>Buscamos personas con ganas de transformar su entorno: profesionales, voluntariado y estudiantes en prácticas.</p>
        <div data-reveal style="--d:.1s;display:flex;gap:10px;flex-wrap:wrap"><a class="btn btn-mag magnetic" href="contacto.html#escribenos">Envíanos tu candidatura <span class="arr">→</span></a></div>
      </div>
    </div>
  </section>

''' + next_link('mision.html', 'Siguiente', 'Nuestra <em>misión</em>')
write('equipo.html', 'Equipo y patronato · fundación conecta+', 'El patronato y el equipo de la fundación conecta+.', eq, parent='nosotros.html')


# ------------------------------------------------------------------ TRANSFORMACIÓN DIGITAL (subpágina de Misión)
TX_HEAD = '<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">'

tx_services = [
    ('asesoria_digital', 'Asesoría digital y tecnológica',
     'Acompañamos a las entidades en su desarrollo digital y en la implantación de servicios y tecnologías: para optimizar su gestión y para acercar tecnología social a las personas beneficiarias y usuarias de su acción.',
     ['gestión', 'tecnología social', 'servicios digitales'],
     '<path d="M8 36h48M8 20h48M20 8v48M44 8v48" /><circle cx="44" cy="20" r="5" />'),
    ('formacion_tech', 'Formación y capacitación tecnológica',
     'Formamos a profesionales y personas voluntarias del sector social en competencias digitales, cultura organizativa y definición de procesos, y en el manejo de herramientas, el despliegue de servicios digitales y la implantación de tecnología.',
     ['presencial', 'online', 'mixta', 'DigComp 2.0'],
     '<rect x="8" y="12" width="48" height="32" rx="4" /><path d="M24 52h16M32 44v8M20 26l6 5-6 5M30 36h12" />'),
    ('consultoria_digital', 'Consultoría digital',
     'Auditoría y consultoría para el control de las medidas de seguridad de la información y la implantación de nuevas herramientas digitales en la entidad.',
     ['seguridad', 'auditoría', 'herramientas'],
     '<path d="M32 6l22 8v16c0 14-10 24-22 28C20 54 10 44 10 30V14z" /><path d="M23 31l6 6 12-13" />'),
]
tx_cards = ''
for n, (slug, title, text, tags, icon) in enumerate(tx_services):
    tg = ''.join(f'<span>{t}</span>' for t in tags)
    tx_cards += f'''        <article class="tx-card" data-reveal style="--d:{n*.08:.2f}s">
          <div class="tx-card-top"><span>0{n+1} // {slug}</span><i aria-hidden="true"></i></div>
          <svg class="tx-icon" viewBox="0 0 64 64" aria-hidden="true">{icon}</svg>
          <h3>{title}</h3>
          <p>{text}</p>
          <div class="tx-tags">{tg}</div>
        </article>
'''

digcomp = [
    ('Información y alfabetización de datos', 'Buscar, evaluar y gestionar información y datos.'),
    ('Comunicación y colaboración', 'Interactuar, compartir y participar en entornos digitales.'),
    ('Creación de contenidos digitales', 'Crear, editar y reutilizar contenidos con criterio.'),
    ('Seguridad', 'Proteger dispositivos, datos personales, salud y entorno.'),
    ('Resolución de problemas', 'Identificar necesidades y resolverlas con tecnología.'),
]
dc_rows = ''.join(f'''        <li data-reveal style="--d:{i*.06:.2f}s"><span class="tx-mono">0{i+1}</span><b>{t}</b><span>{d}</span><i aria-hidden="true" style="--w:{[92,84,76,88,80][i]}%"></i></li>
''' for i, (t, d) in enumerate(digcomp))

develop = [
    'Consultoría para la transformación digital de entidades',
    'Acompañamiento en la implantación de soluciones tecnológicas',
    'Licencias de servicios digitales a mejor precio para el sector',
    'Kit Digital',
    'Software a medida para el sector social',
    'Desarrollo web',
    'Formación en competencias digitales básicas, intermedias y avanzadas',
    'Desarrollo de contenidos digitales',
    'Mentoría de software',
]
dev_items = ''.join(f'        <li data-reveal style="--d:{(i%5)*.05:.2f}s"><span class="tx-mono">{i+1:02d}</span>{t}</li>\n' for i, t in enumerate(develop))
dev_items += '        <li class="tx-dev-cta" data-reveal style="--d:.2s"><a href="contacto.html#escribenos"><span class="tx-mono">+</span>¿Tienes otra idea? Hablemos <b aria-hidden="true">→</b></a></li>\n'

tx = f'''  <section class="page-hero tx-hero" aria-labelledby="page-h">
    <canvas class="tx-net" id="txNet" aria-hidden="true"></canvas>
    <div class="wrap">
      <nav class="crumbs fade-up" aria-label="Ruta"><a href="index.html">Inicio</a><span aria-hidden="true">/</span><a href="mision.html">Misión</a><span aria-hidden="true">/</span><span>Transformación digital</span></nav>
      <p class="tx-status fade-up"><i aria-hidden="true"></i>conecta+ // equipo de tecnología · online</p>
      <h1 id="page-h"><span class="line"><span>Transformación</span></span><span class="line"><span><em>digital.</em></span></span></h1>
      <p class="tx-prompt fade-up" aria-label="Desde el tercer sector, para el tercer sector"><span aria-hidden="true">&gt;</span> <span class="tx-typed" data-type="desde el tercer sector, para el tercer sector" aria-hidden="true"></span><b aria-hidden="true">_</b></p>
      <div class="page-hero-foot fade-up">
        <p>Somos el equipo de tecnología de conecta+: técnicos, desarrolladores y profesionales del tercer sector que ayudan a las entidades sociales a modernizarse e innovar.</p>
        <div class="anchors"><a href="#servicios">Servicios</a><a href="#digitalizaong">DigitalizaciONG</a><a href="#desarrollamos">Qué desarrollamos</a><a href="#por-que">Por qué nosotros</a></div>
      </div>
    </div>
  </section>

  <section class="pad tx-grid-bg" id="servicios" aria-labelledby="srv-h">
    <div class="wrap">
''' + head2('Servicios', 'Tres formas de', '<em>ayudaros.</em>', 'Asesoría, formación y consultoría pensadas para las necesidades reales de las entidades del sector social.', 'srv-h') + f'''      <div class="tx-cards">
{tx_cards}      </div>
    </div>
  </section>

  <section class="pad" id="digcomp" aria-labelledby="dc-h" style="padding-top:0">
    <div class="wrap tx-dc">
      <div class="prose">
        <span class="kicker">Marco europeo</span>
        <h2 class="h2" id="dc-h" data-lines><span class="line"><span>Formación con</span></span><span class="line"><span><em>DigComp 2.0.</em></span></span></h2>
        <p data-reveal>Nuestras formaciones se apoyan en el Marco Europeo de Competencias Digitales DigComp 2.0 y sus cinco áreas.</p>
      </div>
      <ol class="tx-dc-list">
{dc_rows}      </ol>
    </div>
  </section>

  <section class="pad tx-grid-bg" id="digitalizaong" aria-labelledby="dong-h" style="background-color:var(--bg-2)">
    <div class="wrap split">
      <div class="prose">
        <span class="kicker">Iniciativa propia</span>
        <h2 class="h2" id="dong-h" data-lines><span class="line"><span>Digitaliza<em>ONG</em></span></span></h2>
        <p class="big" data-reveal>Un proceso profundo de consultoría digital para tu entidad.</p>
        <p data-reveal>Evaluamos y diagnosticamos la madurez digital de la entidad y la acompañamos en la confección de su Plan de Transformación Digital.</p>
        <ol class="tx-steps" data-reveal>
          <li><span class="tx-mono">01</span>Evaluación</li>
          <li><span class="tx-mono">02</span>Diagnóstico de madurez digital</li>
          <li><span class="tx-mono">03</span>Plan de Transformación Digital</li>
          <li><span class="tx-mono">04</span>Acompañamiento en la implantación</li>
        </ol>
      </div>
      <div class="tx-term" data-reveal aria-label="Ejemplo ilustrativo de un diagnóstico de DigitalizaciONG">
        <div class="tx-term-bar"><i></i><i></i><i></i><span>digitalizaong — diagnóstico</span></div>
        <pre class="tx-term-body" id="txTerm" aria-hidden="true"
data-lines='["$ digitalizaong --diagnostico --entidad tu-entidad","› analizando procesos de gestión ........... ok","› revisando seguridad de la información .... ok","› evaluando competencias digitales ........ ok","› inventario de herramientas y licencias .. ok","› calculando madurez digital","  [████████████████░░░░░░░░] 64%","✓ plan de transformación digital listo","$ _"]'></pre>
        <p class="tx-term-note">Ejemplo ilustrativo</p>
      </div>
    </div>
  </section>

  <section class="pad" id="desarrollamos" aria-labelledby="dev-h">
    <div class="wrap">
      <div class="tx-words" aria-hidden="true"><span>Inmersivo.</span><span>Interactivo.</span><span><em>Innovador.</em></span></div>
''' + head2('Qué desarrollamos', 'Del diagnóstico', 'al <em>código.</em>', None, 'dev-h') + f'''      <ul class="tx-dev">
{dev_items}      </ul>
    </div>
  </section>

  <section class="pad tx-grid-bg" id="por-que" aria-labelledby="why-h" style="background-color:var(--bg-2)">
    <div class="wrap">
      <span class="kicker">Por qué nosotros</span>
      <h2 class="tx-quote" id="why-h" data-lines><span class="line"><span>Desde el tercer sector,</span></span><span class="line"><span><em>para el tercer sector.</em></span></span></h2>
      <div class="tiles c3" style="margin-top:clamp(48px,6vw,88px)">
        <div class="tile" data-reveal><span class="n">// experiencia</span><h3>Experiencia</h3><p>Más de 20 años trabajando en derechos digitales, brecha digital y fortalecimiento asociativo.</p></div>
        <div class="tile" data-reveal style="--d:.08s"><span class="n">// transversalidad</span><h3>Transversalidad</h3><p>Un equipo interdisciplinar de técnicos y profesionales del tercer sector y del sector tecnológico.</p></div>
        <div class="tile" data-reveal style="--d:.16s"><span class="n">// ajuste</span><h3>Ajuste a la necesidad</h3><p>Cada proyecto parte de lo que la entidad necesita de verdad, no de la tecnología de moda.</p></div>
      </div>
    </div>
  </section>

  <section class="pad tx-cta" id="empieza" aria-labelledby="go-h">
    <div class="wrap">
      <span class="kicker">¡Empieza ya!</span>
      <h2 id="go-h" data-lines><span class="line"><span>Modernizar el sector,</span></span><span class="line"><span><em>innovar</em> para mejorar.</span></span></h2>
      <div class="cta-grid">
        <p data-reveal>Cuéntanos en qué punto está tu entidad y diseñamos juntos el siguiente paso.</p>
        <div data-reveal style="--d:.1s;display:flex;gap:10px;flex-wrap:wrap">
          <a class="btn btn-tec magnetic" href="contacto.html#escribenos">Hablemos de tu entidad <span class="arr">→</span></a>
          <a class="btn btn-ghost magnetic" href="mailto:info@conectamas.org">info@conectamas.org</a>
        </div>
      </div>
    </div>
  </section>

''' + next_link('mision.html', 'Volver', 'Toda la <em>misión</em>')
write('transformacion-digital.html', 'Transformación digital · fundación conecta+',
      'Asesoría, formación y consultoría digital para entidades del tercer sector: DigitalizaciONG, DigComp 2.0, software a medida y desarrollo web.',
      tx, parent='mision.html', extra_head=TX_HEAD)

# ------------------------------------------------------------------ PORTADA: menú y pie compartidos
p = os.path.join(ROOT, 'index.html')
s = io.open(p, encoding='utf-8').read()
a = s.index('<!-- ============ NAV ============ -->'); b = s.index('<main id="top">')
s = s[:a] + NAV + '\n' + s[b:]
a = s.index('<!-- ============ FOOTER ============ -->'); b = s.index('<script src="https://unpkg.com/lenis')
s = s[:a] + FOOTER + '\n' + s[b:]
if 'id="curtain"' not in s:
    s = s.replace('<div class="cursor-dot" aria-hidden="true"></div>\n', '<div class="cursor-dot" aria-hidden="true"></div>\n<div class="curtain" id="curtain" aria-hidden="true"><svg><use href="#sym"/></svg></div>\n', 1)
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('patched index.html')
