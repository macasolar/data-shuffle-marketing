# Plantillas de imagen

Se renderizan con Chrome sin ventana, no con Canva y no con un modelo de
imagen. El motivo está en `brand/visual.md` y, más largo, en el README de marca
del sitio: así la pieza sale con el logo exacto y las tipografías reales.

    ds render <plantilla> <datos.json> <salida.png>

Ejemplo:

    ds render instagram content/2026-11/data/2026-11-03-ig.json output/2026-11-03-ig.png

`ds/render.py` sustituye cada `{{campo}}` del HTML por su valor del JSON,
sirve la carpeta por HTTP (las tipografías no cargan por `file://`) y captura
el tamaño exacto de la plantilla.

## Campos y límites

Los límites no son decorativos: la plantilla tiene alto fijo, así que un texto
más largo se sale del lienzo y la captura queda cortada. `ds check`
verifica cada pieza contra esta tabla y falla si algo se pasa.

| Plantilla | Medida | Campos | Límite |
|---|---|---|---|
| `linkedin` | 1200x627 | `kicker`, `titulo`, `cuerpo`, `cta` | 5 / 12 / 22 / 7 palabras |
| `instagram` | 1080x1350 | `kicker`, `titulo`, `cuerpo`, `cta` | 5 / 10 / 28 / 7 palabras |
| `instagram-carousel` | 1080x1350 | `slide`, `total`, `titulo`, `cuerpo`, `cta` | - / - / 9 / 30 / 7 palabras |
| `google` | 1200x900 | `kicker`, `titulo`, `cuerpo`, `cta` | 5 / 10 / 26 / 7 palabras |

## Dos detalles de escritura

**Una palabra en naranja.** En `titulo` se puede envolver una palabra o frase
corta en `<b>`, y sale en el color de acento sin ponerse más negrita. Una por
pieza: si todo está en naranja, nada resalta.

**El `kicker` es la categoría, no el título.** "Datos y analítica", "Caso real",
"Facturación electrónica". Va en mayúsculas y en monoespaciada, como las
etiquetas del sitio.

## Un carrusel

Se renderiza una vez por slide, cambiando `slide` y los textos, con el mismo
`total`. Cinco slides es lo habitual: gancho, tres pasos y cierre con CTA.
