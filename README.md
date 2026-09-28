# coipo_maqueta

Portal de maquetas de la Unidad de Información y Análisis (UIA), publicado con GitHub Pages.
Reúne prototipos navegables para mostrar a usuarios y expertos antes de construir la versión
de producción. Pensado para crecer: cada maqueta nueva se agrega sin tocar las demás.

**Sitio publicado:** `https://sud-austral.github.io/coipo_maqueta/` (se activa la primera vez
que se hace push a `main`; ver «Publicar» más abajo).

## Estructura

```
maquetas.json                 registro de maquetas: una entrada por maqueta publicada
sitio/                        lo que se publica tal cual en GitHub Pages
  index.html                  portada (generada, no editar a mano)
  <carpeta>/                  una maqueta compilada y autocontenida (HTML+JS+datos en un archivo)
herramientas/
  portal.html                 plantilla de la portada
  construir_portal.py         valida sitio/ contra maquetas.json y genera sitio/index.html
  publicar_personal.py        ejemplo: anonimiza y compila la maqueta «Atrasos y Justificativos»
.github/workflows/pages.yml   valida y despliega a Pages en cada push a main
```

La **fuente** de cada maqueta (código de la app, datos reales, base de datos) vive **fuera de
este repositorio** — en el repo del proyecto correspondiente, o en una carpeta local que
`.gitignore` excluye (ver `personal/`, que no se versiona aquí). Este repositorio solo recibe
la maqueta ya compilada, autocontenida y con datos ficticios o agregados, más el registro en
`maquetas.json`.

## Por qué está separado así

Este repo es público (o de acceso amplio) porque es lo que se comparte con usuarios y expertos.
Las fuentes suelen tener datos reales (nombres, RUT, bases de prueba) que **nunca** deben llegar
a un commit aquí, ni siquiera de forma transitoria: un `git push --force` no borra lo que ya se
subió. Por eso `construir_portal.py` es una guarda, no una formalidad — falla si detecta algo
con forma de RUT o de correo `@conaf.cl` real, o si una carpeta de `sitio/` no está registrada.

## Agregar una maqueta nueva

1. Compilar la maqueta en un **único HTML autocontenido** (sin dependencias externas rotas: los
   `<script src>`/`<link>` externos deben ser CDN públicos, como fuentes de Google Fonts).
2. Copiarlo a `sitio/<carpeta-nueva>/index.html`.
3. Agregar una entrada en `maquetas.json`:
   ```json
   {
     "carpeta": "carpeta-nueva",
     "titulo": "Nombre para mostrar",
     "descripcion": "Una frase.",
     "cliente": "Área o gerencia",
     "estado": "prototipo",
     "datos": "ficticios",
     "actualizado": "AAAA-MM-DD"
   }
   ```
   `"datos"` debe ser `"ficticios"`, `"agregados"` (solo cifras de grupo, sin individuos) o
   `"sin_datos"` — es lo que se muestra como etiqueta en la portada y lo que la guarda exige
   declarar explícitamente.
4. Validar y generar la portada:
   ```bash
   python herramientas/construir_portal.py
   ```
5. Revisar `git status`, hacer commit y push a `main`. El workflow de GitHub Actions valida de
   nuevo (independiente de que ya haya pasado local) y despliega.

## Publicar (una sola vez)

En GitHub: **Settings → Pages → Build and deployment → Source: GitHub Actions**. De ahí en
adelante cada push a `main` que pase la validación se publica solo.

## La maqueta «Atrasos y Justificativos» (ejemplo)

Su fuente completa (app, base de datos, herramientas de carga) vive en `personal/`, local y
fuera de este repo. `herramientas/publicar_personal.py` toma `personal/app/app_data.json` (los
datos reales, generados con la base de prueba — ver `personal/README.md`), reemplaza nombre y
apellido de cada persona por un nombre ficticio determinista, compila con `personal/app/build.py`
y verifica que ningún nombre real haya quedado en la salida antes de escribir
`sitio/personal/index.html`.
