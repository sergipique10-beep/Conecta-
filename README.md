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
nosotros.html  equipo.html    Páginas internas GENERADAS por tools/build_pages.py
mision.html    transformacion-digital.html
proyectos.html recursos.html  contacto.html
css/site.css                  Todos los estilos (un solo archivo, por secciones)
js/site.js                    Todo el comportamiento (un solo archivo, por módulos)
tools/build_pages.py          Generador de páginas internas + menú/pie compartidos
img/                          Imágenes (img/equipo/ = fotos del equipo)
video/                        Vídeos de las cabeceras de Misión y Proyectos (+ fotograma .jpg)
planeta.html, js/planet*.js,  Escena 3D antigua del planeta. NO está enlazada en la web
js/earth-webgpu.js            ni la usa ninguna página; se conserva por si se recupera.
```

### Mapa de páginas

| Página | Contenido |
|---|---|
| `index.html` | Portada: cabecera «Nadie fuera», manifiesto, cifras, qué hacemos, actualidad, colectivos (órbita), internacional (globo), newsletter |
| `nosotros.html` | Quiénes somos, cifras, historia, valores, equipos, colaboraciones |
| `equipo.html` | Subpágina de Nosotros: patronato y equipo (fichas con foto), trabaja con nosotros |
| `mision.html` | Las 7 líneas de trabajo. Cabecera con *showreel* de vídeo |
| `transformacion-digital.html` | Subpágina de Misión (equipo de tecnología): servicios, DigComp 2.0, DigitalizaciONG |
| `proyectos.html` | Proyectos nacionales (con filtros) e internacionales (mapa de proyectos). Cabecera con vídeo |
| `recursos.html` | Blog/noticias, publicaciones, transparencia, Campus Virtual |
| `contacto.html` | Formulario, formas de participar, sedes, preguntas frecuentes |

---

## 3. Cómo se editan las páginas (¡importante!)

El menú (NAV) y el pie (FOOTER) son iguales en las 8 páginas. Para no copiarlos a mano, se generan con un script:

```bash
python tools/build_pages.py
```

Ese script:

1. **Reescribe por completo** las páginas internas (`nosotros`, `mision`, `proyectos`, `recursos`, `contacto`, `equipo`, `transformacion-digital`) a partir de las plantillas que contiene.
2. **Sustituye solo el NAV y el FOOTER** dentro de `index.html`. El resto de la portada se respeta.

Por tanto:

| Quiero cambiar… | Dónde se edita |
|---|---|
| El menú o el pie de página | `NAV` / `FOOTER` en `tools/build_pages.py` → ejecutar el script |
| Contenido de una página interna | Su bloque en `tools/build_pages.py` → ejecutar el script |
| Contenido de la portada | Directamente en `index.html` |
| Estilos | `css/site.css` |
| Comportamiento / animaciones | `js/site.js` |

> ⚠️ Si editas a mano `nosotros.html`, `mision.html`, etc., **el próximo que ejecute el script borrará tus cambios**. Edita siempre en `tools/build_pages.py`.

Al ejecutar el script en Windows, git puede marcar como modificadas páginas que en realidad solo difieren en los saltos de línea (LF/CRLF). Comprueba los cambios reales con `git diff --ignore-cr-at-eol` y descarta los que no tengan contenido.

---

## 4. Sistema de diseño

### Colores (tokens en `:root` de `css/site.css`)

| Token | Valor | Uso |
|---|---|---|
| `--bg` | `#0B1510` | Fondo general (verde casi negro) |
| `--forest` | `#16281C` | Verde bosque (texto sobre lima, fondos) |
| `--tec` | `#C4F21D` | **Lima de marca**: acentos, lo «conectado» |
| `--mag` / `--mag-solid` | `#E24BC4` / `#CE0BA5` | **Magenta de marca**: movimiento, segundo acento |
| `--cream` | `#EFF2E8` | Bloques claros (newsletter, CTA) |
| `--ink` / `--ink-soft` / `--ink-dim` | blanco roto en 3 intensidades | Texto |

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
| *Showreel* de vídeo de las líneas | Cabecera de Misión | `Misión: showreel` |
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

Las escenas del *showreel* se definen en la lista `REEL` de `tools/build_pages.py`.

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
- [ ] **Páginas legales**: aviso legal, privacidad, cookies, accesibilidad y canal ético apuntan a `#`.
- [ ] **Documentos**: memoria anual, guías, estatutos, cuentas… (enlaces `#` en Recursos).
- [ ] **Campus Virtual**: falta la URL.
- [ ] **Formularios**: conectar newsletter y contacto a un servicio real (con doble confirmación, por RGPD).
- [ ] **Sedes**: faltan las direcciones de Madrid, Andalucía y Galicia.
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
