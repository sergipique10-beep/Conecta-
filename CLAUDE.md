# CLAUDE.md

Instrucciones para Claude Code en este repositorio. El contexto completo está en [README.md](README.md): léelo antes de cambios grandes.

## Proyecto

Web estática de fundación conecta+ (HTML + CSS + JS, sin framework ni build). Cada push a `main` se publica automáticamente en Render.

## Reglas

- **Idioma:** contenido, comentarios de código y mensajes de commit en español.
- **Páginas internas generadas:** `nosotros`, `mision`, `proyectos`, `recursos`, `contacto`, `equipo` y `transformacion-digital` (.html) se generan con `python tools/build_pages.py`. Edita su contenido en ese script y vuelve a ejecutarlo; **nunca edites esos .html a mano** (se sobrescriben).
- **Menú y pie compartidos:** el NAV y el FOOTER están en `tools/build_pages.py` y el script los copia también en `index.html`. El resto de `index.html` se edita a mano.
- **Estilos y comportamiento:** todos los estilos en `css/site.css` y todo el JS en `js/site.js`. Añade lo nuevo como bloque comentado con el formato existente (`/* ---------- nombre ---------- */`).
- **Ámbito compartido en `js/site.js`:** todo el archivo es una sola función, así que las `var` de todos los módulos comparten ámbito. Usa nombres con prefijo propio en módulos nuevos y comprueba que no choquen con los existentes; esto ya causó errores silenciosos.
- **Saltos de línea:** tras regenerar, git puede marcar páginas cambiadas solo por LF/CRLF. Compruébalo con `git diff --ignore-cr-at-eol` y descarta (`git checkout -- archivo`) las que no tengan cambios reales.
- **Vídeo:** al recodificar, conserva los fps originales (`-fps_mode passthrough`). No pongas `filter`, `mix-blend-mode` ni `backdrop-filter` sobre vídeos; el color se hornea con ffmpeg (ver la receta en el README).
- **Accesibilidad y movimiento:** toda animación nueva debe respetar `reduce` (prefers-reduced-motion) y no bloquear el uso con teclado.
- **Contenido provisional:** nombres y fotos del equipo, enlaces `#` y formularios sin backend son de relleno (lista en README §8). No los presentes como reales ni inventes datos de la fundación: si falta información, pregunta.

## Verificar cambios

- Revisa las páginas afectadas en escritorio (1440×900) y móvil (390×844), sin errores de consola.
- Las anclas internas deben aterrizar justo bajo el menú (`scrollToTarget`).
- No hagas commit ni push sin que el usuario lo pida: publicar en `main` sale directamente a producción.
