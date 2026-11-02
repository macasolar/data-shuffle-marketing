# Playbook de anuncios

> ⚠️ POR CONFIRMAR: **todo este archivo es borrador.** No hay ninguna campaña
> corriendo. José ajusta los umbrales antes de encender nada (Q10 a Q12 del
> cuestionario).

Esto es Fase 5 (`docs/ROLLOUT.md`), y a propósito va al final: encender
anuncios antes de saber qué contenido funciona es pagar por descubrirlo.
Primero hay que tener tres meses de datos orgánicos.

## Lo que ya está instalado

- Meta Pixel `1689401399359995` en el sitio.
- Google Ads `AW-18466592069`, con dos conversiones: `whatsapp` y `formulario`.
- Google Analytics 4 `G-NREDG185HK`.
- La cuenta publicitaria de Meta existe. No hay campañas.

## Estructura propuesta

- **Una campaña** Meta, objetivo **Leads** (clic a WhatsApp o evento `Lead`).
- Presupuesto: lo decide José.
- Mantener entre **3 y 6 anuncios activos**.
- La audiencia sale de `strategy/audiences.md`, no de una segmentación nueva.

## Lo que Claude puede hacer, cuando se encienda

- Leer insights (7 y 28 días).
- Crear anuncios dentro de campañas ya listadas en `ads/campaigns.md`, con
  creatividades de piezas `approved`.
- Pausar un anuncio que cumpla la regla de pausa.

## Lo que Claude no hace nunca

- Cambiar un presupuesto.
- Crear una campaña nueva.
- Tocar la configuración de pago.
- Usar una creatividad o un texto con tag `legal` o `price` sin aprobación.

Todo eso se **propone** en `ads/log.md`.

## Reglas de evaluación, en borrador

- **Periodo mínimo:** 7 días y 15 dólares antes de juzgar un anuncio.
- **Pausa:** costo por lead más de 2 veces el promedio de la campaña en los
  últimos 7 días.
- **Sin leads:** 7 días y 15 dólares sin un solo lead, teniendo la campaña
  leads, se pausa.
- **Mínimo activo:** nunca menos de 3 anuncios. Si pausar dejaría menos, se
  crean variantes primero.
- **Frecuencia:** por encima de 3 en 7 días, proponer refrescar creatividades.
