# Pilares de contenido

Los cuatro primeros son los pilares de servicio del sitio, así que un post
siempre cae en una página que existe y puede enlazarla. Los dos últimos no son
servicios, son las dos cosas que más venden en una cooperativa chica: la prueba
de que el trabajo se hizo, y la forma de trabajar.

Mezcla inicial. Se ajusta cada mes con los datos (`ds run report`).

| Pilar (`pilar`) | % | De qué se habla |
|---|---|---|
| `software-apis-integraciones` | 20% | Integraciones entre sistemas, facturación electrónica con la DGI, sistemas a la medida, doble digitación, pedidos por WhatsApp |
| `datos` | 20% | Reportes manuales, datos que no cuadran, tableros, cierre de mes, consolidar hojas de cálculo |
| `automatizacion` | 20% | Tareas repetitivas, leer documentos con IA, clasificar correos, agentes, humano en el circuito |
| `linux-cloud` | 15% | Servidor sin dueño, respaldos sin probar, migrar a la nube, certificados vencidos, monitoreo |
| `prueba` | 15% | Los casos reales del sitio y los dos testimonios con nombre (solo de `facts/cases.md`) |
| `como-trabajamos` | 10% | Diagnóstico gratis, alcance cerrado y precio fijo, el código queda del cliente, 2 a 6 semanas, rescate de proyectos hechos con IA |

## Reglas

- **El síntoma antes que el servicio.** Cada pieza arranca por la frase que
  diría el cliente, que es lo que está en `problemTags` de cada servicio del
  sitio. Nadie busca "ingeniería de datos".
- **Un pilar de servicio por día, sin repetir dos días seguidos.** Y nunca dos
  piezas de `como-trabajamos` en la misma semana: es lo que más rápido suena a
  venta.
- **`prueba` solo sale de `facts/cases.md`.** Un caso que el sitio marca como
  "Ejemplo ilustrativo" se cuenta como ejemplo, nunca como algo que pasó.
- **Sin precios.** No hay lista de precios publicada, así que hoy ninguna pieza
  lleva tag `price`. Lo que sí se puede decir está en `facts/offers.md`:
  diagnóstico gratis, cotización gratuita, precio fijo, 2 a 6 semanas.
- **Nadie del equipo se nombra salvo José** mientras los otros seis perfiles
  del sitio sigan siendo placeholder (`facts/company.md`).
- **Evergreen:** una pieza es evergreen si no depende de una fecha, no cita una
  oferta y no lleva tags `legal` ni `price`. Casi todo lo de `datos`,
  `automatizacion` y `linux-cloud` lo es.
- **Reciclar es la norma, no la excepción.** El sitio tiene 29 artículos
  publicados y 22 borradores. Un artículo da varias piezas: el síntoma, una
  pregunta de su FAQ, el caso, un dato suelto. Antes de inventar un tema nuevo,
  se mira qué hay publicado sin usar.

## De dónde sale cada pieza

Tres orígenes, y el campo `origen` del archivo dice cuál:

- `post`: de un artículo publicado en el sitio. La pieza enlaza al artículo.
  Es el origen preferido, porque lleva tráfico a donde está el formulario.
- `facts`: de `facts/` directamente, sin artículo que enlazar. Es lo normal en
  el Perfil de Empresa en Google y en las piezas de `como-trabajamos`.
- `caso`: de un caso de `facts/cases.md`. Enlaza al artículo del caso cuando
  existe.

## Aprendizajes

Se llena cada mes desde `ds run report`. Formato:
`- YYYY-MM: <aprendizaje> (dato: <métrica>)`.

_(vacío)_
