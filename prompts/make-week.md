# Escribir la semana

Escribes el texto y renderizas las imágenes de las piezas de los próximos 7
días, y las dejas en `estado: draft` para que José las apruebe.

Sigue `CLAUDE.md`. Español de Panamá, voz de `brand/voice.md`. Sin rayas largas.

## Entrada

Las piezas con `estado: idea` y `fecha_publicacion` dentro de los próximos 7
días (hoy incluido), en `content/*/`. Revisa los dos meses si la semana cruza
el cambio de mes.

Si no hay ninguna, no inventes un plan completo: escribe hasta 6 piezas nuevas
siguiendo `strategy/cadence.md` y `strategy/pillars.md`, dilo en el resumen, y
recomienda correr `ds run plan`.

## Lo que se lee

`facts/` (solo los archivos que cite cada pieza en `fuentes`), `brand/voice.md`,
`brand/templates/README.md` (los campos y sus límites), `strategy/audiences.md`
y, para las piezas de origen `post`, el artículo entero en
`$WEBSITE_REPO/src/content/blog/`.

## Por cada pieza

1. **Verifica los hechos.** Cada afirmación tiene que salir de una entrada de
   `facts/` sin `⚠️ POR CONFIRMAR` y fresca (precio como máximo 90 días, hecho
   legal como máximo 180 días desde `Última confirmación`). Si falla un hecho
   necesario, **deja la pieza en `idea`**, anota el motivo en "Notas / feedback
   de José" y ponla en la lista del resumen. No inventes.
2. **Si el origen es `post`, comprueba que el artículo está publicado.** Tiene
   que existir en `$WEBSITE_REPO/src/content/blog/` fuera de `draft/` y con
   `draft: false`. Un artículo que todavía está en una rama no tiene URL viva:
   la pieza se queda en `idea` y lo dices.
3. **Escribe el texto por red**, en la sección que corresponda:
   - **LinkedIn**: el argumento en 3 o 4 párrafos, un dato concreto o un caso,
     cierre con pregunta abierta o paso siguiente, de 0 a 3 hashtags. El enlace
     al artículo **al final del texto**, nunca solo y nunca al principio. Jamás
     el artículo completo.
   - **Instagram y Facebook**: primera línea de gancho que funcione sola,
     párrafos de una o dos frases, CTA a WhatsApp, de 3 a 5 hashtags. El enlace
     no se pone en el texto de Instagram (no es clicable): se dice "enlace en
     la bio" o se deja el CTA a WhatsApp. En Facebook sí va el enlace.
   - **Perfil de Empresa en Google**: un párrafo, un servicio, la zona, un CTA.
   - Nunca el mismo párrafo en dos redes.
4. **Rellena el bloque JSON "Campos de la plantilla"** con los campos exactos
   de `brand/templates/README.md` y respetando los límites de palabras. Una
   palabra del `titulo` puede ir en `<b>` para que salga en naranja.
5. **Renderiza la imagen.** Guarda el JSON en
   `content/<mes>/data/<id>.json` y corre:
   `ds render <plantilla> content/<mes>/data/<id>.json output/<id>.png`
   Para un carrusel, un JSON y un PNG por slide (`<id>-1.json`, etc.), con el
   mismo `total`.
   **Mira el PNG** después de renderizarlo. Si el texto se sale o queda
   apretado, acorta el texto, no cambies la plantilla.
   Anota las rutas en `imagen`.
6. **Si el formato es `reel`**: mira `brand/canva-templates.md`. Si la
   plantilla no tiene Canva ID, **deja la pieza en `idea`** con la nota
   "plantilla de Canva pendiente" y sigue con las demás. Si lo tiene, rellénala
   por el conector de Canva, exporta el MP4 y guarda `canva_design_id`.
7. `estado: draft`.
8. **Revisa.** Pasa todos los borradores por el subagente `post-checker`, o
   compruébalo tú: ninguna raya larga, cada número y cada nombre trazable a
   `fuentes`, los tags `legal`/`price` donde hagan falta, las reglas de voz, y
   los límites de las plantillas. `ds check` comprueba la parte mecánica.
9. Confirma: `make-week: drafts for YYYY-MM-DD to YYYY-MM-DD`.

## Resumen para José

Tabla: `fecha | red | formato | pilar | tema | imagen | estado`.

Después: qué piezas quedaron en `idea` y por qué, qué necesita su aprobación, y
cómo aprobar: cambiar `estado: draft` a `estado: approved` (o `rejected` con
una nota) y correr `ds run publish`.
