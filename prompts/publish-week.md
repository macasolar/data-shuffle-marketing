# Publicar la semana

Mandas a Metricool las piezas aprobadas, a su cola de revisión, y guardas el id
que devuelve.

Esta corrida **toca el exterior**. Sé exacto y registra todo. Sigue `CLAUDE.md`.

## Qué piezas entran

1. Lee `strategy/cadence.md` para la fase y `auto_approve_evergreen`.
2. Candidatas: archivos en `content/*/` con `fecha_publicacion` en el futuro y:
   - `estado: approved`, o
   - `estado: draft` **y** `auto_approve_evergreen: true` **y** sin tags
     `legal` ni `price` **y** la pieza es evergreen (ver `strategy/pillars.md`).
3. **Nunca** una pieza con tag `legal` o `price` que no esté `approved`. Nunca
   una en `idea`, `rejected` o `review`. Nunca una sin su imagen cuando la red
   la exige (Instagram siempre).
4. Vuelve a comprobar la frescura de los hechos (regla 3 de `CLAUDE.md`). Si un
   hecho se pasó de fecha desde que José aprobó, salta la pieza y dilo.
5. Para las piezas de origen `post`, comprueba otra vez que el artículo está
   publicado y que la URL responde. Un enlace a un 404 es peor que no publicar.

## Cómo se manda

1. Mira `getBrandSettings` para confirmar qué marca y qué redes están
   conectadas en Metricool. Si una red de la pieza no está conectada, salta esa
   red y dilo.
2. Por cada pieza y cada red de `redes`, crea la publicación **con
   `createScheduledPostForReview`**, no con `createScheduledPost`. Así entra en
   la cola de revisión de Metricool y José aprueba desde el teléfono, que es la
   última puerta antes de que salga.
3. Texto: el de la sección de esa red, no el de otra. Adjunta la imagen de
   `imagen` (o el MP4 del reel).
4. Hora: la de `fecha_publicacion`, hora de Panamá (UTC-5). Si las notas de la
   pieza dicen "mejor hora", pide la de `getBestTimeToPostByNetwork` para esa
   red y ese día, o pídesela al subagente `metricool-lookup`.
5. Durante el piloto y la fase 1, **programa con 3 días de anticipación como
   mínimo**, para que José pueda cancelar.
6. Si adjuntar la imagen falla, **no publiques solo el texto.** Deja la pieza
   en `approved`, dilo en el resumen y da la ruta del PNG para que José lo
   suba a mano.
7. Guarda `metricool_id` (uno por red, como lista si hace falta) y pon
   `estado: review`. Añade una línea en "Notas / feedback de José":
   `YYYY-MM-DD enviado a revisión en Metricool <ids> por publish-week`.
8. Confirma: `publish-week: N pieces sent for review`.

## Resumen para José

Tabla `fecha | red | tema | metricool_id`.

Después: las piezas que se saltaron y por qué, y el recordatorio de que están
en la cola de revisión de Metricool y que **hasta que él las apruebe ahí no se
publican**. Si alguna imagen hay que subirla a mano, su ruta.
