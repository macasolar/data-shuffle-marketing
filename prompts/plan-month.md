# Planificar el mes

Escribes el plan de contenido de un mes: `content/YYYY-MM/plan.md` y un archivo
por pieza en estado `idea`.

Sigue `CLAUDE.md`. Todo el contenido en español de Panamá. Sin rayas largas.

## Lee esto antes de planificar

- `strategy/cadence.md`: cantidades por red, días, fase
- `strategy/pillars.md`: la mezcla y los "Aprendizajes"
- `strategy/audiences.md`
- `facts/`, todos los archivos, y `facts/OPEN-QUESTIONS.md`
- El último `reports/YYYY-MM.md`, si existe
- `content/` de los dos meses anteriores, para no repetir
- **Los artículos del sitio**: `$WEBSITE_REPO/src/content/blog/*.md`
  (publicados) y `draft/` (borradores). Son la materia prima: un artículo
  publicado y sin usar vale más que un tema inventado.

## Pasos

1. El mes es el de la entrada, o el siguiente si no se indica. Si
   `content/YYYY-MM/plan.md` ya existe, **para y pregunta** si se reemplaza o
   se amplía.
2. Cuenta los espacios por semana desde `cadence.md` (semana de lunes a
   domingo, las parciales en proporción).
3. Reparte los pilares para que la mezcla salga parecida a la de
   `pillars.md`, ajustada por los "Aprendizajes". Reparte también los orígenes:
   la mayoría `post`, el resto `facts` y `caso`.
4. Asigna a cada espacio un tema, una audiencia y una plantilla. Reglas:
   - Cada tema tiene que estar respaldado por `facts/` o por un artículo
     publicado. Un hecho `⚠️ POR CONFIRMAR` no se usa: o se replantea el tema
     sin esa afirmación, o entra en "Hechos que faltan".
   - El tema se nombra por el síntoma, no por el servicio.
   - Nada repetido de los dos meses anteriores, salvo con otro ángulo, y
     entonces se anota el ángulo.
   - Tag `legal` si la pieza menciona una ley, resolución, plazo o multa de la
     DGI. Tag `price` si menciona un precio o un descuento. Hoy no hay precios
     publicados, así que `price` debería quedar vacío todo el mes.
   - Las piezas de `linkedin` llevan el argumento largo; las de
     `instagram`+`facebook` van juntas en una sola pieza (cross-post); la de
     `gbp` es una por semana y casi siempre de origen `facts`.
5. **Marca qué semanas llevan artículo del sitio.** Uno por semana como techo,
   dos al mes como piso. Si el mes va a llevar artículos, apunta el tema de
   cada uno: es lo que después recibe `ds run post`.
6. Escribe `content/YYYY-MM/plan.md`:
   - Cabecera: mes, fase, mezcla de pilares objetivo contra la planeada (%).
   - Tabla: `fecha | red(es) | formato | pilar | origen | tema | audiencia | tags | id`.
   - Una sección "Artículos del mes" con el tema de cada uno y su semana.
   - "Hechos que faltan": las preguntas que, respondidas, darían mejores
     piezas. Cruza con `facts/OPEN-QUESTIONS.md` y no repitas lo que ya está
     ahí, remítete a su número de pregunta.
7. Crea un archivo por fila en `content/YYYY-MM/<id>.md`, desde
   `content/_templates/post.md`:
   - `id`: `YYYY-MM-DD-<red>-<slug>`, con la red en corto: `li`, `ig`, `gbp`.
     Un cross-post de Instagram y Facebook usa `ig`.
   - Rellena el frontmatter completo, `estado: idea`, y deja en las secciones de
     texto una línea con el ángulo. No escribas el texto final: eso es
     `make-week`.
8. Confirma: `plan: YYYY-MM content plan (N pieces)`.

## Resumen para José

- Piezas por red y por pilar, contra el objetivo.
- Los artículos propuestos para el mes, con su semana.
- Piezas con tag `legal` o `price`, que necesitarán su aprobación.
- "Hechos que faltan".
- El paso siguiente: `ds run week` el lunes.
