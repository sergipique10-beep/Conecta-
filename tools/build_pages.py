"""Generador de las páginas de fundación conecta+.

Escribe TODAS las páginas de la web salvo la portada, a partir de las plantillas
y listas de datos de este archivo, y sustituye el menú (NAV) y el pie (FOOTER)
de index.html, que comparten todas.

Uso, desde la raíz del repositorio:
    python tools/build_pages.py

Importante: las páginas se SOBRESCRIBEN. Si cambias su contenido, cámbialo
aquí y vuelve a ejecutar el script; no edites esos .html a mano.
index.html es la excepción: se edita a mano salvo su NAV y su FOOTER.

Estructura (según el wireframe de navegación):
    Nosotros      → quienes-somos, equipo, historia, ecosistema (→ eco-*)
    Qué hacemos   → formacion-tic, observatorio, voluntariado, jovenes,
                    inclusion-digital, transformacion-digital
    Proyectos     → proyectos-nacionales / proyectos-internacionales (→ proyecto-*)
    Recursos      → blog (→ noticia-*), publicaciones (→ publicacion-*),
                    transparencia, preguntas-frecuentes, campus
    Contacto      → escribenos, sedes
    Colabora      → hazte-voluntario, dona, unete
    Pie           → boletin, canal-denuncia, aviso-legal
"""
# Genera las páginas de conecta+ con cabecera y pie compartidos.
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
<!-- paleta guardada antes de pintar (selector «Modo») -->
<script>(function(d){{var ok={{bosque:1,verde:1,noche:1,papel:1,lima:1,magenta:1}},p=null;try{{var q=new URLSearchParams(location.search).get('paleta');if(ok[q]){{p=q;localStorage.setItem('conecta-paleta',q)}}else{{p=localStorage.getItem('conecta-paleta')}}}}catch(e){{}}d.setAttribute('data-paleta',ok[p]?p:'bosque');d.classList.add('js')}})(document.documentElement)</script>
<link rel="stylesheet" href="css/site.css">
</head>
<body>
'''

CHROME = '''
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="sym" viewBox="0 0 64 64">
    <circle cx="21" cy="15" r="8" fill="var(--sym-1)"/>
    <rect x="8" y="26" width="26" height="30" rx="13" fill="var(--sym-1)"/>
    <g transform="rotate(180 32 32)">
      <circle cx="21" cy="15" r="8" fill="var(--sym-2)"/>
      <rect x="8" y="26" width="26" height="30" rx="13" fill="var(--sym-2)"/>
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
          <li><a href="quienes-somos.html">Quiénes somos</a></li>
          <li><a href="equipo.html">Equipo y patronato</a></li>
          <li><a href="historia.html">Historia</a></li>
          <li><a href="ecosistema.html">Nuestro ecosistema</a></li>
        </ul></div></div>
      </li>
      <li class="has-drop">
        <a href="que-hacemos.html" aria-haspopup="true">Qué hacemos</a>
        <div class="drop"><div class="drop-panel"><ul>
          <li><a href="formacion-tic.html">Formación TIC e inserción laboral</a></li>
          <li><a href="observatorio.html">Observatorio de Brechas Digitales</a></li>
          <li><a href="voluntariado.html">Voluntariado</a></li>
          <li><a href="jovenes.html">Jóvenes</a></li>
          <li><a href="inclusion-digital.html">e-Inclusión digital</a></li>
          <li><a href="transformacion-digital.html">Transformación digital y Tercer Sector</a></li>
        </ul></div></div>
      </li>
      <li class="has-drop">
        <a href="proyectos.html" aria-haspopup="true">Proyectos</a>
        <div class="drop"><div class="drop-panel"><ul>
          <li><a href="proyectos-nacionales.html">Proyectos nacionales</a></li>
          <li><a href="proyectos-internacionales.html">Proyectos internacionales</a></li>
        </ul></div></div>
      </li>
      <li class="has-drop">
        <a href="recursos.html" aria-haspopup="true">Recursos</a>
        <div class="drop"><div class="drop-panel"><ul>
          <li><a href="blog.html">Blog y noticias</a></li>
          <li><a href="publicaciones.html">Publicaciones y descargables</a></li>
          <li><a href="transparencia.html">Transparencia</a></li>
          <li><a href="preguntas-frecuentes.html">Preguntas frecuentes</a></li>
          <li><a href="campus.html">Campus Virtual</a></li>
        </ul></div></div>
      </li>
      <li class="has-drop">
        <a href="contacto.html" aria-haspopup="true">Contacto</a>
        <div class="drop"><div class="drop-panel"><ul>
          <li><a href="escribenos.html">Escríbenos</a></li>
          <li><a href="sedes.html">Sedes</a></li>
        </ul></div></div>
      </li>
    </ul>
    <button class="search-btn" id="searchBtn" type="button" aria-label="Abrir el buscador" aria-controls="search" aria-expanded="false"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5l5 5"/></svg></button>
    <div class="modo" id="modo">
      <button class="modo-btn" id="modoBtn" type="button" aria-haspopup="menu" aria-expanded="false" aria-controls="modoMenu" aria-label="Modo de color: cambiar paleta"><span class="modo-sw" aria-hidden="true"><i></i><i></i><i></i></span><span class="modo-lbl">Modo</span><span class="modo-chev" aria-hidden="true"></span></button>
      <div class="modo-menu" id="modoMenu" role="menu" aria-label="Paleta de colores"></div>
    </div>
    <a class="btn btn-tec nav-cta magnetic" href="colabora.html">Colabora <span class="arr">→</span></a>
    <button class="burger" id="burger" aria-expanded="false" aria-controls="mmenu" aria-label="Abrir menú"><div><span></span><span></span></div></button>
  </div>
</header>

<div class="mmenu" id="mmenu">
  <a class="big" href="nosotros.html">Nosotros</a>
  <div class="subs"><a href="quienes-somos.html">Quiénes somos</a><a href="equipo.html">Equipo y patronato</a><a href="historia.html">Historia</a><a href="ecosistema.html">Nuestro ecosistema</a></div>
  <a class="big" href="que-hacemos.html"><em>Qué hacemos</em></a>
  <div class="subs"><a href="formacion-tic.html">Formación TIC</a><a href="observatorio.html">Observatorio</a><a href="voluntariado.html">Voluntariado</a><a href="jovenes.html">Jóvenes</a><a href="inclusion-digital.html">e-Inclusión digital</a><a href="transformacion-digital.html">Transformación digital</a></div>
  <a class="big" href="proyectos.html">Proyectos</a>
  <div class="subs"><a href="proyectos-nacionales.html">Nacionales</a><a href="proyectos-internacionales.html">Internacionales</a></div>
  <a class="big" href="recursos.html">Recursos</a>
  <div class="subs"><a href="blog.html">Blog</a><a href="publicaciones.html">Publicaciones</a><a href="transparencia.html">Transparencia</a><a href="preguntas-frecuentes.html">Preguntas frecuentes</a><a href="campus.html">Campus Virtual</a></div>
  <a class="big" href="contacto.html">Contacto</a>
  <div class="subs"><a href="escribenos.html">Escríbenos</a><a href="sedes.html">Sedes</a></div>
  <a class="btn btn-tec" href="colabora.html">Colabora <span class="arr">→</span></a>
</div>

<!-- buscador: de momento solo la interfaz (sin resultados) -->
<div class="search" id="search" role="dialog" aria-modal="true" aria-labelledby="searchTitle" hidden>
  <div class="search-panel">
    <div class="search-head">
      <p class="search-title" id="searchTitle">Buscar en conecta+</p>
      <button type="button" class="search-close" data-search-close aria-label="Cerrar el buscador">×</button>
    </div>
    <form class="search-form" id="searchForm" role="search">
      <label for="searchInput" class="sr-only">¿Qué estás buscando?</label>
      <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5l5 5"/></svg>
      <input id="searchInput" type="search" placeholder="¿Qué estás buscando?" autocomplete="off">
    </form>
    <p class="search-note" id="searchNote" aria-live="polite">El buscador estará disponible muy pronto. Mientras tanto, prueba con estos accesos:</p>
    <div class="search-links"><a href="que-hacemos.html">Qué hacemos</a><a href="proyectos.html">Proyectos</a><a href="blog.html">Blog y noticias</a><a href="publicaciones.html">Publicaciones</a><a href="campus.html">Campus Virtual</a><a href="colabora.html">Colabora</a><a href="escribenos.html">Contacto</a></div>
  </div>
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
      <a class="fc-big" href="escribenos.html">¿<em>Conectamos</em>?</a>
      <div class="fc-actions">
        <a class="btn btn-tec magnetic" href="escribenos.html">Escríbenos <span class="arr">→</span></a>
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
      <div class="fc-col" role="navigation" aria-label="La fundación">
        <h4>La fundación</h4>
        <ul>
          <li><a class="roll" href="boletin.html"><span class="rl"><span>Boletín único</span></span></a></li>
          <li><a class="roll" href="transparencia.html"><span class="rl"><span>Transparencia</span></span></a></li>
          <li><a class="roll" href="canal-denuncia.html"><span class="rl"><span>Canal de denuncia</span></span></a></li>
          <li><a class="roll" href="aviso-legal.html"><span class="rl"><span>Aviso legal y privacidad</span></span></a></li>
        </ul>
      </div>
      <div class="fc-col" role="navigation" aria-label="Accesos">
        <h4>Accesos</h4>
        <ul>
          <li><a class="roll" href="campus.html"><span class="rl"><span>Campus Virtual</span></span></a></li>
          <li><a class="roll" href="sedes.html"><span class="rl"><span>Sedes</span></span></a></li>
          <li><a class="roll" href="que-hacemos.html"><span class="rl"><span>Qué hacemos</span></span></a></li>
          <li><a class="roll" href="colabora.html"><span class="rl"><span>Colabora</span></span></a></li>
        </ul>
      </div>
      <div class="fc-news">
        <h4>Boletín</h4>
        <form class="foot-form" novalidate data-msg="¡Gracias! Te hemos enviado un correo para confirmar la suscripción.">
          <label for="footMail" class="sr-only">Correo electrónico para el boletín</label>
          <div class="foot-form-row">
            <input id="footMail" type="email" placeholder="tu@email.com" required autocomplete="email">
            <button type="submit" aria-label="Suscribirme">→</button>
          </div>
          <p class="foot-privacy">Un correo al mes, sin spam. Al suscribirte aceptas la <a href="aviso-legal.html#privacidad">política de privacidad</a>.</p>
        </form>
        <p class="form-note" aria-live="polite"></p>
        <div class="foot-trust">
          <a href="transparencia.html">ENS</a><a href="transparencia.html">ISO 9001</a><a href="transparencia.html">ISO 14001</a><a href="transparencia.html">ISO 27001</a><a href="proyectos-internacionales.html">ALL DIGITAL</a><a href="proyectos-internacionales.html">Erasmus+</a>
        </div>
      </div>

      <div class="fc-legal">
        <span>© <span data-year>2026</span> Fundación Conecta+</span>
        <nav aria-label="Legal"><a href="aviso-legal.html">Aviso legal</a><a href="aviso-legal.html#privacidad">Privacidad</a><a href="aviso-legal.html#cookies">Cookies</a><button type="button" class="link-btn" data-cookie-open>Configurar cookies</button><a href="aviso-legal.html#accesibilidad">Accesibilidad</a><a href="canal-denuncia.html">Canal de denuncia</a></nav>
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
  <a href="escribenos.html"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>Escribir</a>
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

# ================================================================== HELPERS

def crumbs(*items):
    """Migas tras «Inicio»: crumbs(('Nosotros', 'nosotros.html'), ('Historia', None))."""
    sep = '<span aria-hidden="true">/</span>'
    return sep.join(f'<a href="{h}">{t}</a>' if h else f'<span>{t}</span>' for t, h in items)

def page_hero(crumb, l1, l2, lede, img, anchors=(), pos='center', media=None, cls='', back=None):
    a = ''.join('<a href="#%s">%s</a>' % (h, t) for h, t in anchors)
    anchors_html = f'\n        <div class="anchors">{a}</div>' if a else ''
    media_html = media or f'    <div class="hero-media"><img src="img/{img}" alt="" fetchpriority="high" style="object-position:{pos}"></div>\n'
    back_html = f'      <a class="back-pill fade-up" href="{back[0]}"><span aria-hidden="true">←</span>Volver a {back[1]}</a>\n' if back else ''
    line2 = f'<span class="line"><span>{l2}</span></span>' if l2 else ''
    return f'''  <section class="page-hero{cls}" aria-labelledby="page-h">
{media_html}    <div class="wrap">
{back_html}      <nav class="crumbs fade-up" aria-label="Ruta"><a href="index.html">Inicio</a><span aria-hidden="true">/</span>{crumb if '<' in crumb else '<span>' + crumb + '</span>'}</nav>
      <h1 id="page-h"><span class="line"><span>{l1}</span></span>{line2}</h1>
      <div class="page-hero-foot fade-up">
        <p>{lede}</p>{anchors_html}
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

def ph_note(text):
    """Aviso visible de contenido provisional (pendiente de la fundación)."""
    return f'<p class="ph-note" data-reveal>{text}</p>'

def hub_cards(items, cls=''):
    """Tarjetas con foto que enlazan a subpáginas: (href, img, n, título, texto, acción)."""
    out = f'      <div class="values{cls}">\n'
    for i, (href, img, n, title, text, more) in enumerate(items):
        out += f'''        <a class="value" href="{href}" data-reveal style="--d:{(i % 3) * .08:.2f}s">
          <img src="img/{img}" alt="" loading="lazy">
          <div class="value-top"><span class="n">{n}</span><svg class="sym" aria-hidden="true"><use href="#sym"/></svg></div>
          <div class="value-body"><h3>{title}</h3><p>{text}</p><span class="more">{more} <b aria-hidden="true">→</b></span></div>
        </a>
