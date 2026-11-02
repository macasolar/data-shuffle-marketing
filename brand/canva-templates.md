# Plantillas de Canva, solo para video

Las imágenes fijas no pasan por Canva: se renderizan desde HTML
(`brand/templates/`). Canva está aquí para lo que el HTML no puede hacer, que
es video.

## Antes de nada

> ⚠️ POR CONFIRMAR: estas plantillas **no existen todavía**. Hay que crearlas
> una vez (abajo cómo) y pegar su ID en la tabla. Mientras la columna "Canva
> ID" esté vacía, las piezas de formato `reel` se quedan en `idea` y el resumen
> de la corrida lo dice.

El autofill de Brand Templates requiere **Canva Pro**.

## Cómo crearlas, una sola vez

1. En Canva, armar el **Brand Kit "Data-Shuffle"**: los colores de
   `brand/visual.md`, las tipografías Space Grotesk e Inter, y el logo desde
   `brand/templates/_logo.svg`.
2. Crear el diseño en el tamaño de la tabla, con fondo `#0b0e14`.
3. Publicarlo como **Brand Template**.
4. Conectar cada texto a un campo de datos (autofill) con el nombre exacto de
   la lista de campos.
5. Nombrarlo **`Data-Shuffle - <clave> - v1`**. Si se rediseña, `v2`, y se
   actualiza aquí.
6. Copiar el ID desde la URL de Canva a la columna de abajo.

## Plantillas

| Clave (`plantilla`) | Nombre en Canva | Canva ID | Tamaño | Uso |
|---|---|---|---|---|
| `reel-explicacion` | Data-Shuffle - reel-explicacion - v1 | | 1080x1920 | 3 escenas de texto sobre fondo oscuro, tarjeta final con logo |
| `reel-caso` | Data-Shuffle - reel-caso - v1 | | 1080x1920 | Problema, qué se hizo, resultado, tarjeta final |

## Campos de autofill

### reel-explicacion
- `escena1_texto`: el gancho, máximo 8 palabras
- `escena2_texto`: máximo 14 palabras
- `escena3_texto`: máximo 14 palabras
- `cta_final`: la tarjeta de cierre, máximo 6 palabras

### reel-caso
- `sector`: el sector del caso, nunca el nombre del cliente salvo permiso en
  `facts/cases.md`
- `problema`: máximo 12 palabras
- `solucion`: máximo 14 palabras
- `resultado`: máximo 12 palabras, y solo con un dato que esté en `facts/`
- `cta_final`: máximo 6 palabras

## Lo que no se hace en Canva

- **Imágenes fijas.** Para eso están las plantillas HTML, que usan el logo y
  las tipografías reales.
- **Video con gente de banco de imágenes.** No hay material propio todavía
  (`facts/cases.md`), y un video de stock de una oficina se reconoce al
  instante. Mientras no haya material, los reels son texto en movimiento sobre
  el fondo de la marca.
