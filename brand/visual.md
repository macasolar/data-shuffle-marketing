# Identidad visual

Los valores salen del sitio, que es la marca real. Si algo cambia allí, cambia
aquí.

Fuente: `website-data-shuffle/src/styles/global.css` y
`website-data-shuffle/brand/README.md`.
Última confirmación: 2026-10-30.

## Colores

| Uso | Hex |
|---|---|
| Fondo | `#0b0e14` |
| Superficie, tarjetas | `#131826` |
| Bordes | `#262e42` |
| Texto | `#f3f5f9` |
| Texto secundario | `#99a0b2` |
| Acento | `#e8503a` |

La marca es **oscura**. No se hacen piezas de fondo blanco: el sitio es oscuro
y una pieza clara no se reconoce como de la misma empresa.

El acento naranja es para una cosa por pieza. Si todo está en naranja, nada
resalta.

## Tipografía

- Títulos: **Space Grotesk** 600 o 700
- Texto: **Inter** 400 o 500
- Datos, código, cifras: **JetBrains Mono** 400 o 500

Los archivos están en `brand/fonts/`, copiados de
`website-data-shuffle/public/fonts/`. Son los mismos que sirve el sitio, y por
eso las piezas salen con la tipografía real y no con una parecida.

## Logo

Una retícula de puntos con tres en naranja. El SVG está en
`brand/templates/_logo.svg`, copiado del sitio.

Dos versiones del mismo dibujo, según el fondo:
- sobre fondo oscuro, los puntos grises van en `#f3f5f9` con opacidad 0.4 y 0.28
- los tres puntos de acento siempre `#e8503a`

**No se redibuja ni se regenera con un modelo de imagen.** Es la razón por la
que todo esto se renderiza desde HTML, y está explicada en el README de marca
del sitio: un modelo no reproduce el logo exacto ni escribe "data-shuffle" sin
deformarlo.

## Medidas por red

| Pieza | Medida | Nota |
|---|---|---|
| LinkedIn, imagen de post | 1200x627 | |
| Instagram y Facebook, post | 1080x1350 (4:5) | la cuadrícula del perfil recorta a 3:4, unos 34 px por lado |
| Instagram, carrusel | 1080x1350 por slide | |
| Perfil de Empresa en Google | 1200x900 (4:3) | |
| Reel vertical | 1080x1920 | se hace en Canva, ver `canva-templates.md` |

**Margen interno de 88 px** en las piezas de Instagram, por el recorte de la
cuadrícula. Todo lo legible queda muy dentro.

## Reglas de diseño

- Una idea por pieza. Título de 8 palabras como techo, legible en el celular.
- Mucho espacio vacío. El fondo oscuro necesita aire o se ve denso.
- El logo siempre, sin deformar, en una esquina o en la cabecera.
- Ilustración antes que foto de banco de imágenes. No hay fotos propias todavía
  (`facts/cases.md`), y una foto de stock de gente en una oficina se reconoce
  al instante.
- Las ilustraciones de las cuatro páginas de servicio del sitio
  (`website-data-shuffle/src/assets/servicio-*.png`) y las imágenes de los
  artículos se pueden reutilizar en las piezas de redes. Ya son de la marca.

## Dos cosas que costaron un intento en el sitio, por si se repiten

1. **La etiqueta `viewport` es obligatoria** en cada plantilla HTML. Sin ella,
   al emular un ancho menor a 768 px el navegador maqueta a 980 px y escala
   todo.
2. **`flex-shrink` parte el texto.** Donde haya una fila de etiquetas, hace
   falta `white-space: nowrap` y `flex-shrink: 0`.