'''
    return out + '      </div>\n'

def hub_section(kicker, l1, l2, p, hid, items, cls='', sid=None):
    idattr = f' id="{sid}"' if sid else ''
    return f'''
  <section class="pad values-sec"{idattr} aria-labelledby="{hid}">
    <div class="wrap">
''' + head2(kicker, l1, l2, p, hid) + hub_cards(items, cls) + '''    </div>
  </section>
'''

def siblings(group, items, current):
    """«Sigue explorando»: enlaces a las páginas hermanas, sin la actual. items: (href, título, texto)."""
    rest = [it for it in items if it[0] != current]
    c = ' c3' if len(rest) % 3 == 0 or len(rest) > 4 else (' c4' if len(rest) == 4 else '')
    tiles = ''.join(f'        <a class="tile" href="{h}" data-reveal style="--d:{(i % 4) * .08:.2f}s"><span class="n">{group}</span><h3>{t}</h3><p>{x}</p><span class="more">Ir a la página <span>→</span></span></a>\n'
                    for i, (h, t, x) in enumerate(rest))
    return f'''
  <section class="pad sib-sec" aria-labelledby="sib-h">
    <div class="wrap">
''' + head2('Sigue explorando', 'También en', f'<em>{group}.</em>', None, 'sib-h') + f'''      <div class="tiles{c}">
{tiles}      </div>
    </div>
  </section>
'''

def pager(label, prev, nxt):
    """Anterior / siguiente entre páginas de detalle. prev y nxt: (href, título) o None."""
    def one(item, cls, word):
        if not item:
            return f'    <span class="pager-empty {cls}" aria-hidden="true"></span>\n'
        return f'    <a class="{cls}" href="{item[0]}"><small>{word}</small><strong>{item[1]}</strong></a>\n'
    return f'''
  <nav class="pager" aria-label="{label}">
{one(prev, 'pager-prev', '← Anterior')}{one(nxt, 'pager-next', 'Siguiente →')}  </nav>
'''

def portal_link(domain, url):
    if url == '#':
        return f'<span class="portal-link is-pending">{domain}</span>'
    return f'<a class="portal-link" href="{url}" target="_blank" rel="noopener">{domain} <b aria-hidden="true">↗</b></a>'

def portal_cta(hid, l1, l2, text, name, url):
    """Bloque crema con llamada al portal externo (lo que el wireframe llama «inyección de CTA»)."""
    btn = (f'<a class="btn btn-mag magnetic" href="{url}" target="_blank" rel="noopener">Visitar {name} <span class="arr">↗</span></a>'
           if url != '#' else '<span class="btn btn-mag is-disabled" aria-disabled="true">Enlace pendiente</span>')
    return f'''
  <section class="cta pad" aria-labelledby="{hid}">
    <canvas class="cta-net" aria-hidden="true"></canvas>
    <div class="wrap">
      <span class="kicker">Portal</span>
      <h2 id="{hid}" data-lines><span class="line"><span>{l1}</span></span><span class="line"><span>{l2}</span></span></h2>
      <div class="cta-grid">
        <p data-reveal>{text}</p>
        <div data-reveal style="--d:.1s;display:flex;gap:10px;flex-wrap:wrap">{btn}</div>
      </div>
    </div>
  </section>
'''

def neighbours(lst, i, key):
    prev = key(lst[i - 1]) if i > 0 else None
    nxt = key(lst[i + 1]) if i < len(lst) - 1 else None
    return prev, nxt

def write(name, title, desc, body, parent=None, extra_head=''):
    head = HEAD.format(title=title, desc=desc)
    if extra_head:
        head = head.replace('</head>', extra_head + '\n</head>')
    if parent:  # marca la sección padre como activa en el menú
        head = head.replace('<body>', f'<body data-parent="{parent}">')
    html = head + CHROME + '\n' + NAV + '\n<main id="top">\n' + body + '</main>\n\n' + FOOTER + TAIL
    io.open(os.path.join(ROOT, name), 'w', encoding='utf-8', newline='\n').write(html)
    print('wrote', name)

def redirect(name, to):
    """Antiguas URL: página mínima que lleva a la nueva (para no romper enlaces ya publicados)."""
    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>fundación conecta+</title>
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={to}">
<link rel="canonical" href="{to}">
</head>
<body><p>Esta página se ha movido. <a href="{to}">Ir a la nueva página</a>.</p></body>
</html>
'''
    io.open(os.path.join(ROOT, name), 'w', encoding='utf-8', newline='\n').write(html)
    print('wrote', name, '->', to)

# ================================================================== DATOS COMPARTIDOS

# Áreas de «Qué hacemos». cat = categoría de los proyectos de esa área (filtro de Proyectos nacionales).
AREAS = [
    dict(href='formacion-tic.html', cat='formacion', name='Formación TIC e inserción laboral', short='Formación TIC',
         img='news-formacion.jpg', alt='Grupo de personas aprendiendo con portátiles',
         h1=('Formación TIC', 'e <em>inserción laboral.</em>'),
         card='Capacitación digital orientada a la empleabilidad real.',
         lede='La formación tecnológica como vía de inclusión social, ciudadana y laboral, sobre todo para los colectivos más vulnerables.',
         lead='Itinerarios formativos conectados con lo que pide el mercado de trabajo.',
         body='Combinamos formación técnica, orientación laboral individualizada y prospección con empresas tecnológicas, y acompañamos a cada persona hasta la inserción. También formamos a profesionales de la educación y del sector social.',
         ticks=['Bootcamps de programación y datos para jóvenes en desempleo', 'Formación online para profesionales de la educación y entidades', 'Servicios formativos para entidades y Administración pública', 'Certificaciones digitales reconocidas'],
         tags=['Jóvenes', 'Personas desempleadas', 'Profesionales'],
         portal=('Conecta IA', 'conecta-ia.fundacionesplai.org', 'https://conecta-ia.fundacionesplai.org/',
                 'Cursos online de competencias digitales e inteligencia artificial para profesionales, entidades y dinamizadores sociodigitales.')),
    dict(href='observatorio.html', cat='observatorio', name='Observatorio de Brechas Digitales', short='Observatorio (OBD)',
         img='contenido.jpg', alt='Pantallas con datos y gráficos',
         h1=('Observatorio de', '<em>brechas digitales.</em>'),
         card='Datos para entender —y reducir— las desigualdades digitales.',
         lede='Investigamos las desigualdades en el acceso y el uso de la tecnología para que entidades y administraciones decidan con datos.',
         lead='Medir la brecha digital es el primer paso para cerrarla.',
         body='El Observatorio analiza la infraestructura, las habilidades digitales y las barreras socioeconómicas y culturales que dejan a personas fuera del mundo digital, y comparte sus resultados en informes abiertos.',
         ticks=['Informes periódicos sobre brechas digitales', 'Barómetro y centro de documentación', 'Revista semestral sobre inclusión social', 'Formación y divulgación'],
         tags=['Investigación', 'Administraciones', 'Entidades'],
         portal=('el Observatorio', 'observatoriobrechasdigitales.org', 'https://observatoriobrechasdigitales.org/',
                 'Informes, barómetro, revista y centro de documentación del Observatorio de Brechas Digitales.')),
    dict(href='voluntariado.html', cat='voluntariado', name='Voluntariado', short='Voluntariado',
         img='news-voluntariado.jpg', alt='Persona voluntaria con camiseta de voluntariado',
         h1=('Equipo de', '<em>voluntariado.</em>'),
         card='Personas voluntarias que multiplican nuestro impacto.',
         lede='Promovemos la participación ciudadana, el trabajo en red y las alianzas para el cambio social.',
         lead='Creemos en la fuerza de la ciudadanía comprometida.',
         body='Acogemos, formamos y acompañamos a las personas que quieren aportar su tiempo, sus conocimientos y su compromiso en proyectos educativos, sociales y de inclusión digital, y conectamos voluntariado y entidades.',
         ticks=['Proyectos de voluntariado educativo, social y de inclusión digital', 'Acogida y formación de personas voluntarias', 'Encuentro anual de juventud comprometida', 'Reconocimiento a la labor voluntaria'],
         tags=['Ciudadanía', 'Jóvenes', 'Entidades'],
         portal=('voluntariado.net', 'voluntariado.net', 'https://voluntariado.net/',
                 'El portal del voluntariado: información, asesoramiento y un espacio de encuentro entre organizaciones y personas voluntarias.')),
    dict(href='jovenes.html', cat='jovenes', name='Jóvenes', short='Jóvenes',
         img='news-internacional.jpg', alt='Grupo de jóvenes abrazados mirando al mar',
         h1=('Participación y', '<em>liderazgo juvenil.</em>'),
         card='Espacios donde la juventud tiene voz propia.',
         lede='Espacios de encuentro, acción, debate y liderazgo para que la juventud transforme su entorno.',
         lead='Las personas jóvenes no son solo destinatarias: son protagonistas.',
         body='Combinamos la participación en el tiempo libre con el Aprendizaje y Servicio para que los jóvenes actúen colectivamente al servicio de su comunidad, con un uso saludable y responsable de la tecnología.',
         ticks=['Propuestas educativas sobre participación y ciudadanía global', 'Aprendizaje y Servicio y acción comunitaria', 'Foro anual liderado por jóvenes', 'Recursos sobre hábitos digitales saludables'],
         tags=['Jóvenes', 'Adolescentes', 'Profesionales de juventud'],
         portal=None),
    dict(href='inclusion-digital.html', cat='inclusion', name='e-Inclusión digital', short='e-Inclusión digital',
         img='vinculo-manos.avif', alt='Dos manos digitales a punto de tocarse',
         h1=('e-Inclusión', '<em>digital.</em>'),
         card='Que nadie quede atrás en lo digital.',
         lede='Competencias digitales para que cada persona pueda participar activamente en la sociedad.',
         lead='Acceso, competencias y acompañamiento para moverse en lo digital con autonomía.',
         body='Tomamos como referencia el marco europeo DigComp y trabajamos sobre todo con personas en riesgo de exclusión, en especial mujeres y jóvenes, con la metodología de Aprendizaje y Servicio: aprender y poner lo aprendido al servicio de la comunidad.',
         ticks=['Jóvenes que enseñan tecnología a personas mayores', 'Vocaciones STEAM para chicas jóvenes', 'Capacitación digital para mujeres en situación de vulnerabilidad', 'Formación en igualdad y competencias transversales'],
         tags=['Mayores', 'Mujeres', 'Jóvenes', 'Migrantes'],
         portal=None),
    dict(href='transformacion-digital.html', cat='tercer', name='Transformación digital y Gestión del Tercer Sector', short='Transformación digital y Tercer Sector',
         img='tech.jpg', alt='Manos en un teclado con datos luminosos',
         card='Asesoría, formación y consultoría digital para entidades sociales.'),
]
AREA_BY_CAT = {a['cat']: a for a in AREAS}
SIB_AREAS = [(a['href'], a['short'], a['card']) for a in AREAS]

SIB_NOS = [
    ('quienes-somos.html', 'Quiénes somos', 'Qué somos, qué nos mueve y con quién caminamos.'),
    ('equipo.html', 'Equipo y patronato', 'Las personas que hacen posible la fundación.'),
    ('historia.html', 'Historia', 'Tres décadas conectando personas y tecnología.'),
    ('ecosistema.html', 'Nuestro ecosistema', 'Los portales y redes que impulsamos.'),
]
SIB_REC = [
    ('blog.html', 'Blog y noticias', 'Lo último de la red.'),
    ('publicaciones.html', 'Publicaciones', 'Memorias, guías y materiales descargables.'),
    ('transparencia.html', 'Transparencia', 'Documentos de la fundación, a la vista.'),
    ('preguntas-frecuentes.html', 'Preguntas frecuentes', 'Respuestas a las dudas más habituales.'),
    ('campus.html', 'Campus Virtual', 'Formación online a tu ritmo.'),
]
SIB_CON = [
    ('escribenos.html', 'Escríbenos', 'Cuéntanos qué necesitas.'),
    ('sedes.html', 'Sedes', 'Dónde estamos.'),
]
SIB_COL = [
    ('hazte-voluntario.html', 'Hazte voluntario/a', 'Dedica tu tiempo a acompañar a otras personas.'),
    ('dona.html', 'Dona', 'Tu aportación sostiene nuestros proyectos.'),
    ('unete.html', 'Únete a la red', 'Suma tu entidad a la red contra la brecha digital.'),
]

