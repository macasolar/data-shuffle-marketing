# Cadencia y fase

```yaml
phase: 1
auto_approve_evergreen: false
```

Solo José cambia estos valores. Ver `docs/ROLLOUT.md`.

## Por semana

| Red (`redes`) | Qué | Cantidad |
|---|---|---|
| `linkedin` | El argumento de un artículo, una pregunta frecuente, un caso | 3 |
| `instagram` + `facebook` | Post de síntoma o carrusel explicativo (cross-post) | 2 |
| `gbp` | Un servicio con la zona y el CTA | 1 |

Seis piezas únicas por semana. LinkedIn lleva el peso porque es donde está
quien compra esto, y porque es lo que dice `src/social.config.ts` del sitio.

**TikTok no está y no se va a crear.** Instagram y Facebook se publican con el
mismo contenido, que es el único caso donde se permite repetir texto, y aun así
conviene adaptar el primer renglón.

## El artículo del sitio

Techo de **uno por semana**, piso de **dos al mes**, y nunca dos el mismo día.
No es una preferencia, es la regla de `claude/post/distribucion.md` del sitio,
con su razón: una descarga de artículos de golpe es justo la señal de
"contenido a escala sin que nadie lo revise" que Google sí persigue.

Cuando sale un artículo, tres de las seis piezas de esa semana salen de él
(LinkedIn el mismo día, Instagram y Facebook con la idea central).

## Horarios

Por defecto, la mejor hora que sugiera Metricool para esa red y ese día. Si no
hay dato:

- LinkedIn: 8:00, de martes a jueves
- Instagram y Facebook: 12:00 o 18:00
- Perfil de Empresa en Google: lunes 10:00

Hora de Panamá (UTC-5).

## Días sugeridos

- Lunes: Perfil de Empresa en Google, y LinkedIn si hay artículo nuevo
- Martes: LinkedIn
- Miércoles: Instagram y Facebook
- Jueves: LinkedIn
- Viernes: Instagram y Facebook

## Lo que corre solo

Lo decide `docs/ROLLOUT.md` según la fase. En Fase 3, los lunes:

1. `ds run post` escribe el borrador del artículo de la semana y deja una rama
   empujada en el repo del sitio.
2. `ds run week` escribe y renderiza las seis piezas.
3. `ds run publish` las manda a la cola de revisión de Metricool.

José aprueba en Metricool desde el teléfono, y mezcla la rama del artículo
cuando lo haya leído.
