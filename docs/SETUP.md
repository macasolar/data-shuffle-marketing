# SETUP, para José

Una sola vez. Marca cada casilla al terminar.

## 1. Python y el repo

Esto es para trabajar en esta máquina. El servidor corre lo mismo en Docker,
y su instalación está en `docs/SERVER.md`.

- [ ] `uv` (`pip install --user uv`) y luego `uv sync`, que instala Python 3.12
      y las dependencias en `.venv/`.
- [ ] `cp .env.example .env` y apuntar `WEBSITE_REPO` al checkout del sitio.
- [ ] `uv run pytest` tiene que pasar entero.
- [ ] ImageMagick, para el recorte final de cada imagen:
      `sudo apt install imagemagick`. Se comprueba con `convert -version`.
- [ ] Google Chrome. Ya está (`google-chrome --version`).
- [ ] Abrir Claude Code una vez en este repo y aceptar el aviso de confianza.
      Sin eso, las corridas ignoran la lista de permisos de
      `.claude/settings.json` y `ds run` se niega a arrancar.

Los comandos se corren con `uv run ds ...`, o activando antes el entorno
(`source .venv/bin/activate`) para escribir solo `ds ...`.

Prueba de que el render funciona:

```
echo '{"kicker":"Datos","titulo":"Una prueba","cuerpo":"Texto corto.","cta":"Escríbenos"}' > /tmp/t.json
ds render linkedin /tmp/t.json /tmp/t.png
```

Tiene que salir un PNG de 1200x627 con la tipografía del sitio y el logo
completo. Si las letras salen distintas a las del sitio, las fuentes no
cargaron y hay que mirar `ds/render.py`.

## 2. Conectores en Claude Code

En Claude Code, `/mcp`. Se autorizan **por máquina**, no en el repo: así ningún
token acaba en git, y el runner (`ds run`) usa los mismos.

- [ ] **Metricool**: https://metricool.com/metricool-claude-mcp-guide/
- [ ] **Canva** (solo para los reels, y solo cuando se vaya a hacer video):
      https://www.canva.com/help/connect-claude-to-canva/
- [ ] **Meta Ads** (Fase 2, todavía no): al autorizar, elegir
      **lectura y escritura sin permiso financiero**.

Prueba cada uno con algo de solo lectura:

- [ ] Metricool: "lista mis marcas en Metricool"
- [ ] Canva: "lista mis brand templates en Canva"

## 3. Metricool

- [ ] La marca "Data-Shuffle" existe y tiene conectadas:
  - [ ] Página de empresa en LinkedIn (https://www.linkedin.com/company/data-shuffle/)
  - [ ] Página de Facebook (https://www.facebook.com/data.shuffle)
  - [ ] Instagram business (@data.shuffle)
  - [ ] Perfil de Empresa en Google
- [ ] El plan permite **publicar en LinkedIn** (en Metricool es el plan
      Starter o superior). Sin eso, la red que más pesa aquí no se puede
      programar.
- [ ] La **cola de revisión** está activada, que es donde van a caer las
      piezas antes de salir.

## 4. Perfil de Empresa en Google

- [ ] Reclamado y verificado.
- [ ] Las piezas de marca ya están hechas, en
      `website-data-shuffle/brand/`: logo 720x720, portada 1024x576 y cuatro
      fotos de 1024x768, una por área.

## 5. Canva, solo si se van a hacer reels

- [ ] Canva Pro (el autofill de Brand Templates lo necesita).
- [ ] Brand Kit "Data-Shuffle" con los colores y tipografías de
      `brand/visual.md` y el logo de `brand/templates/_logo.svg`.
- [ ] Las dos plantillas de `brand/canva-templates.md`, y pegar sus IDs ahí.

## 6. Lo que falta de información

- [ ] Contestar `facts/QUESTIONNAIRE.md`, aunque sea por nota de voz, y
      pasarlo por el skill `add-fact`. Son 13 preguntas: el sitio ya contestó
      el resto.