# Proyectos nacionales. cat: categorías del filtro (las de AREAS), separadas por espacios.
PROJ_NAC = [
    dict(slug='saad', img='news-tercer-sector.jpg', alt='Dos personas revisando código en un portátil', tag='Tercer sector', cat='tercer',
         title='SAAD: asesoría digital gratuita para entidades sociales', text='Acompañamiento para que las entidades sociales den el salto digital sin coste.',
         body='Un servicio de asesoría cercana y práctica para entidades que no tienen tiempo ni recursos para modernizarse: diagnóstico, recomendaciones y acompañamiento en las primeras decisiones.'),
    dict(slug='ens', img='news-ens.jpg', alt='Placa de circuito iluminada', tag='Calidad', cat='tercer',
         title='Certificación en el Esquema Nacional de Seguridad', text='Garantizamos la seguridad de la información de las personas y entidades con las que trabajamos.',
         body='La certificación ENS se suma a nuestras normas ISO 9001, ISO 14001 e ISO 27001 y refuerza cómo cuidamos los datos de las personas y entidades que confían en nosotros.'),
    dict(slug='itinerarios', img='tech.jpg', alt='Manos en un teclado con datos luminosos', tag='Formación', cat='formacion',
         title='Itinerarios de competencias digitales', text='Formación orientada a la inserción laboral, presencial y en nuestro Campus Virtual.',
         body='Itinerarios por niveles que combinan formación técnica, orientación laboral y prácticas, con acompañamiento personalizado hasta la inserción.'),
    dict(slug='tric', img='news-formacion.jpg', alt='Grupo de personas aprendiendo con portátiles', tag='Formación', cat='formacion',
         title='Curso de TRIC aplicadas a la educación no formal', text='Formación en Madrid para educadores que quieren incorporar la tecnología a su trabajo.',
         body='Un curso para que educadoras y educadores del tiempo libre incorporen las tecnologías de la relación, la información y la comunicación (TRIC) a sus proyectos.'),
    dict(slug='informe-brechas', img='contenido.jpg', alt='Pantallas con datos y gráficos', tag='Observatorio', cat='observatorio',
         title='Informe sobre brechas digitales', text='Datos actualizados sobre las desigualdades digitales en España.',
         body='El informe analiza el acceso, el uso y las habilidades digitales de la población, y las barreras socioeconómicas y culturales que todavía dejan a personas fuera.'),
    dict(slug='red-voluntariado', img='news-voluntariado.jpg', alt='Persona voluntaria con camiseta de voluntariado', tag='Voluntariado', cat='voluntariado',
         title='Red de personas voluntarias', text='Una nueva red que acompaña a las personas que más lo necesitan en su día a día digital.',
         body='Personas voluntarias formadas por la fundación que acompañan a quienes tienen dificultades con trámites, comunicaciones y servicios digitales.'),
    dict(slug='campamentos', img='news-campamentos.jpg', alt='Niñas y niños en un aula durante una actividad', tag='Jóvenes', cat='jovenes',
         title='Campamentos tecnológicos de verano', text='Programación, robótica y creatividad en Madrid y Galicia durante el verano.',
         body='Semanas de verano en las que niñas, niños y adolescentes aprenden programación, robótica y creación digital en grupo y jugando.'),
    dict(slug='conecta-joven', img='conexion-personas.jpg', alt='Personas conectadas', tag='e-Inclusión', cat='inclusion jovenes',
         title='Conecta Joven', text='Jóvenes que enseñan tecnología a personas mayores para reducir la brecha digital generacional.',
         body='Un proyecto de Aprendizaje y Servicio: los jóvenes se forman como dinamizadores y, a la vez, enseñan a personas mayores de su barrio a usar la tecnología.'),
    dict(slug='chicas-in-tech', img='hero-personas.jpg', alt='Grupo de personas', tag='e-Inclusión', cat='inclusion jovenes',
         title='#ChicasInTech', text='Talleres, mentorías y divulgación para orientar a mujeres jóvenes hacia vocaciones STEAM.',
         body='Talleres prácticos, mentorías con profesionales y acciones de divulgación para que más chicas se imaginen en carreras científicas y tecnológicas.'),
]
for p in PROJ_NAC:
    p['href'] = f"proyecto-{p['slug']}.html"

# Proyectos internacionales (los datos de mapa se usan en el mapa de proyectos).
PROJ_INT = [
    dict(slug='all-digital', pin='eu', lat='50.85', lon='4.35', zone='01 — Europa', img='news-internacional.jpg', alt='Grupo de jóvenes abrazados mirando al mar',
         title='ALL DIGITAL', text='Red europea que impulsa la inclusión y las competencias digitales para todas las personas.',
         body='Formamos parte de esta red europea de centros y entidades que trabajan para que toda la ciudadanía tenga las competencias digitales que necesita.'),
    dict(slug='inclusion-europa', pin='eu2', lat='48.2', lon='16.4', zone='02 — Erasmus+', img='conecta.jpg', alt='Figuras de personas conectadas por hilos de colores',
         title='Inclusión digital en Europa', text='Nuevo proyecto Erasmus+ para compartir metodologías de inclusión digital con entidades europeas.',
         body='Un proyecto Erasmus+ para intercambiar metodologías de inclusión digital con entidades de otros países europeos y llevarlas a nuestras sedes.'),
    dict(slug='liga-iberoamericana', pin='latam', lat='4.7', lon='-74.1', zone='03 — Iberoamérica', img='bosque.jpg', alt='Bosque',
         title='La Liga Iberoamericana', text='Cooperación con entidades de América Latina en educación y acción social.',
         body='Cooperamos con organizaciones de la sociedad civil de Iberoamérica que trabajan con infancia, juventud y familias, y en la incidencia en políticas públicas.'),
    dict(slug='movilidad-juvenil', pin='youth', lat='45.4', lon='9.2', zone='04 — Juventud', img='news-campamentos.jpg', alt='Niñas y niños en un aula durante una actividad',
         title='Movilidad juvenil', text='Intercambios que permiten a jóvenes vivir experiencias de participación en otros países.',
         body='Intercambios y encuentros que permiten a jóvenes de nuestras sedes conocer otras realidades y participar en proyectos europeos.'),
]
for p in PROJ_INT:
    p['href'] = f"proyecto-{p['slug']}.html"

# Noticias del blog. cat: filtro del blog.
NEWS = [
    dict(slug='certificacion-ens', img='news-ens.jpg', alt='Placa de circuito iluminada', tag='Calidad', cat='calidad',
         title='Nos certificamos en el Esquema Nacional de Seguridad (ENS)', lead='La certificación ENS refuerza cómo protegemos la información de las personas y entidades con las que trabajamos.'),
    dict(slug='saad', img='news-tercer-sector.jpg', alt='Dos personas revisando código en un portátil', tag='Tercer sector', cat='comunidad',
         title='SAAD: asesoría digital gratuita para las entidades sociales', lead='Abrimos un servicio de asesoría digital gratuita para que las entidades sociales den el salto digital.'),
    dict(slug='curso-tric', img='news-formacion.jpg', alt='Grupo de personas aprendiendo con portátiles', tag='Formación', cat='formacion',
         title='Curso de TRIC aplicadas a la educación no formal en Madrid', lead='Una formación para educadores que quieren incorporar la tecnología a su trabajo en el tiempo libre.'),
    dict(slug='campamentos', img='news-campamentos.jpg', alt='Niñas y niños en un aula durante una actividad', tag='Infancia', cat='formacion',
         title='Campamentos tecnológicos de verano en Madrid y Galicia', lead='Programación, robótica y creatividad para niñas, niños y adolescentes durante el verano.'),
    dict(slug='red-voluntariado', img='news-voluntariado.jpg', alt='Persona voluntaria con camiseta de voluntariado', tag='Voluntariado', cat='comunidad',
         title='La nueva red de personas voluntarias arranca su acompañamiento', lead='Las primeras personas voluntarias de la red ya acompañan a quienes más lo necesitan en su día a día digital.'),
    dict(slug='erasmus-inclusion', img='news-internacional.jpg', alt='Grupo de jóvenes abrazados mirando al mar', tag='Internacional', cat='internacional',
         title='Nuevo proyecto Erasmus+ para la inclusión digital en Europa', lead='Compartiremos metodologías de inclusión digital con entidades de otros países europeos.'),
]
for n in NEWS:
    n['href'] = f"noticia-{n['slug']}.html"

PUBS = [
    dict(slug='memoria-anual', img='pub-memoria.jpg', n='PDF', title='Memoria anual de actividades', text='Lo que hicimos durante el año, con quién y con qué resultados.'),
    dict(slug='guia-competencias', img='pub-guia.jpg', n='Guía', title='Guía de competencias digitales', text='Material de apoyo para formadores y personas voluntarias.'),
    dict(slug='digitalizacion-tercer-sector', img='pub-tercer-sector.jpg', n='Guía', title='Digitalización del tercer sector', text='Claves prácticas para que las entidades sociales den el salto digital.'),
]
for p in PUBS:
    p['href'] = f"publicacion-{p['slug']}.html"

# Portales del ecosistema (URL reales; '#' = pendiente de confirmar).
ECO = [
    dict(slug='gestion-tercer-sector', tipo='formacion', name='Gestión Tercer Sector', domain='gestiontercersector.org', url='https://gestiontercersector.org/', img='news-tercer-sector.jpg',
         short='El sitio del tercer sector para el tercer sector.',
         body='Recursos, asesoría y herramientas para la gestión de las entidades sociales: calidad, protección de datos, gestión económica y buen gobierno.'),
    dict(slug='voluntariado', tipo='intervencion', name='Voluntariado.net', domain='voluntariado.net', url='https://voluntariado.net/', img='news-voluntariado.jpg',
         short='El portal del voluntariado.',
         body='Información, asesoramiento y un espacio de relación entre organizaciones y personas voluntarias.'),
    dict(slug='conecta-ia', tipo='formacion', name='Conecta IA', domain='conecta-ia.fundacionesplai.org', url='https://conecta-ia.fundacionesplai.org/', img='news-formacion.jpg',
         short='Cursos online de competencias digitales e inteligencia artificial.',
         body='Catálogo de formación online para profesionales de la educación, entidades y dinamizadores sociodigitales.'),
    dict(slug='observatorio', tipo='tecnologia', name='Observatorio de Brechas Digitales', domain='observatoriobrechasdigitales.org', url='https://observatoriobrechasdigitales.org/', img='contenido.jpg',
         short='Datos sobre las desigualdades digitales en España.',
         body='Informes, barómetro, revista semestral sobre inclusión social y centro de documentación sobre el acceso y el uso de la tecnología.'),
    dict(slug='red-conecta', tipo='intervencion', name='Red Conecta', domain='redconecta.org', url='https://redconecta.org/', img='conecta.jpg',
         short='Una red de entidades contra la brecha digital.',
         body='Una plataforma de entidades con más de veinte años de experiencia contra la brecha digital: crea espacios de acceso a las TIC, forma a dinamizadores y ofrece formación en competencias digitales.'),
    dict(slug='digitalizaciong', tipo='tecnologia', name='DigitalizaciONG', domain='digitalizaciong.org', url='https://digitalizaciong.org/', img='tech.jpg',
         short='Transformación digital del tercer sector.',
         body='Evaluamos la madurez digital de cada entidad y la acompañamos en la confección y la implantación de su Plan de Transformación Digital.'),
    dict(slug='innovacion', tipo='tecnologia', name='ESInnovación', domain='innovaccion.net', url='https://innovaccion.net/', img='bosque.jpg',
         short='Innovación y transformación digital para la economía social.',
         body='Una iniciativa para impulsar a las entidades de la economía social a través de la innovación y la transformación digital.'),
    dict(slug='liga-iberoamericana', tipo='intervencion', name='La Liga Iberoamericana', domain='ligaiberoamericana.org', url='https://ligaiberoamericana.org/', img='news-internacional.jpg',
         short='Organizaciones de la sociedad civil de Iberoamérica.',
         body='Reúne a organizaciones de la sociedad civil de 18 países de Iberoamérica que trabajan por el desarrollo de la infancia, la juventud y las familias, y por la incidencia en políticas públicas.'),
    dict(slug='foro-derechos-digitales', tipo='intervencion', name='Foro de Derechos Digitales', domain='foroderechosdigitales.org', url='https://foroderechosdigitales.org/', img='conexion-personas.jpg',
         short='Derechos digitales en la era de la inteligencia artificial.',
         body='Un encuentro sobre acceso efectivo a la tecnología, alfabetización digital crítica, inclusión social, discurso de odio, desinformación y retos éticos de la inteligencia artificial.'),
]
for e in ECO:
    e['href'] = f"eco-{e['slug']}.html"

# Tipos de portal para el filtro de «Nuestro ecosistema».
# Es el ÚNICO sitio donde están los nombres visibles: chips, etiquetas de las tarjetas
# y mensajes del filtro salen de aquí. Si se decide usar los pilares de la portada,
# basta con cambiar la columna del nombre (p. ej. Formación → Aprender,
# Tecnología → Transformar, Intervención → Participar); el id puede quedarse igual.
# El tipo de cada portal se asigna con tipo='…' en la lista ECO de arriba.
ECO_TIPOS = [
    ('formacion', 'Formación',
     '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 9.5 12 5l9 4.5-9 4.5z"/><path d="M7 11.6V16c0 1.4 2.2 2.6 5 2.6s5-1.2 5-2.6v-4.4"/><path d="M21 9.5V15"/></svg>'),
    ('tecnologia', 'Tecnología',
     '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="7" y="7" width="10" height="10" rx="2"/><path d="M10 10.5h4v3h-4z"/><path d="M10 3v4M14 3v4M10 17v4M14 17v4M3 10h4M3 14h4M17 10h4M17 14h4"/></svg>'),
    ('intervencion', 'Intervención',
     '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="8" cy="7.5" r="2.6"/><circle cx="16" cy="7.5" r="2.6"/><path d="M3.5 19c0-3 2-5.2 4.5-5.2 1.6 0 3 .9 4 2.3 1-1.4 2.4-2.3 4-2.3 2.5 0 4.5 2.2 4.5 5.2"/></svg>'),
]
ECO_TODOS_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="4" width="6.5" height="6.5" rx="1.6"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="1.6"/><rect x="4" y="13.5" width="6.5" height="6.5" rx="1.6"/><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1.6"/></svg>'
ECO_TIPO_NOMBRE = {t[0]: t[1] for t in ECO_TIPOS}

