# Servicios

Los cuatro pilares son los del sitio. Cada uno tiene su página publicada, así
que todo lo de aquí es copia aprobada.

Fuente de todo el archivo: `website-data-shuffle/src/content/services/*.md`.
Última confirmación: 2026-10-30.

## `software-apis-integraciones`, Software a la medida, APIs e integraciones
- **La frase del cliente:** "Todo lo hacemos a mano, en Excel y WhatsApp".
- **Qué se entrega:** sistemas a la medida, APIs e integraciones entre las
  herramientas que ya usa el cliente.
- **Síntomas que busca la gente:** procesos manuales, sistemas desconectados,
  doble digitación, facturación electrónica, pedidos por WhatsApp, inventario
  descuadrado, sistema a la medida, punto de venta, reportes a mano, todo en
  Excel, cobrar en línea, planilla a mano.
- **Tecnologías:** C#, .NET, Java, Spring, Go, Node.js, TypeScript, Python,
  React, Angular, REST, GraphQL, Webhooks, SQL, no-SQL, Docker, CI/CD, PWA,
  WhatsApp API, Yappy, Factura Fácil, DigiFact, Siteck.
- **Facturación electrónica:** se trabaja con **Factura Fácil, DigiFact y
  Siteck**, tres de los PAC autorizados por la DGI. La integración incluye el
  manejo del CUFE, el reintento cuando el servicio no responde y el resguardo
  de los XML firmados.

## `datos`, Datos y analítica
- **La frase del cliente:** "Tengo los datos, pero no me dicen nada".
- **Qué se entrega:** extracción y pipelines de datos para dejar de exportar y
  pegar información a mano.
- **Síntomas:** reportes manuales, información dispersa, exportar y pegar,
  datos que no cuadran, tablero de indicadores, cierre de mes lento, un solo
  lugar, histórico sin usar, veinte hojas de cálculo, clientes duplicados.
- **Tecnologías:** Python, SQL, dbt, Pandas, Airflow, ETL / ELT, PostgreSQL,
  MySQL, SQL Server, SQLite, ArangoDB, MongoDB, Power BI, Metabase, Looker
  Studio, web scraping, APIs, Excel, Jupyter, data warehouse.
- **Postura sobre herramientas:** no se venden licencias de ninguna, así que la
  recomendación no depende de cuál conviene. Para el volumen de una pyme, una
  base PostgreSQL bien modelada alcanza y no cuesta licencia.

## `automatizacion`, IA y automatización
- **La frase del cliente:** "Se me va el día en tareas repetitivas".
- **Qué se entrega:** conectar lo que ya existe y automatizar lo repetitivo,
  **con un humano siempre en el circuito para lo sensible**.
- **Síntomas:** tareas repetitivas, copiar entre sistemas, documentos
  repetidos, seguimiento que se olvida, horas perdidas, aprobación humana,
  respuestas manuales, clasificar correos, avisar al cliente, asistente con tus
  documentos.
- **Tecnologías:** n8n, Make, Zapier, Python, LangChain, RAG, OpenAI API,
  Claude API, LLMs, embeddings, pgvector, OCR, IDP, chatbots, WhatsApp API,
  webhooks, APIs, agentes de IA, human in the loop, Google Sheets.

## `linux-cloud`, Servidores Linux y Windows, virtualización y nube
- **La frase del cliente:** "Si el servidor se cae, no sé a quién llamar".
- **Qué se entrega:** administración de servidores Linux y Windows,
  virtualización, migración a la nube y soporte.
- **Síntomas:** servidor sin dueño, respaldos sin probar, caídas sin aviso,
  migrar a la nube, monitoreo y alertas, sin documentación, accesos perdidos,
  servidor Windows viejo, máquinas virtuales, mantenimiento de servidores,
  certificado vencido, factura de la nube, hosting que no aguanta.
- **Tecnologías:** Linux, Ubuntu, Debian, RHEL, Windows Server, Active
  Directory, IIS, PowerShell, Proxmox, VMware, Hyper-V, máquinas virtuales,
  Nginx, Apache, Docker, Bash, SSH, systemd, AWS, DigitalOcean, Cloudflare,
  VPS, VPN, backups, monitoreo, SSL / TLS, CI/CD.

## Un servicio propio que no es un pilar
**Rescate de proyectos hechos con IA.** Alguien armó algo con Cursor, Lovable o
ChatGPT y ya no aguanta más parches. Se audita (seguridad, credenciales
expuestas, código duplicado), se arregla lo urgente y se deja listo para
producción real, con pruebas y documentación.
- Fuente: `website-data-shuffle/src/components/Faq.astro`

## Cómo se trabaja, y esto se puede decir en cualquier post
- **Diagnóstico gratis** por WhatsApp: se revisa el proceso y se identifican 2 o
  3 oportunidades concretas, sin compromiso.
- **Cotización gratuita y después precio fijo** por el trabajo acordado. Sin
  sorpresas a mitad de camino.
- **Alcance delimitado y escrito antes de empezar**, con avances visibles
  durante el desarrollo en vez de una sola entrega al final.
- **La mayoría de los proyectos toma entre 2 y 6 semanas.** Una integración
  puntual entre dos sistemas se entrega en días.
- **Casi nunca hay que botar el sistema que ya existe.**
- **El código queda del cliente**, en un repositorio suyo, con su historial, y
  las credenciales a su nombre.
- Fuente: `website-data-shuffle/src/components/Faq.astro` y
  `src/faq.config.ts`
