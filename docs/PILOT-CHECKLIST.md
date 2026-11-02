# Piloto, semana 2

Correr el sistema entero una vez, a mano, para ver la calidad y descubrir los
límites de los conectores antes de dejarlo solo.

## Pasos

1. [ ] `ds run plan` para el mes siguiente. Revisar que el plan respete la
       cadencia y la mezcla de pilares, y que cada tema tenga de dónde salir.
2. [ ] `ds run post --input '{"tema": "<un tema del plan>"}'`. Revisar la rama que deja:
       leer el artículo entero, mirar la página construida, comprobar los
       enlaces. **No mezclarla todavía.**
3. [ ] Mezclar esa rama a mano y desplegar, para que el artículo tenga URL
       viva.
4. [ ] `ds run week`. Mirar los PNG uno por uno y leer los textos.
5. [ ] Anotar el feedback en cada archivo, bajo "Notas / feedback de José".
6. [ ] Ajustar `brand/voice.md` y las plantillas con ese feedback.
7. [ ] Aprobar **una sola pieza** (`estado: approved`) y correr
       `ds run publish`. Comprobar en Metricool que llegó bien: texto,
       imagen, red, hora.

## Incógnitas que hay que resolver

| # | Pregunta | Cómo se prueba | Resultado | Plan B |
|---|---|---|---|---|
| 1 | ¿El conector de Metricool adjunta un PNG local? | Programar 1 pieza con imagen | | Subir la imagen a mano en Metricool, Claude deja el texto listo |
| 2 | ¿`createScheduledPostForReview` deja la pieza en la cola de revisión de verdad? | Mandar 1 y mirar en la app | | Programar con 3+ días de anticipación para poder cancelar |
| 3 | ¿El artículo que escribe `ds run post` está a la altura de los 29 ya publicados? | Leerlo entero, compararlo con `capturar-gastos-y-facturas-en-quickbooks.md` | | Usar la corrida para el borrador y terminarlo a mano |
| 4 | ¿Los tres pasos corren sin nadie delante? | Correr `docker compose run --rm -T ds run week` en el servidor sin nadie delante, como lo harÃ­a el cron (`docs/SERVER.md`) | | Seguir corriéndolo a mano los lunes |
| 5 | ¿Las imágenes se ven bien en el teléfono, no solo en el PNG? | Mirar la vista previa de Metricool en el móvil | | Ajustar tamaños en las plantillas |
| 6 | ¿Cuánto cuesta cada corrida? | `ds runs`: el coste de cada corrida queda en `runs/runs.db` | | Bajar el modelo para `plan` y `report`, dejar Opus solo para escribir |

## Para pasar a Fase 2

- [ ] José aprobaría al menos 4 de cada 5 piezas con cambios menores.
- [ ] Ninguna afirmación salió de fuera de `facts/`.
- [ ] Las incógnitas 1 y 2 tienen respuesta.
- [ ] El artículo de la incógnita 3 se publicó sin reescribirlo entero.