def pcard(p, d=''):
    style = f' style="--d:{d}"' if d else ''
    return f'''        <a class="card" href="{p['href']}" data-cat="{p['cat']}" data-reveal{style}><div class="card-img"><img src="img/{p['img']}" alt="{p['alt']}" loading="lazy"><span class="card-tag">{p['tag']}</span></div><h3>{p['title']}</h3><p>{p['text']}</p><span class="meta">Ver proyecto</span></a>
'''

def ritem(tp, title, meta, cat, href='#'):
    return f'        <a class="ritem" href="{href}" data-cat="{cat}"><span class="type">{tp}</span><h3>{title}</h3><span class="meta">{meta}</span><span class="go" aria-hidden="true">→</span></a>\n'

def area_projects(cat):
    """Proyectos de un área + enlace a la lista filtrada por esa área."""
    items = [p for p in PROJ_NAC if cat in p['cat'].split()]
    cards = ''.join(pcard(p, f'{(i % 3) * .08:.2f}s') for i, p in enumerate(items))
    return f'''
  <section class="pad" id="proyectos-area" aria-labelledby="pa-h" style="background:var(--bg-2)">
    <div class="wrap">
''' + head2('Proyectos del área', 'Lo que estamos', '<em>haciendo.</em>', None, 'pa-h') + f'''      <div class="pgrid">
{cards}      </div>
      <div style="margin-top:clamp(40px,5vw,64px)" data-reveal><a class="btn btn-ghost magnetic" href="proyectos-nacionales.html?area={cat}">Ver todos los proyectos del área <span class="arr">→</span></a></div>
    </div>
  </section>
'''

# ================================================================== NOSOTROS (hub)
STATS = '''
  <section aria-label="Cifras">
    <div class="stats">
      <div class="stat" data-reveal><b><span data-count="1995">0</span></b><span>año de nacimiento de la fundación</span></div>
      <div class="stat" data-reveal style="--d:.08s"><b><span data-count="4">0</span></b><span>sedes: Andalucía, Madrid, Cataluña y Galicia</span></div>
      <div class="stat" data-reveal style="--d:.16s"><b><span data-count="6">0</span></b><span>áreas de trabajo</span></div>
      <div class="stat" data-reveal style="--d:.24s"><b><span data-count="9">0</span></b><span>portales y redes en nuestro ecosistema</span></div>
    </div>
  </section>
'''
nosotros = page_hero('Nosotros', 'Somos', '<em>conecta+.</em>',
    'Una fundación que lleva desde 1995 tendiendo puentes entre la tecnología y las personas que más lo necesitan.',
    'news-internacional.jpg', [('secciones', 'Conócenos')], 'center 40%')
nosotros += STATS + hub_section('Conócenos', 'Todo sobre', '<em>la fundación.</em>',
    'Quiénes somos, quién forma parte de la fundación, de dónde venimos y la red de portales que impulsamos.', 'nos-h', [
        ('quienes-somos.html', 'vinculo-manos.avif', '01', 'Quiénes somos', 'Tecnología con propósito social: misión, valores y colaboraciones.', 'Conócenos'),
        ('equipo.html', 'news-voluntariado.jpg', '02', 'Equipo y patronato', 'Las personas detrás de la red.', 'Conoce al equipo'),
        ('historia.html', 'bosque.jpg', '03', 'Historia', 'Tres décadas conectando personas y tecnología.', 'Ver la historia'),
        ('ecosistema.html', 'conecta.jpg', '04', 'Nuestro ecosistema', 'Portales y redes que multiplican nuestro impacto.', 'Explorar'),
    ], ' four', sid='secciones') + '\n' + next_link('que-hacemos.html', 'Siguiente', 'Qué <em>hacemos</em>')
write('nosotros.html', 'Nosotros · fundación conecta+', 'Quiénes somos, equipo y patronato, historia y ecosistema de la fundación conecta+.', nosotros)

# ------------------------------------------------------------------ QUIÉNES SOMOS
qs = page_hero(crumbs(('Nosotros', 'nosotros.html'), ('Quiénes somos', None)), 'Tecnología con', '<em>propósito social.</em>',
    'Somos una entidad sin ánimo de lucro dedicada a la educación, la inclusión digital y la acción social.',
    'vinculo-manos.avif', [('quienes-somos', 'Quiénes somos'), ('valores', 'Valores'), ('colaboraciones', 'Colaboraciones')], back=('nosotros.html', 'Nosotros'))
qs += '''
  <section class="pad" id="quienes-somos" aria-labelledby="qs-h">
    <div class="wrap split">
      <div class="prose">
        <span class="kicker">Quiénes somos</span>
        <h2 class="h2" id="qs-h" data-lines><span class="line"><span>Participar, aprender</span></span><span class="line"><span><em>y transformar.</em></span></span></h2>
        <p class="big" data-reveal>Que la tecnología sea una vía real de participación, aprendizaje y derechos — no una barrera más.</p>
        <p data-reveal>Lo hacemos desde la proximidad: escuchando a las comunidades, diseñando con ellas y acompañándolas en el tiempo, desde nuestras sedes en Andalucía, Madrid, Cataluña y Galicia.</p>
      </div>
      <div class="split-media" data-clip><img src="img/vinculo-manos.avif" alt="Dos manos digitales a punto de tocarse" loading="lazy"></div>
    </div>
  </section>
''' + STATS + '''
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

  <section class="pad" id="colaboraciones" aria-labelledby="col-h">
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
        <div><a class="btn btn-ghost magnetic" href="colabora.html">Colabora con nosotros <span class="arr">→</span></a></div>
      </div>
      <div class="split-media wide" data-clip><img src="img/conecta.jpg" alt="Figuras de personas conectadas por hilos de colores" loading="lazy"></div>
    </div>
  </section>
''' + siblings('Nosotros', SIB_NOS, 'quienes-somos.html')
write('quienes-somos.html', 'Quiénes somos · fundación conecta+', 'Qué es la fundación conecta+, sus valores y sus colaboraciones.', qs, parent='nosotros.html')

# ------------------------------------------------------------------ HISTORIA
hist = page_hero(crumbs(('Nosotros', 'nosotros.html'), ('Historia', None)), 'Tres décadas', '<em>conectando.</em>',
    'De una pequeña iniciativa a una red con presencia en cuatro comunidades autónomas y en proyectos europeos e iberoamericanos.',
    'bosque.jpg', back=('nosotros.html', 'Nosotros'))
hist += '''
  <section class="pad" id="historia" aria-labelledby="hist-h">
    <div class="wrap">
''' + head2('Historia', 'De dónde', '<em>venimos.</em>', None, 'hist-h') + '''      <div class="timeline">
        <div class="tl" data-reveal><b>1995</b><h3>Nace conecta+</h3><p>La fundación arranca con una idea sencilla: que el acceso a la tecnología no dependa del lugar donde naces ni de tus recursos.</p></div>
        <div class="tl" data-reveal><b>Red</b><h3>Presencia en cuatro territorios</h3><p>Abrimos sedes en Andalucía, Madrid, Cataluña y Galicia para trabajar cerca de cada comunidad.</p></div>
        <div class="tl" data-reveal><b>Europa</b><h3>Una red que cruza fronteras</h3><p>Nos sumamos a ALL DIGITAL, a La Liga Iberoamericana y a proyectos Erasmus+ para ampliar nuestro impacto.</p></div>
        <div class="tl" data-reveal><b>Calidad</b><h3>Certificados en lo que importa</h3><p>Contamos con las normas ISO 9001, ISO 14001 e ISO 27001 y con el Esquema Nacional de Seguridad (ENS).</p></div>
        <div class="tl" data-reveal><b>Hoy</b><h3>Seis áreas, un propósito</h3><p>Seguimos trabajando para que nadie quede fuera del mundo digital.</p></div>
      </div>
    </div>
  </section>
''' + siblings('Nosotros', SIB_NOS, 'historia.html')
write('historia.html', 'Historia · fundación conecta+', 'La historia de la fundación conecta+ desde 1995.', hist, parent='nosotros.html')

# ------------------------------------------------------------------ NUESTRO ECOSISTEMA
eco_tiles = ''.join(f'''        <a class="tile" href="{e['href']}" data-tipo="{e['tipo']}" data-reveal style="--d:{(i % 3) * .08:.2f}s"><span class="tile-top"><span class="n">{e['domain']}</span><span class="eco-tag" data-tipo="{e['tipo']}">{ECO_TIPO_NOMBRE[e['tipo']]}</span></span><h3>{e['name']}</h3><p>{e['short']}</p><span class="more">Ver portal <span>→</span></span></a>
''' for i, e in enumerate(ECO))
# chips del filtro: los contadores también los recalcula js/site.js a partir de data-tipo
def eco_chip(tid, nombre, icon, n, on=False):
    return (f'        <button type="button" class="eco-chip" data-tipo-filtro="{tid}" aria-pressed="{"true" if on else "false"}">'
            f'{icon}<span class="eco-lbl">{nombre}</span><span class="eco-n">{n}</span></button>\n')
eco_chips = eco_chip('todos', 'Todos', ECO_TODOS_ICON, len(ECO), True) + ''.join(
    eco_chip(t, nombre, icon, sum(1 for e in ECO if e['tipo'] == t)) for t, nombre, icon in ECO_TIPOS)
ecos = page_hero(crumbs(('Nosotros', 'nosotros.html'), ('Nuestro ecosistema', None)), 'Nuestro', '<em>ecosistema.</em>',
    'Portales, redes y encuentros que impulsamos para multiplicar el impacto de nuestro trabajo.',
    'conecta.jpg', [('portales', 'Portales')], back=('nosotros.html', 'Nosotros'))
ecos += '''
  <section class="pad" id="portales" aria-labelledby="eco-h">
    <div class="wrap">
''' + head2('Portales', 'Una red de', '<em>redes.</em>', 'Cada portal se centra en una parte de nuestra misión. Entra en cada uno para saber qué ofrece.', 'eco-h') + f'''      <div class="filters eco-filtros" role="group" aria-label="Filtrar portales por tipo" data-eco-filtros="#ecoGrid">
{eco_chips}      </div>
      <p class="sr-only" id="ecoFiltroEstado" aria-live="polite"></p>
      <div class="tiles c3 eco-grid" id="ecoGrid">
{eco_tiles}      </div>
    </div>
  </section>
''' + siblings('Nosotros', SIB_NOS, 'ecosistema.html')
write('ecosistema.html', 'Nuestro ecosistema · fundación conecta+', 'Los portales y redes del ecosistema de la fundación conecta+.', ecos, parent='nosotros.html')

for i, e in enumerate(ECO):
    prev, nxt = neighbours(ECO, i, lambda x: (x['href'], x['name']))
    pend = ('\n        ' + ph_note(e['pending'])) if e.get('pending') else ''
    pg = page_hero(crumbs(('Nosotros', 'nosotros.html'), ('Nuestro ecosistema', 'ecosistema.html'), (e['name'], None)),
        e['name'], None, e['short'], e['img'], cls=' hero-sm', back=('ecosistema.html', 'Nuestro ecosistema'))
    pg += f'''
  <section class="pad" id="info" aria-labelledby="info-h">
    <div class="wrap split">
      <div class="prose">
        <span class="kicker">Portal del ecosistema</span>
        <h2 class="h2" id="info-h" data-lines><span class="line"><span>Información sobre</span></span><span class="line"><span><em>{e['domain']}</em></span></span></h2>
        <p class="big" data-reveal>{e['short']}</p>
        <p data-reveal>{e['body']}</p>
        <div data-reveal>{portal_link(e['domain'], e['url'])}</div>{pend}
      </div>
      <div class="split-media" data-clip><img src="img/{e['img']}" alt="" loading="lazy"></div>
    </div>
  </section>
''' + portal_cta('cta-h', 'Visita', f'<em>{e["name"]}.</em>', e['body'], e['name'], e['url']) + pager('Más portales del ecosistema', prev, nxt)
    write(e['href'], f"{e['name']} · Nuestro ecosistema · fundación conecta+", f"Información sobre {e['domain']}, portal del ecosistema de la fundación conecta+.", pg, parent='nosotros.html')

