# Solución — portal estático con guarda de datos personales

## Arquitectura (VERIFICADO)
Sitio estático en `sitio/` desplegado con GitHub Pages mediante `.github/workflows/pages.yml` en cada push a `main` (y `workflow_dispatch`). Dos jobs: `validar` y `publicar`.

## Componentes
- `maquetas.json`: registro (carpeta, titulo, descripcion, cliente, estado, datos, actualizado).
- `herramientas/construir_portal.py`: (1) comprueba que cada entrada tenga todos los campos, `datos` válido y `index.html`; (2) que no haya carpetas sin registrar; (3) revisa los archivos de texto de `sitio/` buscando RUT con dígito verificador válido y correos `@conaf.cl` fuera de la lista `PERMITIDOS`; (4) genera `sitio/index.html` desde `herramientas/portal.html`, ordenando por `actualizado` descendente. Sale con código 1 si algo falla.
- `herramientas/publicar_personal.py`: anonimiza (nombres ficticios deterministas) y compila la maqueta «personal» desde una fuente local; falla si queda un nombre real. No lo ejecuté.
- Maquetas: `personal` (GEDEP), `canal-ley21719` (Transparencia), `pasillo` y `pasillo-chile` (todas las gerencias; compilaciones de otra aplicación con rutas bajo `/coipo_maqueta/`).

## Flujo de datos
Fuente fuera del repo -> compilación con datos ficticios -> `sitio/<carpeta>/` -> entrada en `maquetas.json` -> `construir_portal.py` -> commit -> push a `main` -> el CI repite la validación, exige que `sitio/index.html` no cambie y despliega.

## Decisiones
- Repo separado de las fuentes y `.gitignore` que sólo deja pasar `sitio/`, `herramientas/` y `.github/` (VERIFICADO).
- Guarda con dígito verificador (2026-10-24, decisión de Luis Monsalve según el docstring de `dv_valido`): se acepta no detectar un RUT real mal tipeado a cambio de no bloquear con coordenadas SVG.
- Los commits del 2026-10-24 agregan `pasillo` y `pasillo-chile`; el 2026-10-16 se reemplazó la versión de `canal-ley21719` (INFERIDO por el historial).

## Estado y pendientes
- Validación local OK (ejecutada al escribir este documento). Despliegue real en Pages y URL pública: no lo comprobé; `[PENDIENTE]` confirmar que Pages está activo.
- No hay pruebas automatizadas de la guarda; sólo la ejecución del script.
- La guarda no detecta otros datos personales (nombres, teléfonos, direcciones): `[PENDIENTE]` decidir si hace falta.
- `HUSKY_AUDIT.md` indica que no hay hooks locales; la única barrera es el CI.
