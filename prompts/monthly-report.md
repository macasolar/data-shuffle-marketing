# Reporte del mes

Escribes `reports/YYYY-MM.md` con los números reales del mes y propones los
cambios que esos números justifican.

Sigue `CLAUDE.md`. Español de Panamá. Sin rayas largas. **Solo números que
devuelva un conector. Una métrica que falte se escribe "sin dato", nunca se
estima.**

## Pasos

1. El mes es el de la entrada, o el anterior si no se indica. Copia
   `reports/_templates/monthly.md` a `reports/YYYY-MM.md`.
2. Pide la analítica al subagente `metricool-lookup`, para que los datos crudos
   no entren en la conversación. Por red (LinkedIn, Facebook, Instagram, Perfil
   de Empresa en Google): piezas, alcance, interacciones, tasa de interacción,
   clics, cambio de seguidores. Y los totales de Meta Ads y Google Ads si hay
   gasto.
3. Del sitio: sesiones, sesiones desde redes, y las dos conversiones
   (`whatsapp` y `formulario`). Si no tienes acceso a Google Analytics por
   conector, escribe "sin dato" y pídelo en el resumen. No lo estimes desde los
   clics de Metricool.
4. Cruza las publicaciones con los archivos de `content/YYYY-MM/` por
   `metricool_id`. A las que salieron, ponles `estado: published`. A las que
   siguen en `review` y ya pasó su fecha, anótalo: significa que José no las
   aprobó, y eso es un dato del proceso, no un fallo del contenido.
5. Top 5 y bottom 5 por tasa de interacción (alcance en el caso del Perfil de
   Empresa en Google). De cada una: pilar, origen, formato y una hipótesis
   corta.
6. Compara la mezcla publicada con la de `strategy/pillars.md`, y la
   interacción por pilar, por formato y **por origen** (`post`, `facts`,
   `caso`). Lo del origen es lo que más decide el mes siguiente: si las piezas
   que enlazan un artículo rinden mejor, hay que escribir más artículos.
7. "Hacer más" y "Hacer menos", 3 viñetas cada uno, **cada una con el número
   que la respalda**.
8. "Propuestas para José": cambios de mezcla, de cadencia, de red, o encender
   Meta Ads. Cada una con su dato.
9. Añade de 2 a 4 líneas a "Aprendizajes" en `strategy/pillars.md`, en el
   formato `- YYYY-MM: <aprendizaje> (dato: <métrica>)`. **No cambies tú los
   porcentajes de la mezcla**, propónlos.
10. Confirma: `report: YYYY-MM`.

## Resumen para José

Tres líneas, los clics a WhatsApp y los envíos del formulario, la pieza que
mejor funcionó, y las propuestas que necesitan su decisión.