# ================================================================== QUÉ HACEMOS (hub, antes «Misión»)
# Escenas del showreel de la cabecera: (página del área, rótulo, archivo en video/ sin extensión)
REEL = [
    ('voluntariado.html', 'Voluntariado', 'mision-voluntariado'),
    ('transformacion-digital.html', 'Transformación digital', 'mision-transformacion'),
    ('inclusion-digital.html', 'e-Inclusión digital', 'mision-inclusion'),
    ('formacion-tic.html', 'Formación TIC', 'mision-formacion'),
    ('jovenes.html', 'Jóvenes', 'mision-liderazgo'),
]
_reel_items = ''.join(f'<li data-src="video/{v}.mp4" data-poster="video/{v}.jpg" data-href="{h}" data-label="{t}"></li>' for h, t, v in REEL)
_reel_bars = ''.join('<i><b></b></i>' for _ in REEL)
REEL_MEDIA = f'''    <div class="hero-media reel" id="reel" aria-hidden="true">
      <video class="reel-v on" muted playsinline preload="auto" poster="video/{REEL[0][2]}.jpg"></video>
      <video class="reel-v" muted playsinline preload="auto"></video>
      <span class="reel-grade"></span>
      <ul class="reel-list" hidden>{_reel_items}</ul>
    </div>
    <a class="reel-cap" id="reelCap" href="{REEL[0][0]}">
      <span class="reel-bars" aria-hidden="true">{_reel_bars}</span>
      <span class="reel-meta"><span class="reel-n">01 / {len(REEL):02d}</span><b class="reel-t">{REEL[0][1]}</b><span class="reel-go">Ver área →</span></span>
    </a>
'''
qh = page_hero('Qué hacemos', 'Que nadie', 'quede <em>fuera.</em>',
    'Seis áreas de trabajo que combinan tecnología, formación y acompañamiento para reducir la brecha digital y social.',
    'contenido.jpg', [('areas', 'Ver las áreas')], media=REEL_MEDIA, cls=' hero-reel')
qh += '''
  <section class="pad" aria-labelledby="mis-h" style="padding-bottom:clamp(60px,8vw,110px)">
    <div class="wrap">
      <p class="manifesto-text" id="manifesto">Nuestra misión es que la tecnología sea una <em>vía real</em> de participación, aprendizaje y derechos para todas las personas — especialmente para quienes hoy se quedan <em>fuera.</em></p>
      <h2 class="sr-only" id="mis-h">Nuestra misión</h2>
    </div>
  </section>
''' + hub_section('Áreas de trabajo', 'Seis áreas,', '<em>un propósito.</em>', 'Cada área tiene su propio equipo, sus proyectos y, en muchos casos, su propio portal.', 'areas-h',
    [(a['href'], a['img'], f'0{i + 1}', a['short'], a['card'], 'Ver el área') for i, a in enumerate(AREAS)], sid='areas') \
    + '\n' + next_link('proyectos.html', 'Siguiente', 'Ver <em>proyectos</em>')
write('que-hacemos.html', 'Qué hacemos · fundación conecta+', 'Las áreas de trabajo de la fundación conecta+: formación TIC, observatorio, voluntariado, jóvenes, e-inclusión y transformación digital del tercer sector.', qh)
redirect('mision.html', 'que-hacemos.html')

# ------------------------------------------------------------------ ÁREAS (todas menos transformación digital, que tiene página propia)
for a in AREAS[:-1]:
    tk = ''.join(f'<li>{t}</li>' for t in a['ticks'])
    tg = ''.join(f'<span>{t}</span>' for t in a['tags'])
    pt = a['portal']
    plink = f'\n        <div data-reveal>{portal_link(pt[1], pt[2])}</div>' if pt else ''
    pg = page_hero(crumbs(('Qué hacemos', 'que-hacemos.html'), (a['short'], None)), a['h1'][0], a['h1'][1], a['lede'], a['img'],
        [('area', 'Qué hacemos'), ('proyectos-area', 'Proyectos')], back=('que-hacemos.html', 'Qué hacemos'))
    pg += f'''
  <section class="mline" id="area" aria-labelledby="area-h">
    <div class="wrap split">
      <div class="prose">
        <span class="kicker">{a['name']}</span>
        <h2 class="h2" id="area-h" data-lines><span class="line"><span>Qué hacemos</span></span></h2>
        <p class="big" data-reveal>{a['lead']}</p>
        <p data-reveal>{a['body']}</p>
        <ul class="ticks" data-reveal>{tk}</ul>
        <div class="tags" data-reveal>{tg}</div>{plink}
      </div>
      <div class="split-media" data-clip><img src="img/{a['img']}" alt="{a['alt']}" loading="lazy"></div>
    </div>
  </section>
'''
    if pt:
        pg += portal_cta('cta-h', 'Conoce', f'<em>{pt[0]}.</em>', pt[3], pt[0], pt[2])
    pg += area_projects(a['cat']) + siblings('Qué hacemos', SIB_AREAS, a['href'])
    write(a['href'], f"{a['name']} · fundación conecta+", a['lede'], pg, parent='que-hacemos.html')

# ================================================================== PROYECTOS (hub)
PROY_MEDIA = '''    <div class="hero-media city" aria-hidden="true">
      <video class="city-v" muted playsinline loop autoplay preload="auto" poster="video/proyectos-ciudad.jpg"><source src="video/proyectos-ciudad.mp4" type="video/mp4"></video>
      <span class="city-grade"></span>
      <canvas class="city-arcs" id="cityArcs"></canvas>
    </div>
'''
proyectos = page_hero('Proyectos', 'Proyectos que', 'dejan <em>huella.</em>',
    'Iniciativas en España y en el resto del mundo para que la tecnología abra puertas en lugar de cerrarlas.',
    'tech.jpg', [('ambitos', 'Nacionales e internacionales')], 'center 30%', media=PROY_MEDIA, cls=' hero-city')
proyectos += hub_section('Proyectos', 'Cerca y', '<em>lejos.</em>', 'Proyectos en nuestras cuatro sedes y alianzas con Europa e Iberoamérica.', 'amb-h', [
        ('proyectos-nacionales.html', 'news-campamentos.jpg', f'{len(PROJ_NAC):02d}', 'Proyectos nacionales', 'Andalucía, Madrid, Cataluña y Galicia: proyectos cercanos, diseñados con cada comunidad.', 'Ver proyectos'),
        ('proyectos-internacionales.html', 'news-internacional.jpg', f'{len(PROJ_INT):02d}', 'Proyectos internacionales', 'Una red que cruza fronteras, de Europa a Iberoamérica.', 'Ver proyectos'),
    ], ' two', sid='ambitos') + '''
  <section class="people" aria-hidden="true" style="padding-block:clamp(40px,6vw,80px)">
    <div class="ticker" data-speed="-0.35"></div>
  </section>
''' + next_link('recursos.html', 'Siguiente', 'Explorar <em>recursos</em>')
write('proyectos.html', 'Proyectos · fundación conecta+', 'Proyectos nacionales e internacionales de la fundación conecta+.', proyectos)

SIB_PROY = [('proyectos-nacionales.html', 'Proyectos nacionales', 'En nuestras cuatro sedes.'),
            ('proyectos-internacionales.html', 'Proyectos internacionales', 'Una red que cruza fronteras.')]

# ------------------------------------------------------------------ PROYECTOS NACIONALES
filters = ''.join(f'        <button type="button" data-filter="{a["cat"]}" aria-pressed="false">{a["short"]}</button>\n' for a in AREAS)
nac = page_hero(crumbs(('Proyectos', 'proyectos.html'), ('Proyectos nacionales', None)), 'En nuestras', '<em>cuatro sedes.</em>',
    'Andalucía, Madrid, Cataluña y Galicia: proyectos cercanos, diseñados con cada comunidad.',
    'news-campamentos.jpg', [('nacionales', 'Ver proyectos')], back=('proyectos.html', 'Proyectos'))
nac += '''
  <section class="pad" id="nacionales" aria-labelledby="nac-h">
    <div class="wrap">
''' + head2('Proyectos nacionales', 'Filtra por', '<em>área.</em>', None, 'nac-h') + '''      <div class="filters" data-filter-group="#pgridNac" role="group" aria-label="Filtrar proyectos por área">
        <button type="button" data-filter="all" aria-pressed="true">Todos</button>
''' + filters + '''      </div>
      <div class="pgrid" id="pgridNac">
''' + ''.join(pcard(p, f'{(i % 3) * .08:.2f}s') for i, p in enumerate(PROJ_NAC)) + '''      </div>
    </div>
  </section>
''' + siblings('Proyectos', SIB_PROY, 'proyectos-nacionales.html')
write('proyectos-nacionales.html', 'Proyectos nacionales · fundación conecta+', 'Proyectos de la fundación conecta+ en Andalucía, Madrid, Cataluña y Galicia.', nac, parent='proyectos.html')

# ------------------------------------------------------------------ PROYECTOS INTERNACIONALES
pins = ''.join(f'''        <a class="pin-card" href="{p['href']}" data-pin="{p['pin']}" data-lat="{p['lat']}" data-lon="{p['lon']}" data-label="{p['title']}" data-reveal style="--d:{i * .07:.2f}s">
          <span class="pin-card-top"><span class="pin-dot" aria-hidden="true"></span>{p['zone']}</span>
          <h3>{p['title']}</h3>
          <p>{p['text']}</p>
          <span class="pin-more">Ver proyecto →</span>
        </a>
''' for i, p in enumerate(PROJ_INT))
intl = page_hero(crumbs(('Proyectos', 'proyectos.html'), ('Proyectos internacionales', None)), 'Una red que', '<em>cruza fronteras.</em>',
    'Desde nuestras cuatro sedes en España tejemos alianzas con Europa e Iberoamérica.',
    'news-internacional.jpg', [('internacionales', 'Ver el mapa')], back=('proyectos.html', 'Proyectos'))
intl += '''
  <section class="pad" id="internacionales" aria-labelledby="int-h" style="background:var(--bg-2)">
    <div class="wrap">
''' + head2('Proyectos internacionales', 'Del mapa', 'al <em>proyecto.</em>', 'Pasa el cursor por cada proyecto para verlo en el mapa, y entra para conocerlo.', 'int-h') + f'''      <div class="flatmap" id="flatmap" data-reveal>
        <canvas class="flatmap-canvas" role="img" aria-label="Mapa de proyectos internacionales: España conectada con Europa e Iberoamérica"></canvas>
      </div>
      <div class="pin-cards">
{pins}      </div>
    </div>
  </section>
''' + siblings('Proyectos', SIB_PROY, 'proyectos-internacionales.html')
write('proyectos-internacionales.html', 'Proyectos internacionales · fundación conecta+', 'Proyectos internacionales de la fundación conecta+ en Europa e Iberoamérica.', intl, parent='proyectos.html')

# ------------------------------------------------------------------ PROYECTO CONCRETO
def project_page(p, i, lst, list_href, list_name):
    prev, nxt = neighbours(lst, i, lambda x: (x['href'], x['title']))
    cats = p.get('cat', '').split()
    area = AREA_BY_CAT.get(cats[0]) if cats else None
    area_btn = (f'<a class="btn btn-ghost magnetic" href="{area["href"]}">Área: {area["short"]} <span class="arr">→</span></a>' if area else '')
    tag = p.get('tag') or p.get('zone')
    pg = page_hero(crumbs(('Proyectos', 'proyectos.html'), (list_name, list_href), (p['title'], None)),
        p['title'], None, p['text'], p['img'], cls=' hero-sm', back=(list_href, list_name))
    pg += f'''
  <section class="pad" id="proyecto" aria-labelledby="pr-h">
    <div class="wrap split">
      <div class="prose">
        <span class="kicker">{tag}</span>
        <h2 class="h2" id="pr-h" data-lines><span class="line"><span>Sobre el</span></span><span class="line"><span><em>proyecto.</em></span></span></h2>
        <p class="big" data-reveal>{p['text']}</p>
        <p data-reveal>{p['body']}</p>
        {ph_note('Faltan las fechas, las sedes participantes, los financiadores y los resultados del proyecto.')}
        <div data-reveal style="display:flex;gap:10px;flex-wrap:wrap">{area_btn}<a class="btn btn-tec magnetic" href="escribenos.html">Quiero participar <span class="arr">→</span></a></div>
      </div>
      <div class="split-media" data-clip><img src="img/{p['img']}" alt="{p['alt']}" loading="lazy"></div>
    </div>
  </section>
''' + pager(f'Más {list_name.lower()}', prev, nxt)
    write(p['href'], f"{p['title']} · Proyectos · fundación conecta+", p['text'], pg, parent='proyectos.html')

for i, p in enumerate(PROJ_NAC):
    project_page(p, i, PROJ_NAC, 'proyectos-nacionales.html', 'Proyectos nacionales')
for i, p in enumerate(PROJ_INT):
    project_page(p, i, PROJ_INT, 'proyectos-internacionales.html', 'Proyectos internacionales')

# ================================================================== RECURSOS (hub)
recursos = page_hero('Recursos', 'Aprende,', 'descarga, <em>consulta.</em>',
    'Noticias, publicaciones, documentos de transparencia y formación online, reunidos en un solo lugar.',
    'news-formacion.jpg', [('secciones', 'Ver recursos')])
recursos += hub_section('Recursos', 'Todo en', '<em>un lugar.</em>', None, 'rec-h', [
        ('blog.html', 'news-voluntariado.jpg', f'{len(NEWS):02d}', 'Blog y noticias', 'Lo último de la red.', 'Leer'),
        ('publicaciones.html', 'pub-memoria.jpg', f'{len(PUBS):02d}', 'Publicaciones', 'Memorias, guías y materiales descargables.', 'Descargar'),
        ('transparencia.html', 'news-ens.jpg', 'PDF', 'Transparencia', 'Cuentas claras y documentos de la fundación.', 'Consultar'),
        ('preguntas-frecuentes.html', 'conexion-personas.jpg', 'FAQ', 'Preguntas frecuentes', 'Respuestas a las dudas más habituales.', 'Ver respuestas'),
        ('campus.html', 'tech.jpg', 'Online', 'Campus Virtual', 'Cursos online a tu ritmo.', 'Entrar'),
    ], sid='secciones') + '\n' + next_link('contacto.html', 'Siguiente', 'Ir a <em>contacto</em>')
