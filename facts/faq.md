# Preguntas frecuentes

Las del sitio, que son copia publicada y por tanto se pueden usar textuales o
reescritas. Cada una es material de post: una pregunta real con respuesta corta
rinde mejor en redes que un anuncio.

Fuente: `website-data-shuffle/src/components/Faq.astro` y `src/faq.config.ts`.
Última confirmación: 2026-10-30.

## Generales

### ¿Qué tipo de empresas atienden?
Pymes en Panamá, principalmente. Una cooperativa de más de 7 profesionales en
software, datos e IA, con proyectos armados para empresas medianas y chicas:
alcance acotado, entrega rápida y trato directo con quien desarrolla.

### ¿Cuánto cuesta un proyecto?
Depende del alcance. Primero una cotización gratuita, después precio fijo por
el trabajo acordado.

### ¿Cuánto se demora?
La mayoría entre 2 y 6 semanas, con alcance escrito antes de empezar y avances
visibles durante el desarrollo.

### ¿Tengo que botar el sistema que ya tengo?
Casi nunca. Buena parte del trabajo es aprovechar lo que ya existe: conectar
sistemas que nunca se hablaron, modernizar tecnología sin soporte, o migrar los
datos a algo mantenible.

### ¿Con qué tecnologías trabajan?
En desarrollo, Python, Java, Go y Node.js. En datos, PostgreSQL, MySQL, SQL
Server y ArangoDB, con dbt para los pipelines. En automatización, n8n y Make.
La herramienta se elige según el problema, no al revés.

### Armé algo con IA (Cursor, Lovable, ChatGPT) y ya no aguanta más parches. ¿Eso lo ven?
Sí, es un servicio propio. Se audita seguridad, credenciales expuestas y código
duplicado, se arregla lo urgente y queda listo para producción real, con
pruebas y documentación.

### ¿Puedo empezar con algo pequeño?
Sí, y es lo recomendado. El primer paso es un diagnóstico gratis por WhatsApp.

## De software e integraciones

### La herramienta que uso no está en la lista. ¿Se puede conectar igual?
Casi siempre. En orden: por API si la tiene; por los archivos que ya exporta
(CSV, XML, Excel); y si no, leyendo su base de datos cuando el proveedor lo
permite. No se promete una integración antes de ver por dónde entra.

### ¿Qué pasa si el proveedor cambia su API y la integración deja de funcionar?
Las integraciones se entregan con monitoreo y alerta: si la sincronización
falla, avisa, en vez de romperse en silencio. Durante el acompañamiento
posterior a la entrega, ajustarla a ese cambio está incluido.

### ¿El código queda mío?
Sí. En un repositorio tuyo, con su historial, credenciales a tu nombre, y con
la documentación de despliegue para que otro equipo pueda continuar.

### ¿Hacen facturación electrónica con la DGI?
Sí, es de lo que más se ha hecho. Con Factura Fácil, DigiFact y Siteck, tres de
los PAC autorizados. Incluye CUFE, reintento cuando el servicio no responde y
resguardo de los XML firmados.

## De datos

### ¿Tengo que comprar un data warehouse o una herramienta cara?
Casi nunca al principio. Para el volumen de una pyme, una base PostgreSQL bien
modelada sostiene los años de historia y los tableros, sin licencia.

### Mis datos están sucios y no cuadran. ¿Eso es un problema para empezar?
No, es el trabajo. Casi ningún proyecto empieza con datos limpios.

### ¿Power BI, Metabase o Looker Studio?
Depende de lo que el equipo ya use y pueda mantener. No se venden licencias de
ninguna. Si el pipeline está bien hecho, cambiar de tablero después es un
trabajo de días.

### ¿Cada cuánto se actualizan los datos?
Lo que haga falta para la decisión que se toma con ellos. Para la mayoría de
tableros de gestión, una actualización diaria de madrugada alcanza.

## Lo que falta

> ⚠️ POR CONFIRMAR: las preguntas que de verdad llegan por WhatsApp, y las
> objeciones reales ("está caro", "ya tengo proveedor", "lo hace mi sobrino").
> Las de arriba son las del sitio, que son las que suponemos, no las que
> contamos.

- Última confirmación: pendiente
