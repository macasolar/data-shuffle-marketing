# El servidor (Compute Engine, Docker)

Las corridas en producción salen de un contenedor en la VM de Google Compute
Engine. El contenedor no queda prendido: cada corrida es un
`docker compose run --rm ds ...` que arranca, hace su trabajo y se apaga. Quien
decide cuándo es el programador externo (cron de la VM, u otro).

El repo **no** va dentro de la imagen: se monta en `/app`. Las corridas
escriben en `content/` y confirman ahí, y esos cambios tienen que quedar en el
checkout de la VM, no en una capa del contenedor que desaparece.

## Una sola vez

### 1. Docker y los dos repos

```bash
sudo apt install docker.io docker-compose-v2
sudo usermod -aG docker $USER          # salir y volver a entrar
sudo mkdir -p /srv/data-shuffle && sudo chown $USER /srv/data-shuffle
cd /srv/data-shuffle
git clone git@github.com:macasolar/data-shuffle-marketing.git marketing
git clone git@github.com:macasolar/web-data-shuffle.git website
```

### 2. Llave de despliegue para el sitio

La corrida del artículo empuja una rama `post/*` al repo del sitio. Una llave
propia, solo para eso:

```bash
mkdir -p /srv/data-shuffle/ssh && cd /srv/data-shuffle/ssh
ssh-keygen -t ed25519 -f id_ed25519 -N "" -C "ds-marketing@vm"
ssh-keyscan github.com > known_hosts
```

`id_ed25519.pub` va en GitHub, en `web-data-shuffle` > Settings > Deploy keys,
**con permiso de escritura**. La regla de que nunca se toca `master` no depende
de esta llave: la ponen el hook `no-publishing.sh` y la protección de rama.

Si el repo de marketing también se empuja desde la VM, necesita su propia
llave de despliegue (GitHub no deja usar la misma en dos repos).

### 3. `.env`

```bash
cd /srv/data-shuffle/marketing && cp .env.example .env
```

- `CLAUDE_CODE_OAUTH_TOKEN`: se saca en tu máquina con `claude setup-token`
  (dura un año). **No pongas también `ANTHROPIC_API_KEY`**: si están las dos,
  `ds run` se niega a arrancar, porque la de la API ganaría sin avisar y la
  cuenta pasaría a pagarse por token.
- `WEBSITE_HOST_PATH=/srv/data-shuffle/website`
- `SSH_DIR=/srv/data-shuffle/ssh`
- `HOST_UID=` la salida de `id -u`, para que los archivos que escriben las
  corridas sigan siendo tuyos.

### 4. Imagen y dependencias del sitio

```bash
docker compose build
docker compose run --rm -w /work/website --entrypoint npm ds ci
```

### 5. Confianza y Metricool, dentro del contenedor

```bash
docker compose run --rm --entrypoint claude ds
```

Abre Claude Code dentro del contenedor, en `/app`:

1. Acepta el aviso de confianza de la carpeta. Sin eso las corridas ignoran los
   permisos de `.claude/settings.json`, y `ds run` lo detecta y no arranca.
2. `/mcp` y autoriza **metricool**.

Las dos cosas quedan en el volumen `claude-home`, y sobreviven a cada
`docker compose run --rm` y a cada reconstrucción de la imagen.

> ⚠️ POR VERIFICAR: la autorización de Metricool redirige a un `localhost` del
> contenedor, y la VM no tiene navegador. Si al pegar la URL en tu navegador la
> vuelta falla, la salida es un túnel: `ssh -L <puerto>:localhost:<puerto>` a
> la VM, con ese puerto publicado en el `docker compose run` (`-p`). El puerto
> lo muestra Claude al empezar la autorización. Se confirma la primera vez que
> se haga.

### 6. Comprobar

```bash
docker compose run --rm ds run week --dry-run   # el prompt, sin llamar a nada
docker compose run --rm ds check
docker compose run --rm ds runs
```

## El programador

Ejemplo con el cron de la VM. La VM está en UTC y Panamá en UTC-5 todo el año
(no hay horario de verano), así que las 12:00 UTC son las 07:00 en Panamá.

```cron
# lunes 07:00 Panamá: las piezas de la semana
0 12 * * 1  cd /srv/data-shuffle/marketing && docker compose run --rm -T ds run week >> runs/cron.log 2>&1
# día 1, 08:00 Panamá: reporte del mes anterior y plan del mes
0 13 1 * *  cd /srv/data-shuffle/marketing && docker compose run --rm -T ds run report >> runs/cron.log 2>&1
30 13 1 * * cd /srv/data-shuffle/marketing && docker compose run --rm -T ds run plan >> runs/cron.log 2>&1
```

`publish` no va en el cron durante el piloto: José aprueba primero.

Dos corridas a la vez no pueden pasar: la segunda sale con código 6 y no hace
nada. Separa las horas.

## Dónde mirar

| Qué | Dónde |
|---|---|
| Una línea por corrida: estado, coste, duración, turnos, error | `ds runs`, o `runs/runs.db` (SQLite) |
| Lo que hizo el agente, mensaje por mensaje | `runs/<id>/events.jsonl` |
| El prompt exacto y la entrada | `runs/<id>/prompt.md`, `runs/<id>/input.json` |
| El resultado que vio el programador | `runs/<id>/result.json` |
| Errores del CLI de Claude | `runs/<id>/stderr.log` |
| Log general en JSON | `runs/ds.log` |

Una corrida que murió a la mitad queda en `runs.db` con estado `running`: se
inserta antes de empezar, justamente para que no desaparezca.

## Códigos de salida

| Código | Significa | Qué hacer |
|---|---|---|
| 0 | bien | nada |
| 1 | `ds check` o `ds render` encontró problemas | leer la salida |
| 2 | entrada inválida, no se gastó nada | corregir el JSON del programador |
| 3 | el agente falló | leer `events.jsonl` y `stderr.log` |
| 4 | tocó el tope de coste o de turnos | ver si el tope es corto o si el agente se perdió |
| 5 | falta algo del entorno: credenciales, confianza, sitio, Chrome | el mensaje dice qué |
| 6 | ya había otra corrida | reprogramar |

Un error pasajero de la API (429, 529, conexión) se reintenta solo, hasta dos
veces, **pero solo si el agente todavía no había usado ninguna herramienta**.
Si ya había confirmado, empujado o programado algo, repetir la corrida podría
hacerlo dos veces, así que para y lo decide una persona.