write('recursos.html', 'Recursos · fundación conecta+', 'Blog, publicaciones, transparencia, preguntas frecuentes y Campus Virtual de la fundación conecta+.', recursos)

# ------------------------------------------------------------------ BLOG
blog = page_hero(crumbs(('Recursos', 'recursos.html'), ('Blog y noticias', None)), 'Lo último', 'de <em>la red.</em>',
    'Noticias, convocatorias y novedades de la fundación y de los proyectos.',
    'news-voluntariado.jpg', [('blog', 'Noticias')], back=('recursos.html', 'Recursos'))
blog += '''
  <section class="pad" id="blog" aria-labelledby="blog-h">
    <div class="wrap">
''' + head2('Blog y noticias', 'Lo que está', '<em>pasando.</em>', None, 'blog-h') + '''      <div class="filters" data-filter-group="#rlistBlog" role="group" aria-label="Filtrar noticias">
        <button type="button" data-filter="all" aria-pressed="true">Todo</button>
        <button type="button" data-filter="calidad" aria-pressed="false">Calidad</button>
        <button type="button" data-filter="formacion" aria-pressed="false">Formación</button>
        <button type="button" data-filter="comunidad" aria-pressed="false">Comunidad</button>
        <button type="button" data-filter="internacional" aria-pressed="false">Internacional</button>
      </div>
      <div class="rlist" id="rlistBlog">
''' + ''.join(ritem(n['tag'], n['title'], 'Noticia', n['cat'], n['href']) for n in NEWS) + '''      </div>
    </div>
  </section>
''' + siblings('Recursos', SIB_REC, 'blog.html')
write('blog.html', 'Blog y noticias · fundación conecta+', 'Noticias y novedades de la fundación conecta+.', blog, parent='recursos.html')

for i, n in enumerate(NEWS):
    prev, nxt = neighbours(NEWS, i, lambda x: (x['href'], x['title']))
    pg = page_hero(crumbs(('Recursos', 'recursos.html'), ('Blog y noticias', 'blog.html'), (n['tag'], None)),
        n['title'], None, n['lead'], n['img'], cls=' hero-sm', back=('blog.html', 'Blog y noticias'))
    pg += f'''
  <section class="pad" id="noticia" aria-labelledby="nw-h">
    <div class="wrap split">
      <article class="prose">
        <span class="kicker">{n['tag']}</span>
        <h2 class="sr-only" id="nw-h">Contenido de la noticia</h2>
        <p class="big" data-reveal>{n['lead']}</p>
        {ph_note('Falta el texto completo de la noticia, la fecha de publicación y la autoría.')}
        <div data-reveal><a class="btn btn-ghost magnetic" href="blog.html">Todas las noticias <span class="arr">→</span></a></div>
      </article>
      <div class="split-media" data-clip><img src="img/{n['img']}" alt="{n['alt']}" loading="lazy"></div>
    </div>
  </section>
''' + pager('Más noticias', prev, nxt)
    write(n['href'], f"{n['title']} · Blog · fundación conecta+", n['lead'], pg, parent='recursos.html')

# ------------------------------------------------------------------ PUBLICACIONES
pubs = page_hero(crumbs(('Recursos', 'recursos.html'), ('Publicaciones', None)), 'Para leer', 'y <em>compartir.</em>',
    'Memorias, guías y materiales que elaboramos a partir de nuestro trabajo.',
    'pub-guia.jpg', [('publicaciones', 'Publicaciones')], back=('recursos.html', 'Recursos'))
pubs += '''
  <section class="pad values-sec" id="publicaciones" aria-labelledby="pub-h">
    <div class="wrap">
''' + head2('Publicaciones y descargables', 'Materiales', '<em>abiertos.</em>', None, 'pub-h') \
    + hub_cards([(p['href'], p['img'], p['n'], p['title'], p['text'], 'Ver y descargar') for p in PUBS]) + '''    </div>
  </section>
''' + siblings('Recursos', SIB_REC, 'publicaciones.html')
write('publicaciones.html', 'Publicaciones · fundación conecta+', 'Memorias, guías y materiales descargables de la fundación conecta+.', pubs, parent='recursos.html')

for i, p in enumerate(PUBS):
    prev, nxt = neighbours(PUBS, i, lambda x: (x['href'], x['title']))
    pg = page_hero(crumbs(('Recursos', 'recursos.html'), ('Publicaciones', 'publicaciones.html'), (p['title'], None)),
        p['title'], None, p['text'], p['img'], cls=' hero-sm', back=('publicaciones.html', 'Publicaciones'))
    pg += f'''
  <section class="pad" id="publicacion" aria-labelledby="pb-h">
    <div class="wrap split">
      <div class="prose">
        <span class="kicker">{p['n']}</span>
        <h2 class="h2" id="pb-h" data-lines><span class="line"><span>Contenido de la</span></span><span class="line"><span><em>publicación.</em></span></span></h2>
        <p class="big" data-reveal>{p['text']}</p>
        {ph_note('Falta el archivo para descargar, el año de edición y un resumen del contenido.')}
        <div data-reveal><a class="btn btn-tec magnetic" href="#" download>Descargar documento <span class="arr">↓</span></a></div>
      </div>
      <div class="split-media" data-clip><img src="img/{p['img']}" alt="" loading="lazy"></div>
    </div>
  </section>
''' + pager('Más publicaciones', prev, nxt)
    write(p['href'], f"{p['title']} · Publicaciones · fundación conecta+", p['text'], pg, parent='recursos.html')

# ------------------------------------------------------------------ TRANSPARENCIA
tr = page_hero(crumbs(('Recursos', 'recursos.html'), ('Transparencia', None)), 'Cuentas', '<em>claras.</em>',
    'Rendir cuentas es parte de nuestro compromiso con las personas, las entidades y las instituciones que confían en nosotros.',
    'news-ens.jpg', [('transparencia', 'Documentos')], back=('recursos.html', 'Recursos'))
tr += '''
  <section class="pad" id="transparencia" aria-labelledby="tr-h">
    <div class="wrap">
''' + head2('Transparencia', 'Documentación', '<em>para descargar.</em>', None, 'tr-h') + '''      <div class="rlist">
''' + ritem('Documento', 'Estatutos de la fundación', 'PDF', '') \
    + ritem('Documento', 'Composición del patronato', 'PDF', '') \
    + ritem('Economía', 'Cuentas anuales e informe de auditoría', 'PDF', '') \
    + ritem('Calidad', 'Política de calidad y medio ambiente (ISO 9001 · ISO 14001)', 'PDF', '') \
    + ritem('Seguridad', 'Política de seguridad de la información (ENS · ISO 27001)', 'PDF', '') \
    + ritem('Ética', 'Canal de denuncia', 'Página', '', 'canal-denuncia.html') + '''      </div>
      <div style="margin-top:32px">''' + ph_note('Faltan los archivos PDF de los documentos de transparencia.') + '''</div>
    </div>
  </section>
''' + siblings('Recursos', SIB_REC, 'transparencia.html')
write('transparencia.html', 'Transparencia · fundación conecta+', 'Estatutos, cuentas, patronato y políticas de la fundación conecta+.', tr, parent='recursos.html')

# ------------------------------------------------------------------ PREGUNTAS FRECUENTES
faq = page_hero(crumbs(('Recursos', 'recursos.html'), ('Preguntas frecuentes', None)), 'Resolvemos', 'tus <em>dudas.</em>',
    'Las preguntas que más nos hacéis, con sus respuestas.',
    'conexion-personas.jpg', [('faq', 'Preguntas')], back=('recursos.html', 'Recursos'))
faq += '''
  <section class="pad" id="faq" aria-labelledby="faq-h">
    <div class="wrap">
''' + head2('Preguntas frecuentes', 'Preguntas y', '<em>respuestas.</em>', None, 'faq-h') + '''      <div class="faq" data-reveal>
        <details><summary>¿Cómo puedo hacerme voluntario?</summary><p>Rellena el formulario de <a href="hazte-voluntario.html">Hazte voluntario/a</a>. Te escribiremos para conocerte y contarte los proyectos disponibles cerca de ti.</p></details>
        <details><summary>¿Las formaciones tienen coste?</summary><p>Muchas de nuestras formaciones son gratuitas para las personas participantes gracias a la financiación pública y privada. Consulta cada convocatoria.</p></details>
        <details><summary>Soy una entidad social, ¿cómo podéis ayudarnos?</summary><p>A través del área de <a href="transformacion-digital.html">Transformación digital y Gestión del Tercer Sector</a>, incluido el servicio SAAD de asesoría digital gratuita. Escríbenos y valoramos juntos vuestras necesidades.</p></details>
        <details><summary>¿Cómo puedo hacer una donación?</summary><p>Desde la página <a href="dona.html">Dona</a> puedes elegir el importe y la periodicidad de tu aportación.</p></details>
        <details><summary>¿Cómo entro en el Campus Virtual?</summary><p>Desde la página <a href="campus.html">Campus Virtual</a>, con el usuario y la contraseña que recibiste al inscribirte en el curso.</p></details>
        <details><summary>¿Dónde estáis?</summary><p>Tenemos sedes en Andalucía, Madrid, Cataluña y Galicia. Consulta las direcciones en <a href="sedes.html">Sedes</a>.</p></details>
      </div>
      <div style="margin-top:40px" data-reveal><a class="btn btn-ghost magnetic" href="escribenos.html">¿Otra pregunta? Escríbenos <span class="arr">→</span></a></div>
    </div>
  </section>
''' + siblings('Recursos', SIB_REC, 'preguntas-frecuentes.html')
write('preguntas-frecuentes.html', 'Preguntas frecuentes · fundación conecta+', 'Respuestas a las preguntas más habituales sobre la fundación conecta+.', faq, parent='recursos.html')

# ------------------------------------------------------------------ CAMPUS VIRTUAL
campus = page_hero(crumbs(('Recursos', 'recursos.html'), ('Campus Virtual', None)), 'Aprende a tu', '<em>ritmo.</em>',
    'Cursos online de competencias digitales y formación para la inserción laboral, con acompañamiento de nuestro equipo.',
    'tech.jpg', [('acceso', 'Acceder')], back=('recursos.html', 'Recursos'))
campus += '''
  <section class="pad" id="acceso" aria-labelledby="cv-h">
    <div class="wrap contact-grid">
      <div class="prose">
        <span class="kicker">Campus Virtual</span>
        <h2 class="h2" id="cv-h" data-lines><span class="line"><span>Accede a</span></span><span class="line"><span><em>tus cursos.</em></span></span></h2>
        <p data-reveal>Entra con el usuario y la contraseña que recibiste al inscribirte. Si aún no tienes cuenta, consulta los cursos abiertos en el área de <a href="formacion-tic.html">Formación TIC</a>.</p>
        ''' + ph_note('Falta la dirección del Campus Virtual: el acceso todavía no redirige a la plataforma.') + '''
      </div>
      <div class="contact-form" data-reveal>
        <form id="campusForm" novalidate data-msg="El acceso al Campus Virtual estará disponible muy pronto.">
          <div class="fields">
            <div class="field full"><label for="cvUser">Usuario o correo electrónico</label><input id="cvUser" name="usuario" required autocomplete="username"></div>
            <div class="field full"><label for="cvPass">Contraseña</label><input id="cvPass" name="password" type="password" required autocomplete="current-password"></div>
          </div>
          <button type="submit" class="btn btn-tec magnetic">Entrar al Campus <span class="arr">→</span></button>
        </form>
        <p class="form-note" aria-live="polite"></p>
      </div>
    </div>
  </section>
''' + siblings('Recursos', SIB_REC, 'campus.html')
write('campus.html', 'Campus Virtual · fundación conecta+', 'Acceso al Campus Virtual de formación online de la fundación conecta+.', campus, parent='recursos.html')

# ================================================================== CONTACTO (hub)
contacto = page_hero('Contacto', 'Hablemos,', '<em>conectemos.</em>',
    '¿Quieres participar, colaborar o necesitas información? Escríbenos o acércate a tu sede más cercana.',
    'news-tercer-sector.jpg', [('secciones', 'Cómo contactar')])
contacto += '''
  <section class="pad" aria-labelledby="direct-h" style="padding-bottom:0">
    <div class="wrap">
      <span class="kicker">Directo</span>
      <h2 class="sr-only" id="direct-h">Contacto directo</h2>
      <div data-reveal style="margin-top:22px">
        <a class="big-link" href="mailto:info@conectamas.org">info@conectamas.org</a>
        <a class="big-link" href="tel:+34934745546">934 745 546</a>
      </div>
    </div>
  </section>
''' + hub_section('Contacto', 'Elige', '<em>cómo.</em>', None, 'con-h', [
        ('escribenos.html', 'news-tercer-sector.jpg', '01', 'Escríbenos', 'Cuéntanos qué necesitas y te responderemos lo antes posible.', 'Escribir'),
        ('sedes.html', 'hero-personas.jpg', '02', 'Sedes', 'Cataluña, Madrid, Andalucía y Galicia.', 'Ver sedes'),
    ], ' two', sid='secciones') + '\n' + next_link('colabora.html', 'Siguiente', '<em>Colabora</em>')
