# CLAUDE.md — coipo_maqueta

Guía para agentes. Detalle de uso en [`README.md`](README.md); problema y solución en `insumos/`.

## Qué es
Portal de maquetas de la UIA publicado en GitHub Pages (`sitio/`). El repo **no contiene el código fuente de las
maquetas**: sólo recibe su salida compilada, con datos ficticios o agregados, y el registro `maquetas.json`.
No hay `package.json` ni `requirements.txt`; las herramientas son dos scripts de Python 3 sin dependencias externas.

## Estructura
- `maquetas.json`: registro; una entrada por carpeta de `sitio/` (campos obligatorios: carpeta, titulo, descripcion, cliente, estado, datos, actualizado).
- `sitio/index.html`: portada **generada**; no editar a mano.
- `sitio/<carpeta>/`: `personal`, `canal-ley21719` (un HTML) y `pasillo`, `pasillo-chile` (compilaciones con `assets/`).
- `herramientas/construir_portal.py`: guarda + generador de portada. `herramientas/portal.html`: plantilla. `herramientas/publicar_personal.py`: anonimiza y compila «personal» desde una fuente local (`personal/`, ignorada por git).
- `.github/workflows/pages.yml`: en cada push a `main` valida, exige que `sitio/index.html` no cambie y despliega.

## Comandos
```
python herramientas/construir_portal.py     # valida y regenera sitio/index.html (VERIFICADO: corre OK con 4 maquetas)
git diff --exit-code -- sitio/index.html    # lo que exige el CI tras validar
```
No hay pruebas automatizadas ni lint.

## Reglas
- Nunca subir datos reales: nombres, RUT, correos `@conaf.cl`, bases de prueba. Un force push no borra lo ya subido.
- Toda carpeta nueva de `sitio/` se registra en `maquetas.json` con `datos` = `ficticios` | `agregados` | `sin_datos`.
- Tras tocar `maquetas.json` o `sitio/`, correr `construir_portal.py` y commitear el `sitio/index.html` resultante.
- `.gitignore` excluye toda carpeta de primer nivel salvo `sitio/`, `herramientas/` y `.github/`: una carpeta nueva fuera de ellas no se versiona.
- Los HTML de `pasillo*` usan rutas absolutas `/coipo_maqueta/...`: no renombrar el repo ni mover las carpetas sin recompilar.

## Trampas conocidas
- `insumos/` queda ignorada por la regla `/*/` de `.gitignore`: sus documentos se agregaron con `git add -f`. Para modificarlos hay que repetirlo (o añadir `!/insumos/` al `.gitignore`).
- La guarda de RUT sólo considera números con dígito verificador válido (módulo 11); la lista `PERMITIDOS` del script autoriza casos ficticios de ejemplo.
- `HUSKY_AUDIT.md` está versionado y es una auditoría de una tarea anterior; no es documentación del proyecto.
- Con Git Bash, rutas que empiezan con `/` pueden reescribirse (un commit reciente corrigió la ruta base por MSYS_NO_PATHCONV).
