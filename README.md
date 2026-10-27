# fundación conecta+ · web

Web estática de **fundación conecta+**, entidad sin ánimo de lucro de educación, inclusión digital y acción social (desde 1995; sedes en Cataluña, Madrid, Andalucía y Galicia).

- **Tecnología:** HTML + CSS + JavaScript sin framework ni paso de compilación.
- **Publicación:** cada push a `main` se despliega automáticamente en **Render**.
- **Idioma:** todo el contenido, los comentarios del código y los mensajes de commit van en **español**.

---

## 1. Ver la web en local

No hace falta instalar nada. Hay dos opciones:

- Abrir `index.html` directamente en el navegador.
- O, mejor, servirla para que funcionen las rutas y los vídeos igual que en producción:

  ```bash
  python -m http.server 8000
  # y abrir http://localhost:8000
  ```

Algunas piezas cargan recursos externos (ver [§7](#7-dependencias-externas)), así que necesitan conexión a internet.

---

## 2. Estructura del proyecto

```
index.html                    Portada (se edita a mano, salvo menú y pie)
*.html (resto)                Todas las demás páginas: GENERADAS por tools/build_pages.py
css/site.css                  Todos los estilos (un solo archivo, por secciones)
js/site.js                    Todo el comportamiento (un solo archivo, por módulos)
tools/build_pages.py          Generador de páginas + menú/pie compartidos + listas de datos
img/                          Imágenes (img/equipo/ = fotos del equipo)
video/                        Vídeos de las cabeceras de Qué hacemos y Proyectos (+ fotograma .jpg)
planeta.html, js/planet*.js,  Escena 3D antigua del planeta. NO está enlazada en la web
js/earth-webgpu.js            ni la usa ninguna página; se conserva por si se recupera.
```

### Mapa de páginas

La navegación sigue el wireframe: cada sección del menú es una página **hub** con tarjetas a sus subpáginas. Las subpáginas llevan un botón «← Volver a …» y un bloque «Sigue explorando» con sus páginas hermanas; las páginas de detalle tienen «anterior / siguiente».

| Hub | Subpáginas |
|---|---|
| `nosotros.html` | `quienes-somos`, `equipo`, `historia`, `ecosistema` (tarjetas que enlazan a los 9 portales externos) |
| `que-hacemos.html` (cabecera con *showreel*) | `formacion-tic`, `observatorio`, `voluntariado`, `jovenes`, `inclusion-digital`, `transformacion-digital` |
| `proyectos.html` (cabecera con vídeo) | `proyectos-nacionales` (filtros por área) y `proyectos-internacionales` (mapa) → `proyecto-*.html` |
| `recursos.html` | `blog` → `noticia-*.html`, `publicaciones` → `publicacion-*.html`, `transparencia`, `preguntas-frecuentes`, `campus` |
| `contacto.html` | `escribenos`, `sedes` |
| `colabora.html` (botón de la cabecera) | `hazte-voluntario`, `dona`, `unete` |
| Pie | `boletin`, `canal-denuncia`, `aviso-legal` (con `#privacidad`, `#cookies`, `#accesibilidad`) |

- `mision.html` ya no existe como página: es una redirección a `que-hacemos.html` para no romper enlaces antiguos.
- Las áreas enlazan a sus proyectos con `proyectos-nacionales.html?area=<categoría>`, que deja ese filtro activo.
- Proyectos, noticias y publicaciones salen de las listas `PROJ_NAC`, `PROJ_INT`, `NEWS` y `PUBS` de `tools/build_pages.py`: añadir un elemento a la lista crea su página y la enlaza.
- Los portales salen de la lista `ECO`: cada elemento es una tarjeta de `ecosistema.html` que enlaza directamente al portal externo (sin página propia).
- El **buscador** de la cabecera es solo la interfaz (panel con campo y accesos rápidos); todavía no busca.
- Los bloques marcados como **«Provisional»** (borde magenta discontinuo) señalan contenido que falta.

## 3. Cómo se editan las páginas (¡importante!)

El menú (NAV, con el panel del buscador) y el pie (FOOTER) son iguales en todas las páginas. Para no copiarlos a mano, se generan con un script:

```bash
python tools/build_pages.py
```

Ese script:

1. **Reescribe por completo** todas las páginas salvo la portada, a partir de las plantillas y listas de datos que contiene.
2. **Sustituye solo el NAV y el FOOTER** dentro de `index.html`. El resto de la portada se respeta.

Por tanto:

| Quiero cambiar… | Dónde se edita |
|---|---|
| El menú o el pie de página | `NAV` / `FOOTER` en `tools/build_pages.py` → ejecutar el script |
| Contenido de una página interna | Su bloque en `tools/build_pages.py` → ejecutar el script |
| Contenido de la portada | Directamente en `index.html` |
| Estilos | `css/site.css` |
| Comportamiento / animaciones | `js/site.js` |

> ⚠️ Si editas a mano cualquier página que no sea `index.html`, **el próximo que ejecute el script borrará tus cambios**. Edita siempre en `tools/build_pages.py`.

Al ejecutar el script en Windows, git puede marcar como modificadas páginas que en realidad solo difieren en los saltos de línea (LF/CRLF). Comprueba los cambios reales con `git diff --ignore-cr-at-eol` y descarta los que no tengan contenido.

---

## 4. Sistema de diseño

### Colores y paletas (selector «Modo»)

La web tiene **6 paletas** que se eligen con el botón **Modo** de la cabecera (entre el buscador y «Colabora»):

| id | Nombre | Tipo |
|---|---|---|
| `bosque` | Bosque (la original, por defecto) | oscura |
| `verde` | Verde marca | oscura |
| `noche` | Noche magenta | oscura |
| `papel` | Papel | clara |
| `lima` | Lima | clara |
| `magenta` | Magenta suave | clara |

Cómo funciona:

- **CSS** (`css/site.css`, bloque «paletas» al principio): cada paleta define sus colores base en `:root[data-paleta="…"]`. Los colores derivados (`--ink-soft`, `--ink-dim`, `--line`) se calculan con `color-mix`. En el resto del archivo no hay colores escritos a mano: todo usa tokens.
- **Tokens principales:** `--bg`, `--bg-2`, `--surface` (fondos) · `--ink` (texto) · `--tec` y `--on-tec` (relleno de acento y texto encima) · `--tec-text` (acento usado como texto) · `--mag-solid` / `--mag` (segundo acento) · `--cta-*` (bloque de newsletter) · `--foot-bg` / `--foot-accent` (pie) · `--logo-*` y `--sym-*` (logotipo y símbolo) · `--net-1` / `--net-2` (animaciones en canvas). La lista completa está comentada en el CSS.
- **Zonas siempre oscuras:** el pie, las tarjetas sobre foto (`.value`) y el terminal (`.tx-term`) redefinen los tokens para verse oscuros en todas las paletas.
- **`<head>`:** un script mínimo aplica la paleta guardada antes de pintar (sin parpadeo). Se puede forzar una paleta con `?paleta=lima` en la URL (útil para enviar un enlace a una variante concreta).
- **`js/site.js`:** el módulo «selector Modo» construye el desplegable y emite el evento `conecta:paleta` al cambiar; las animaciones en canvas lo escuchan y releen sus colores con `cpRGB()`.

**Dejar solo dos paletas** (cuando se elija la versión definitiva): en `js/site.js`, cambia `cpmVisibles` por los dos ids elegidos (por ejemplo `['verde','papel']`). Si la paleta por defecto deja de ser Bosque, cambia también el valor de reserva `'bosque'` del script del `<head>` en `tools/build_pages.py` e `index.html` y regenera las páginas.

### Tipografías (Google Fonts)

- **Archivo** (variable, con ancho condensado): titulares y texto.
- **Instrument Serif** en cursiva: palabras destacadas dentro de los titulares (`<em>`).
- **Fredoka**: solo el logotipo «conecta+».
- **JetBrains Mono**: solo en Transformación digital (estética técnica).

### Patrones de titular

```html
<h2 class="h2" data-lines>
  <span class="line"><span>Texto normal</span></span>
  <span class="line"><span><em>palabra en cursiva lima.</em></span></span>
</h2>
```

### Animaciones de entrada (atributos)

- `data-reveal`: aparece subiendo al entrar en pantalla. Se puede retrasar con `style="--d:.1s"`.
- `data-lines`: las líneas del titular suben una a una.
- `data-clip`: la imagen se revela con un recorte.

Todo respeta `prefers-reduced-motion`: con movimiento reducido no hay animaciones.

---

## 5. El concepto: «La red que te acompaña»

La web cuenta visualmente el valor de la fundación, **que nadie quede fuera**: el lima es lo conectado, el gris lo que queda fuera y el magenta el movimiento.

| Pieza | Dónde | Módulo en `js/site.js` |
|---|---|---|
| Símbolo de partículas + puntos grises que se conectan con el cursor | Cabecera de la portada | `hero «Nadie fuera»` |
| Hilo conductor (progreso + índice de secciones a la izquierda) | Todas las páginas, en escritorio | `hilo conductor` |
| Órbita de colectivos | Portada, en escritorio (en móvil: tarjetas) | `colectivos: «órbita de personas»` |
| Globo 3D de puntos con arcos | Portada → Internacional | `internacional: «el mundo conectado»` |
| Mapa plano de proyectos | Proyectos → Internacionales | `proyectos internacionales: mapa de proyectos` |
| *Showreel* de vídeo de las líneas | Cabecera de Qué hacemos | `Qué hacemos: showreel` |
| Ciudad nocturna + arcos | Cabecera de Proyectos | `Proyectos: arcos de luz sobre la ciudad` |
| La red que crece al enviar un formulario | Newsletter de la portada, Contacto | `la red que crece` |
| Red de nodos + terminal | Transformación digital | `transformación digital: …` |

Además, en todas las páginas: scroll suave (Lenis), cursor personalizado, transición de cortina entre páginas, footer a pantalla completa, panel de cookies y barra de acceso rápido en móvil.

---

## 6. Notas técnicas de `js/site.js`

- Todo el archivo es **una sola función autoejecutable**. Cada módulo empieza con un comentario `/* ---------- nombre ---------- */` y solo se activa si existe su elemento en la página (`if(elemento){ … }`).
- ⚠️ **Las variables `var` de todos los módulos comparten ámbito.** Dos módulos con una variable del mismo nombre se pisan (ya causó dos errores difíciles de ver). En módulos nuevos usa nombres con prefijo propio (`rCur`, `fDots`, `hT0`…) o envuelve el módulo en su propia función.
- Utilidades disponibles: `$(id)`, `clamp`, `lerp`, `docTop`, `scrollToTarget(el)` y las banderas `reduce` (movimiento reducido) y `fine` (ratón).
- Los enlaces internos con `#ancla` aterrizan en el inicio real de la sección, justo bajo el menú. No uses `scrollIntoView`: usa `scrollToTarget`.
- **Formularios:** no tienen backend. Validan, muestran el estado de envío y la confirmación, y emiten el evento `cm:ok`. Para conectarlos a un servicio real (Mailchimp, Brevo…), sustituye el `setTimeout` del módulo `formularios`.
- **Cookies:** el panel está listo pero no se abre solo, porque la web aún no usa analítica. Cuando se añada, cambia `COOKIE_AUTO = true` y carga la analítica solo si `localStorage['cm-cookies']` lo permite.

### Rendimiento de vídeo (lecciones aprendidas)

- **Respeta los fps originales** del clip al recodificar. Forzar 30 fps en un vídeo de 24 o 25 fps produce tirones visibles.
- **No pongas filtros CSS, `mix-blend-mode` ni `backdrop-filter` encima de un vídeo**: se recalculan en cada fotograma. El color de marca se «hornea» en el propio vídeo con ffmpeg.

Receta para añadir o recodificar un clip:

```bash
# Showreel de Misión (ajuste de color ligero, sin audio, fps nativos)
ffmpeg -ss 1 -t 6 -i original.mp4 -an -fps_mode passthrough \
  -vf "scale=960:-2:flags=lanczos,eq=contrast=1.05:saturation=0.9" \
  -c:v libx264 -preset slow -crf 27 -g 48 -pix_fmt yuv420p -movflags +faststart video/nombre.mp4
ffmpeg -ss 1 -i original.mp4 -frames:v 1 -vf "scale=1280:-2" -q:v 4 video/nombre.jpg
```

Las escenas del *showreel* de Qué hacemos se definen en la lista `REEL` de `tools/build_pages.py`.

---

## 7. Dependencias externas

| Recurso | Origen | Para qué |
|---|---|---|
| Fuentes | Google Fonts | Tipografías |
| Lenis 1.1.13 | unpkg | Scroll suave (si falla, la web funciona con scroll normal) |
| topojson-client + world-atlas (land-110m) | jsDelivr | Continentes del globo y del mapa. Si fallan, se muestra la constelación plana o solo las tarjetas |
| Vídeos de las cabeceras | [Mixkit](https://mixkit.co) | Licencia libre, sin marca de agua |
| Fotos de publicaciones y fondo del footer | Unsplash vía picsum.photos | Licencia libre |
| Fotos del equipo | i.pravatar.cc | **Solo de relleno** (ver §8) |

---

## 8. Contenido provisional que hay que sustituir antes del lanzamiento

- [ ] **Equipo y patronato** (`equipo.html`): los **nombres son ficticios** y las **fotos son de banco de imágenes** (personas reales ajenas a la fundación). Hay que sustituirlos cuanto antes, porque la web ya es pública. Las fotos van en `img/equipo/persona-XX.jpg` y los nombres, cargos y textos en la lista `patronato` / `equipo` de `tools/build_pages.py`.
- [ ] **Documentos**: memoria anual, guías, estatutos, cuentas… (enlaces `#` en Recursos).
- [ ] **Campus Virtual**: falta la URL (el formulario de `campus.html` no redirige).
- [ ] **Buscador**: solo interfaz; falta el índice y los resultados.
- [ ] **Detalles de proyectos, noticias y publicaciones**: faltan textos completos, fechas, financiadores y archivos (bloques «Provisional»).
- [ ] **Donaciones**: `dona.html` no tiene pasarela de pago.
- [ ] **Canal de denuncia**: falta la URL del formulario externo.
- [ ] **Textos legales**: `aviso-legal.html` tiene secciones de relleno.
- [ ] **Formularios**: conectar newsletter y contacto a un servicio real (con doble confirmación, por RGPD).
- [ ] **Sedes** (`sedes.html`): faltan las direcciones de Madrid, Andalucía y Galicia.
- [ ] **Horario de atención**: para mostrarlo junto al reloj del footer.
- [ ] **Logos de financiadores** (si hay fondos públicos o europeos, suele ser obligatorio mostrarlos).
- [ ] **Redes sociales**: los iconos del footer apuntan a `#`.
- [ ] **Años de experiencia**: la web dice «desde 1995» (+30 años) y Transformación digital, «más de 20 años». Confirmar la cifra.
- [ ] **Textos de ejemplo**: las descripciones de colectivos, valores, proyectos y FAQ se redactaron a partir del contenido existente. Conviene revisarlas.

---

## 9. Flujo de trabajo con git

- Se trabaja sobre `main`. **Cada push a `main` publica la web en Render**, así que sube solo lo que esté revisado.
- Antes de hacer push, `git pull --rebase` por si un compañero ha subido cambios.
- Mensajes de commit en español, con prefijo: `feat:` (novedad), `fix:` (arreglo), `docs:` (documentación).
- Tras publicar, recarga con **Ctrl + F5**. Los navegadores guardan en caché `site.css` y `site.js`.