write('contacto.html', 'Contacto · fundación conecta+', 'Contacta con la fundación conecta+: formulario y sedes.', contacto)

# ------------------------------------------------------------------ ESCRÍBENOS
esc = page_hero(crumbs(('Contacto', 'contacto.html'), ('Escríbenos', None)), 'Cuéntanos', '<em>qué necesitas.</em>',
    'Te responderemos lo antes posible.', 'news-tercer-sector.jpg', [('escribenos', 'Formulario')], back=('contacto.html', 'Contacto'))
esc += '''
  <section class="pad net-sec" id="escribenos" aria-labelledby="form-h">
    <canvas class="cta-net" data-theme="dark" data-form="contactForm" aria-hidden="true"></canvas>
    <div class="wrap contact-grid">
      <div class="prose">
        <span class="kicker">Escríbenos</span>
        <h2 class="h2" id="form-h" data-lines><span class="line"><span>Formulario</span></span><span class="line"><span><em>de contacto.</em></span></span></h2>
        <p data-reveal>También puedes llamarnos o escribirnos directamente:</p>
        <div data-reveal>
          <a class="big-link" href="mailto:info@conectamas.org">info@conectamas.org</a>
          <a class="big-link" href="tel:+34934745546">934 745 546</a>
        </div>
        <div data-reveal><a class="btn btn-ghost magnetic" href="sedes.html">Ver nuestras sedes <span class="arr">→</span></a></div>
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
            <label class="check full"><input type="checkbox" required> He leído y acepto la <a href="aviso-legal.html#privacidad">política de privacidad</a>.</label>
          </div>
          <button type="submit" class="btn btn-tec magnetic">Enviar mensaje <span class="arr">→</span></button>
        </form>
        <p class="form-note" aria-live="polite"></p>
      </div>
    </div>
  </section>
''' + siblings('Contacto', SIB_CON, 'escribenos.html')
write('escribenos.html', 'Escríbenos · fundación conecta+', 'Formulario de contacto de la fundación conecta+.', esc, parent='contacto.html')

# ------------------------------------------------------------------ SEDES
sedes = page_hero(crumbs(('Contacto', 'contacto.html'), ('Sedes', None)), 'Cerca', 'de <em>ti.</em>',
    'Estamos presentes en cuatro comunidades autónomas.', 'hero-personas.jpg', [('sedes', 'Sedes')], back=('contacto.html', 'Contacto'))
sedes += '''
  <section class="pad" id="sedes" aria-labelledby="sedes-h">
    <div class="wrap split">
      <div class="prose">
        <span class="kicker">Sedes</span>
        <h2 class="h2" id="sedes-h" data-lines><span class="line"><span>Dónde</span></span><span class="line"><span><em>estamos.</em></span></span></h2>
        <p data-reveal>Escríbenos y te pondremos en contacto con la sede más cercana.</p>
        ''' + ph_note('Faltan las direcciones y teléfonos de las sedes de Madrid, Andalucía y Galicia.') + '''
        <div data-reveal><a class="btn btn-tec magnetic" href="escribenos.html">Escríbenos <span class="arr">→</span></a></div>
      </div>
      <div class="sedes" data-reveal>
        <div class="sede"><b>Cataluña</b><span>C/ Riu Anoia, 42-54<br>08820 El Prat de Llobregat<br><a href="tel:+34934745546">934 745 546</a></span></div>
        <div class="sede"><b>Madrid</b><span>Sede territorial<br><a href="mailto:info@conectamas.org">info@conectamas.org</a></span></div>
        <div class="sede"><b>Andalucía</b><span>Sede territorial<br><a href="mailto:info@conectamas.org">info@conectamas.org</a></span></div>
        <div class="sede"><b>Galicia</b><span>Sede territorial<br><a href="mailto:info@conectamas.org">info@conectamas.org</a></span></div>
      </div>
    </div>
  </section>
''' + siblings('Contacto', SIB_CON, 'sedes.html')
write('sedes.html', 'Sedes · fundación conecta+', 'Sedes de la fundación conecta+ en Cataluña, Madrid, Andalucía y Galicia.', sedes, parent='contacto.html')

# ================================================================== COLABORA (hub)
col = page_hero('Colabora', 'Súmate', 'a <em>la red.</em>',
    'Hay muchas maneras de sumarse a conecta+: tu tiempo, tu aportación o tu entidad. Elige la tuya.',
    'news-voluntariado.jpg', [('formas', 'Formas de colaborar')])
col += hub_section('Colabora', 'Formas de', '<em>participar.</em>', None, 'col-h', [
        ('hazte-voluntario.html', 'news-voluntariado.jpg', '01', 'Hazte voluntario/a', 'Dedica tu tiempo y tu talento a acompañar a otras personas.', 'Quiero participar'),
        ('dona.html', 'conecta.jpg', '02', 'Dona', 'Tu aportación sostiene proyectos de inclusión digital y educación.', 'Hacer un donativo'),
        ('unete.html', 'conexion-personas.jpg', '03', 'Únete a la red', 'Suma tu entidad a la red contra la brecha digital.', 'Unirme'),
    ], sid='formas') + '''
  <section class="pad" aria-labelledby="emp-h">
    <div class="wrap split rev">
      <div class="prose">
        <span class="kicker">Empresas y entidades</span>
        <h2 class="h2" id="emp-h" data-lines><span class="line"><span>Alianzas con</span></span><span class="line"><span><em>impacto.</em></span></span></h2>
        <p data-reveal>Voluntariado corporativo, proyectos conjuntos y alianzas con administraciones, entidades y empresas comprometidas con la inclusión digital.</p>
        <div data-reveal><a class="btn btn-ghost magnetic" href="escribenos.html">Hablemos <span class="arr">→</span></a></div>
      </div>
      <div class="split-media wide" data-clip><img src="img/news-tercer-sector.jpg" alt="Dos personas revisando código en un portátil" loading="lazy"></div>
    </div>
  </section>
''' + next_link('index.html', 'Volver', 'Al <em>inicio</em>')
write('colabora.html', 'Colabora · fundación conecta+', 'Hazte voluntario, dona o únete a la red de la fundación conecta+.', col)

# ------------------------------------------------------------------ HAZTE VOLUNTARIO/A
sede_opts = ''.join(f'<option>{s}</option>' for s in ['Cataluña', 'Madrid', 'Andalucía', 'Galicia', 'Online'])
area_opts = ''.join(f'<option>{a["short"]}</option>' for a in AREAS) + '<option>Lo que haga falta</option>'
vol = page_hero(crumbs(('Colabora', 'colabora.html'), ('Hazte voluntario/a', None)), 'Hazte', '<em>voluntario/a.</em>',
    'Dedica tu tiempo y tu talento a acompañar a otras personas en su camino digital.',
    'news-voluntariado.jpg', [('inscripcion', 'Inscríbete')], back=('colabora.html', 'Colabora'))
vol += f'''
  <section class="pad net-sec" id="inscripcion" aria-labelledby="vol-h">
    <canvas class="cta-net" data-theme="dark" data-form="volForm" aria-hidden="true"></canvas>
    <div class="wrap contact-grid">
      <div class="prose">
        <span class="kicker">Inscripción</span>
        <h2 class="h2" id="vol-h" data-lines><span class="line"><span>Cuéntanos</span></span><span class="line"><span><em>quién eres.</em></span></span></h2>
        <p data-reveal>Te escribiremos para conocerte, contarte los proyectos disponibles cerca de ti y acompañarte en la formación inicial.</p>
        <ul class="ticks" data-reveal><li>Formación y acompañamiento desde el primer día</li><li>Proyectos presenciales y online</li><li>Tú decides cuánto tiempo dedicas</li></ul>
      </div>
      <div class="contact-form" data-reveal>
        <form id="volForm" novalidate data-msg="¡Gracias! Hemos recibido tu inscripción y te escribiremos muy pronto.">
          <div class="fields">
            <div class="field"><label for="vName">Nombre y apellidos</label><input id="vName" name="nombre" required autocomplete="name"></div>
            <div class="field"><label for="vMail">Correo electrónico</label><input id="vMail" name="email" type="email" required autocomplete="email"></div>
            <div class="field"><label for="vTel">Teléfono (opcional)</label><input id="vTel" name="telefono" type="tel" autocomplete="tel"></div>
            <div class="field"><label for="vSede">Sede</label><select id="vSede" name="sede">{sede_opts}</select></div>
            <div class="field full"><label for="vArea">Área que te interesa</label><select id="vArea" name="area">{area_opts}</select></div>
            <div class="field full"><label for="vMsg">Disponibilidad y experiencia</label><textarea id="vMsg" name="mensaje" required></textarea></div>
            <label class="check full"><input type="checkbox" required> He leído y acepto la <a href="aviso-legal.html#privacidad">política de privacidad</a>.</label>
          </div>
          <button type="submit" class="btn btn-tec magnetic">Enviar inscripción <span class="arr">→</span></button>
        </form>
        <p class="form-note" aria-live="polite"></p>
      </div>
    </div>
  </section>
''' + siblings('Colabora', SIB_COL, 'hazte-voluntario.html')
write('hazte-voluntario.html', 'Hazte voluntario/a · fundación conecta+', 'Inscríbete como persona voluntaria en la fundación conecta+.', vol, parent='colabora.html')

# ------------------------------------------------------------------ DONA
dona = page_hero(crumbs(('Colabora', 'colabora.html'), ('Dona', None)), 'Tu aportación', '<em>conecta.</em>',
    'Cada donativo se convierte en formación, acompañamiento y acceso a la tecnología para quien más lo necesita.',
    'conecta.jpg', [('donar', 'Donar')], back=('colabora.html', 'Colabora'))
dona += '''
  <section class="pad net-sec" id="donar" aria-labelledby="don-h">
    <canvas class="cta-net" data-theme="dark" data-form="donaForm" aria-hidden="true"></canvas>
    <div class="wrap contact-grid">
      <div class="prose">
        <span class="kicker">Donativo</span>
        <h2 class="h2" id="don-h" data-lines><span class="line"><span>Haz tu</span></span><span class="line"><span><em>donativo.</em></span></span></h2>
        <p data-reveal>Elige el importe y la periodicidad. Las aportaciones periódicas nos ayudan a planificar proyectos a largo plazo.</p>
        ''' + ph_note('Falta conectar una pasarela de pago y confirmar la información fiscal de los donativos.') + '''
      </div>
      <div class="contact-form" data-reveal>
        <form id="donaForm" novalidate data-msg="¡Gracias! La pasarela de pago aún no está activa: te escribiremos para completar tu donativo.">
          <div class="fields">
            <div class="field"><label for="dAmount">Importe</label><select id="dAmount" name="importe"><option>10 €</option><option selected>25 €</option><option>50 €</option><option>100 €</option><option>Otro importe</option></select></div>
            <div class="field"><label for="dFreq">Periodicidad</label><select id="dFreq" name="periodicidad"><option>Una sola vez</option><option>Mensual</option><option>Anual</option></select></div>
            <div class="field"><label for="dName">Nombre y apellidos</label><input id="dName" name="nombre" required autocomplete="name"></div>
            <div class="field"><label for="dMail">Correo electrónico</label><input id="dMail" name="email" type="email" required autocomplete="email"></div>
            <label class="check full"><input type="checkbox" required> He leído y acepto la <a href="aviso-legal.html#privacidad">política de privacidad</a>.</label>
          </div>
          <button type="submit" class="btn btn-tec magnetic">Continuar con el donativo <span class="arr">→</span></button>
        </form>
        <p class="form-note" aria-live="polite"></p>
      </div>
    </div>
  </section>
''' + siblings('Colabora', SIB_COL, 'dona.html')
write('dona.html', 'Dona · fundación conecta+', 'Haz un donativo a la fundación conecta+.', dona, parent='colabora.html')

# ------------------------------------------------------------------ ÚNETE A LA RED
red = next(e for e in ECO if e['slug'] == 'red-conecta')
unete = page_hero(crumbs(('Colabora', 'colabora.html'), ('Únete a la red', None)), 'Únete a', 'la <em>red.</em>',
    'Entidades que trabajan juntas para que nadie quede fuera del mundo digital.',
    'conexion-personas.jpg', [('red', 'La red')], back=('colabora.html', 'Colabora'))
unete += f'''
  <section class="pad" id="red" aria-labelledby="red-h">
    <div class="wrap split">
      <div class="prose">
        <span class="kicker">Red Conecta</span>
        <h2 class="h2" id="red-h" data-lines><span class="line"><span>Una red contra</span></span><span class="line"><span><em>la brecha digital.</em></span></span></h2>
        <p class="big" data-reveal>Más de veinte años de experiencia compartida entre entidades de todo el territorio.</p>
        <p data-reveal>La red crea espacios de acceso a las TIC, forma a personas dinamizadoras y ofrece formación en competencias digitales en municipios, barrios y colectivos con necesidades de inclusión e inserción laboral.</p>
        <div data-reveal>{portal_link(red['domain'], red['url'])}</div>
      </div>
      <div class="split-media" data-clip><img src="img/conexion-personas.jpg" alt="Personas conectadas" loading="lazy"></div>
    </div>
  </section>
''' + portal_cta('cta-h', 'Suma tu', '<em>entidad.</em>', 'La adhesión de entidades a la red se gestiona desde su portal.', 'Red Conecta', red['url']) \
    + siblings('Colabora', SIB_COL, 'unete.html')
