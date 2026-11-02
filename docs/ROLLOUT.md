# Fases

| Fase | Cuándo | Qué | Tiempo de José |
|---|---|---|---|
| 0 | Semana 0 | `docs/SETUP.md`: conectores, Metricool, prueba del render | 1 a 2 h |
| 1 | Semana 1 | Contestar `facts/QUESTIONNAIRE.md`, revisar `brand/voice.md` | 1 a 2 h |
| Piloto | Semana 2 | Correr el flujo entero a mano una vez y juzgar la calidad (`docs/PILOT-CHECKLIST.md`) | 1 h |
| 2 | Semanas 3 y 4 | `ds run publish` en vivo, con la cola de revisión de Metricool | 15 min por semana |
| 3 | Mes 2 | El cron del servidor corre `ds run week` solo los lunes (`docs/SERVER.md`). José aprueba en Metricool y mezcla la rama del artículo | 15 min por semana |
| 4 | Mes 3 | `auto_approve_evergreen: true`: las piezas evergreen salen sin aprobación. Las de `legal` y `price` siguen pasando por José, y **el artículo del sitio sigue necesitando su merge, siempre** | 15 min al mes |
| 5 | Cuando haya datos | Encender Meta Ads con `ads/playbook.md`, y revisar si Google Ads entra en este flujo | configuración única |

## Cómo se cambia de fase

La fase vive en `strategy/cadence.md` (`phase:`). Solo José la cambia. Al pasar
a Fase 4 también se pone `auto_approve_evergreen: true`.

## Lo que no cambia en ninguna fase

- **El artículo del sitio nunca se publica solo.** La corrida deja una rama
  empujada y para. Mezclar en `master` es lo que despliega, y eso lo hace una
  persona. Hay un hook (`.claude/hooks/no-publishing.sh`) que lo impide aunque
  el prompt diga otra cosa.
- **Nadie del equipo se nombra salvo José** mientras los seis perfiles del
  sitio sigan siendo placeholder.
- **Ninguna cifra sale de fuera de `facts/`.**

## Notas

- Fase 3 solo si la incógnita 4 del piloto salió bien. Si no, se sigue a mano,
  que cuesta quince minutos.
- Fase 5 depende de que haya tráfico que medir. Encender anuncios antes de
  saber qué contenido funciona es pagar por descubrirlo.
