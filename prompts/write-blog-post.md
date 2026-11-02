# Escribir un artículo del sitio

Escribes un artículo para el blog de data-shuffle.com a partir de un tema, lo
dejas listo para publicar y lo empujas en una rama. **No lo publicas tú.**

## Dónde se trabaja

El repo del sitio está en la ruta de la variable `WEBSITE_REPO` (te la pasa el
runner en la entrada). Todo el trabajo del artículo pasa allí. Este repo
(`data-shuffle-marketing`) solo aporta los hechos y la decisión del tema.

## La guía manda, y no está aquí

**Lee `$WEBSITE_REPO/claude/como-se-publica-un-post.md` antes de escribir una
sola línea, siempre.** Es la fuente de verdad del formato, del frontmatter, del
orden de la página y de la lista de comprobación. No trabajes de memoria y no
asumas que lo recuerdas.

Cada fase larga es un archivo aparte, que se abre cuando el trabajo llega a
ella, no antes:

| Archivo | Para qué |
|---|---|
| `claude/post/caso-de-cliente.md` | el caso de cliente y su tarjeta |
| `claude/post/cuerpo.md` | cómo se construye el artículo y cuánto mide |
| `claude/post/imagenes.md` | imagen de cabecera, diagramas, alt, pies |
| `claude/post/seo.md` | qué está resuelto y qué es criterio |
| `claude/post/voz.md` | la pasada de voz y `check:voz` |
| `claude/post/distribucion.md` | lo que viene después de publicar |
| `claude/post/antecedentes.md` | por qué las reglas son las que son |

`$WEBSITE_REPO/src/content/blog/capturar-gastos-y-facturas-en-quickbooks.md` es
el ejemplo trabajado. Ante cualquier duda de forma, ábrelo.

Lee también `$WEBSITE_REPO/CLAUDE.md`: ahí están la regla de la raya larga, el
reparto de idiomas y las reglas de enlaces.

## Lo que este repo añade

- **Los hechos se verifican contra `facts/` de este repo**, además de contra el
  sitio. Si el artículo va a afirmar algo de la empresa (una cifra, un cliente,
  una tecnología, un plazo), tiene que estar en `facts/` sin marca
  `⚠️ POR CONFIRMAR`. Un dato que no esté, no se escribe.
- **El caso de cliente solo puede ser real si está en `facts/cases.md`** como
  real. Si no hay caso real para este tema, el artículo se escribe sin tarjeta
  de caso, o con `source: "Ejemplo ilustrativo"`, nunca marcando como real algo
  que no lo es.
- **Nadie del equipo se nombra salvo José Luis Vieyra** (`facts/company.md`).

## Orden de trabajo

1. Lee la guía. Lee el tema de la entrada.
2. **Comprueba que el tema no está ya escrito.** Mira
   `$WEBSITE_REPO/src/content/blog/` (publicados) y
   `$WEBSITE_REPO/src/content/blog/draft/` (22 borradores). Si ya existe un
   borrador de este tema, **termínalo en vez de escribir otro**, y dilo en el
   resumen. Si ya está publicado, para y dilo: el tema se replantea con otro
   ángulo o se cambia.
3. Rama nueva desde `develop`, en el repo del sitio:
   `git -C $WEBSITE_REPO switch develop && git -C $WEBSITE_REPO pull --ff-only`
   y luego `git -C $WEBSITE_REPO switch -c post/<slug>`.
   Si el árbol de trabajo tiene cambios sin confirmar, **para y dilo**. No
   guardes el trabajo de otro en un stash.
4. Escribe el artículo, abriendo cada archivo de fase cuando llegues a él.
5. Las imágenes, según `claude/post/imagenes.md`. Si no puedes producir una,
   deja `imageTodo` con el nombre del archivo que falta y dilo en el resumen.
   No publiques un artículo con una imagen cortada ni con un diagrama en la
   cabecera (el hueco de cabecera recorta a una banda de 340 px).
6. **Los enlaces.** Solo hacia fuera: el cuerpo del artículo nuevo enlaza dos
   artículos publicados, escritos dentro de este mismo archivo.
   `npm run check:enlaces` falla si faltan, y corre dentro de `validate`.
   Los enlaces hacia dentro **no los escribes tú**: los pone el sitio al
   construirse (`src/related.ts`, las tarjetas "Seguir leyendo"), que garantiza
   que cada artículo reciba al menos dos. **Prohibido editar un artículo ya
   publicado para enlazar a este**, aunque parezca que ayuda.
7. **Deja el artículo listo para publicar**: `draft: false` y el archivo fuera
   de `src/content/blog/draft/` (con `git mv` si venía de ahí). Son los dos
   pasos, y la compilación para si solo se hace uno.
8. `npm run check:voz -- <slug>` y arregla lo que marque, salvo un aviso
   justificado (`claude/post/voz.md` explica cuándo lo es).
9. `npm run validate`. **Verde antes de confirmar, siempre.** Usa el subagente
   `validate-checker` del repo del sitio si está disponible: devuelve solo los
   fallos.
10. Mira la página construida, no solo los checks. Una imagen recortada o una
    maqueta rota pasan todas las pruebas automáticas. El subagente
    `page-checker` captura una ruta a los dos anchos.
11. Confirma y empuja **la rama**:
    `git -C $WEBSITE_REPO add -A && git -C $WEBSITE_REPO commit` y
    `git -C $WEBSITE_REPO push -u origin post/<slug>`.

## Lo que no haces, en ningún caso

- **No mezclas a `master` y no despliegas.** Ahí está la puerta de José. El
  despliegue sale solo al mezclar en `master`, y sube el sitio por FTPS y avisa
  a IndexNow. Eso lo decide una persona.
- **No mezclas a `develop`** tampoco. Dejas la rama empujada y nada más.
- No tocas nada fuera del artículo nuevo y sus imágenes. Ningún artículo ya
  publicado, ni para añadirle un enlace.
- No creas piezas de redes aquí. Eso es `make-week`, y corre cuando el artículo
  ya está publicado y tiene URL viva.

## Resumen para José

- El slug, el título y el pilar.
- Si venía de un borrador existente o es nuevo.
- Qué dice el caso y si es real o ilustrativo, con su fuente.
- Las imágenes hechas y las que faltan.
- Los dos enlaces hacia fuera.
- `validate`: verde, o los fallos exactos.
- El comando para ver la rama y el comando para publicarla, de forma que José
  solo tenga que leerla y mezclar.
- Lo que no pudiste verificar.