write('unete.html', 'Únete a la red · fundación conecta+', 'Suma tu entidad a Red Conecta, la red contra la brecha digital.', unete, parent='colabora.html')

# ================================================================== PIE: BOLETÍN, CANAL DE DENUNCIA, AVISO LEGAL
bol = page_hero('Boletín único', 'Un correo', 'al <em>mes.</em>',
    'Novedades, convocatorias y formas de participar en la fundación conecta+, directamente en tu bandeja de entrada.',
    'footer-colinas.jpg', [('suscripcion', 'Suscribirme')])
bol += '''
  <section class="cta pad" id="suscripcion" aria-labelledby="bol-h">
    <canvas class="cta-net" data-form="boletinForm" aria-hidden="true"></canvas>
    <div class="wrap">
      <span class="kicker">Boletín único</span>
      <h2 id="bol-h" data-lines><span class="line"><span>Súmate a una red</span></span><span class="line"><span>que <em>transforma.</em></span></span></h2>
      <div class="cta-grid">
        <p data-reveal>Un único boletín con lo más importante de todas las áreas y portales de la fundación. Sin spam y con baja en un clic.</p>
        <div data-reveal style="--d:.1s">
          <form class="form" id="boletinForm" novalidate data-msg="¡Gracias por sumarte! Revisa tu correo para confirmar la suscripción.">
            <label for="boletinEmail" class="sr-only">Correo electrónico</label>
            <input type="email" id="boletinEmail" name="email" placeholder="tu@email.com" required autocomplete="email">
            <button type="submit" class="btn btn-mag">Suscríbete <span class="arr">→</span></button>
          </form>
          <p class="form-note">Al suscribirte aceptas la <a href="aviso-legal.html#privacidad">política de privacidad</a>.</p>
        </div>
      </div>
    </div>
  </section>
'''
write('boletin.html', 'Boletín único · fundación conecta+', 'Suscríbete al boletín de la fundación conecta+.', bol)

den = page_hero('Canal de denuncia', 'Canal de', '<em>denuncia.</em>',
    'Un canal seguro y confidencial para comunicar posibles irregularidades.',
    'bosque.jpg', [('canal', 'El canal'), ('preguntas', 'Preguntas')])
den += '''
  <section class="pad" id="canal" aria-labelledby="den-h">
    <div class="wrap split">
      <div class="prose">
        <span class="kicker">Sistema interno de información</span>
        <h2 class="h2" id="den-h" data-lines><span class="line"><span>Comunica con</span></span><span class="line"><span><em>protección.</em></span></span></h2>
        <p class="big" data-reveal>Puedes informar, con protección legal, de irregularidades que puedan constituir infracciones penales o administrativas graves.</p>
        <p data-reveal>Tu identidad es confidencial y no se revela sin tu consentimiento. Cada comunicación recibe un código y un acuse de recibo. Este canal no es un servicio de emergencias ni tramita reclamaciones comerciales.</p>
        ''' + ph_note('Falta la dirección del formulario externo del canal de denuncia.') + '''
        <div data-reveal><span class="btn btn-tec is-disabled" aria-disabled="true">Acceder al canal de denuncia</span></div>
      </div>
      <div class="split-media" data-clip><img src="img/bosque.jpg" alt="" loading="lazy"></div>
    </div>
  </section>

  <section class="pad" id="preguntas" aria-labelledby="denfaq-h" style="padding-top:0">
    <div class="wrap">
''' + head2('Preguntas y respuestas', 'Antes de', '<em>comunicar.</em>', None, 'denfaq-h') + '''      <div class="faq" data-reveal>
        <details><summary>¿Quién puede usar el canal?</summary><p>Personas trabajadoras, miembros del patronato, voluntariado, personas en prácticas o en formación, proveedores y contratistas, antiguos empleados y candidatos en procesos de selección.</p></details>
        <details><summary>¿Qué puedo comunicar?</summary><p>Hechos que puedan constituir infracciones penales o administrativas graves o muy graves, infracciones del Derecho de la Unión Europea y conductas contrarias a nuestros principios o normativa interna.</p></details>
        <details><summary>¿Puedo comunicarlo de forma anónima?</summary><p>Sí. Se aceptan comunicaciones anónimas, aunque su tramitación puede quedar limitada si no podemos pedirte más información.</p></details>
        <details><summary>¿Qué pasa después?</summary><p>Recibirás un código y un acuse de recibo con el que podrás seguir el estado de tu comunicación.</p></details>
      </div>
    </div>
  </section>
'''
write('canal-denuncia.html', 'Canal de denuncia · fundación conecta+', 'Canal de denuncia (sistema interno de información) de la fundación conecta+.', den)

legal_sec = lambda sid, k, l1, l2, text: f'''
  <section class="pad" id="{sid}" aria-labelledby="{sid}-h" style="padding-bottom:0">
    <div class="wrap">
      <div class="prose">
        <span class="kicker">{k}</span>
        <h2 class="h2" id="{sid}-h" data-lines><span class="line"><span>{l1}</span></span><span class="line"><span><em>{l2}</em></span></span></h2>
        <p data-reveal>{text}</p>
        {ph_note('Texto legal pendiente de redactar y revisar por la asesoría jurídica de la fundación.')}
      </div>
    </div>
  </section>
'''
legal = page_hero('Aviso legal y privacidad', 'Aviso legal', 'y <em>privacidad.</em>',
    'Condiciones de uso de la web, tratamiento de datos personales, cookies y accesibilidad.',
    'footer-colinas.jpg', [('aviso-legal', 'Aviso legal'), ('privacidad', 'Privacidad'), ('cookies', 'Cookies'), ('accesibilidad', 'Accesibilidad')])
legal += legal_sec('aviso-legal', 'Aviso legal', 'Condiciones', 'de uso.', 'Datos identificativos de la fundación, condiciones de uso del sitio web y propiedad intelectual de sus contenidos.') \
    + legal_sec('privacidad', 'Privacidad', 'Tus datos,', 'protegidos.', 'Quién trata tus datos, con qué finalidad, durante cuánto tiempo y cómo puedes ejercer tus derechos de acceso, rectificación, supresión, oposición, limitación y portabilidad.') \
    + legal_sec('cookies', 'Cookies', 'Política de', 'cookies.', 'Qué cookies utiliza la web y cómo puedes configurarlas. Ahora mismo solo usamos cookies técnicas necesarias.') \
    + legal_sec('accesibilidad', 'Accesibilidad', 'Declaración de', 'accesibilidad.', 'Nuestro compromiso para que la web pueda usarse con teclado, lectores de pantalla y movimiento reducido.') + '''
  <section class="pad" aria-label="Configurar cookies">
    <div class="wrap"><button type="button" class="btn btn-ghost" data-cookie-open>Configurar cookies</button></div>
  </section>
'''
write('aviso-legal.html', 'Aviso legal y privacidad · fundación conecta+', 'Aviso legal, política de privacidad, cookies y accesibilidad de la fundación conecta+.', legal)


# ================================================================== EQUIPO (subpágina de Nosotros)
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

eq = page_hero(crumbs(('Nosotros', 'nosotros.html'), ('Equipo y patronato', None)),
    'Las personas', 'detrás de <em>la red.</em>',
    'Un patronato comprometido y un equipo multidisciplinar que combina educación, tecnología y acción social en cuatro territorios.',
    'news-voluntariado.jpg', [('patronato', 'Patronato'), ('equipo', 'Equipo'), ('trabaja', 'Trabaja con nosotros')], 'center 30%', back=('nosotros.html', 'Nosotros'))
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
        <div data-reveal style="--d:.1s;display:flex;gap:10px;flex-wrap:wrap"><a class="btn btn-mag magnetic" href="escribenos.html">Envíanos tu candidatura <span class="arr">→</span></a></div>
      </div>
    </div>
  </section>
''' + siblings('Nosotros', SIB_NOS, 'equipo.html')
write('equipo.html', 'Equipo y patronato · fundación conecta+', 'El patronato y el equipo de la fundación conecta+.', eq, parent='nosotros.html')


# ================================================================== TRANSFORMACIÓN DIGITAL Y GESTIÓN DEL TERCER SECTOR (área de Qué hacemos)
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
dev_items += '        <li class="tx-dev-cta" data-reveal style="--d:.2s"><a href="escribenos.html"><span class="tx-mono">+</span>¿Tienes otra idea? Hablemos <b aria-hidden="true">→</b></a></li>\n'

GTS = next(e for e in ECO if e['slug'] == 'gestion-tercer-sector')
DONG = next(e for e in ECO if e['slug'] == 'digitalizaciong')

tx = f'''  <section class="page-hero tx-hero" aria-labelledby="page-h">
    <canvas class="tx-net" id="txNet" aria-hidden="true"></canvas>
    <div class="wrap">
      <a class="back-pill fade-up" href="que-hacemos.html"><span aria-hidden="true">←</span>Volver a Qué hacemos</a>
      <nav class="crumbs fade-up" aria-label="Ruta"><a href="index.html">Inicio</a><span aria-hidden="true">/</span><a href="que-hacemos.html">Qué hacemos</a><span aria-hidden="true">/</span><span>Transformación digital y Tercer Sector</span></nav>
      <p class="tx-status fade-up"><i aria-hidden="true"></i>conecta+ // equipo de transformación digital y gestión del tercer sector · online</p>
      <h1 id="page-h"><span class="line"><span>Transformación</span></span><span class="line"><span><em>digital.</em></span></span></h1>
      <p class="tx-prompt fade-up" aria-label="Desde el tercer sector, para el tercer sector"><span aria-hidden="true">&gt;</span> <span class="tx-typed" data-type="desde el tercer sector, para el tercer sector" aria-hidden="true"></span><b aria-hidden="true">_</b></p>
      <div class="page-hero-foot fade-up">
        <p>Somos el equipo de transformación digital y gestión del tercer sector de conecta+: técnicos, desarrolladores y profesionales del sector social que ayudan a las entidades a modernizarse e innovar.</p>
        <div class="anchors"><a href="#servicios">Servicios</a><a href="#tercer-sector">Gestión del Tercer Sector</a><a href="#digitalizaong">DigitalizaciONG</a><a href="#proyectos-area">Proyectos</a></div>
      </div>
    </div>
  </section>

  <section class="pad tx-grid-bg" id="servicios" aria-labelledby="srv-h">
    <div class="wrap">
''' + head2('Servicios', 'Tres formas de', '<em>ayudaros.</em>', 'Asesoría, formación y consultoría pensadas para las necesidades reales de las entidades del sector social.', 'srv-h') + f'''      <div class="tx-cards">
{tx_cards}      </div>
    </div>
  </section>

  <section class="pad" id="tercer-sector" aria-labelledby="ts-h" style="padding-top:0">
    <div class="wrap split">
      <div class="prose">
        <span class="kicker">Gestión del Tercer Sector</span>
        <h2 class="h2" id="ts-h" data-lines><span class="line"><span>Asesoría y</span></span><span class="line"><span><em>gestión.</em></span></span></h2>
        <p class="big" data-reveal>Acompañamos a entidades sociales en su transformación digital y organizativa.</p>
        <p data-reveal>Las entidades sociales hacen un trabajo imprescindible, pero muchas no tienen tiempo ni recursos para modernizarse. Les ofrecemos asesoría cercana y práctica.</p>
        <ul class="ticks" data-reveal><li>Diagnóstico digital de la entidad</li><li>Asesoría en gestión, calidad y protección de datos</li><li>SAAD: asesoría digital gratuita para entidades</li><li>Formación para equipos y juntas directivas</li></ul>
        <div data-reveal>{portal_link(GTS['domain'], GTS['url'])}</div>
      </div>
      <div class="split-media" data-clip><img src="img/news-tercer-sector.jpg" alt="Dos personas revisando código en un portátil" loading="lazy"></div>
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
        <div data-reveal>{portal_link(DONG['domain'], DONG['url'])}</div>
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
''' + area_projects('tercer') + '''
  <section class="pad tx-cta" id="empieza" aria-labelledby="go-h">
    <div class="wrap">
      <span class="kicker">¡Empieza ya!</span>
      <h2 id="go-h" data-lines><span class="line"><span>Modernizar el sector,</span></span><span class="line"><span><em>innovar</em> para mejorar.</span></span></h2>
      <div class="cta-grid">
        <p data-reveal>Cuéntanos en qué punto está tu entidad y diseñamos juntos el siguiente paso.</p>
        <div data-reveal style="--d:.1s;display:flex;gap:10px;flex-wrap:wrap">
          <a class="btn btn-tec magnetic" href="escribenos.html">Hablemos de tu entidad <span class="arr">→</span></a>
          <a class="btn btn-ghost magnetic" href="''' + GTS['url'] + '''" target="_blank" rel="noopener">Visitar gestiontercersector.org <span class="arr">↗</span></a>
        </div>
      </div>
    </div>
  </section>
''' + siblings('Qué hacemos', SIB_AREAS, 'transformacion-digital.html')
write('transformacion-digital.html', 'Transformación digital y Gestión del Tercer Sector · fundación conecta+',
      'Asesoría, formación y consultoría digital para entidades del tercer sector: gestión, DigitalizaciONG, DigComp 2.0, software a medida y desarrollo web.',
      tx, parent='que-hacemos.html', extra_head=TX_HEAD)

# ================================================================== PORTADA: menú y pie compartidos
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
