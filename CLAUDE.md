# CLAUDE.md — coipo_maqueta

## Qué es

Portal público (GitHub Pages) de maquetas de la UIA. Solo versiona la **salida** compilada
(`sitio/`), el registro `maquetas.json` y las herramientas. Cómo agregar y publicar una
maqueta: `README.md` (manda en eso).

## Lo que no se puede romper

- **Ningún dato real llega a un commit.** El repo es público y un `push --force` no borra lo ya
  subido. La fuente de cada maqueta vive fuera (otro repo o carpeta local); `.gitignore`
  ignora toda carpeta de primer nivel salvo `sitio/`, `herramientas/` y `.github/` a propósito.
  No lo "arregles".
- `herramientas/construir_portal.py` es la guarda (RUT con dígito verificador válido, correos
  `@conaf.cl`, carpetas sin registrar). Corre igual en el CI (`.github/workflows/pages.yml`).
  La lista blanca de RUT/correos ficticios está en el propio script: agregar a ella es una
  decisión, no un arreglo para que pase.
- `sitio/index.html` es **generado** por `construir_portal.py` desde `herramientas/portal.html`;
  no se edita a mano. El CI falla si quedó desactualizado.

## Comandos

- `python herramientas/construir_portal.py` — valida y regenera la portada. Verificado el
  2026-11-24: `OK: 3 maqueta(s) validadas`.
- `herramientas/publicar_personal.py` necesita la carpeta local `personal/`, que no está en el
  repo: no comprobado.
- No hay npm, pruebas ni lint (ver `HUSKY_AUDIT.md`).

## Trampas

- En Git Bash, una ruta base como `/coipo_maqueta/` en un argumento se reescribe a ruta de
  Windows; usar `MSYS_NO_PATHCONV=1` (commit `2635f96`).
- `pasillo` trae varios archivos y fuentes propias; no es un HTML único.

## Git

- Rama por defecto `main`; cada push a `main` publica.
