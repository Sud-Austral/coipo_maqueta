# Problema — mostrar prototipos a usuarios y expertos sin exponer datos reales

Marcas: VERIFICADO (visto en el repo), INFERIDO (deducido), `[PENDIENTE]` lo confirma el equipo.

## Contexto
La Unidad de Información y Análisis (UIA) de CONAF construye prototipos de aplicaciones para validarlos con usuarios y
expertos antes de la versión de producción (README: «Portal de maquetas de la UIA»). VERIFICADO.

## Usuarios
- Quienes revisan las maquetas: gerencias y áreas cliente (`maquetas.json` registra GEDEP, Transparencia y «Todas las gerencias»). VERIFICADO.
- Quien publica: el equipo de la UIA. INFERIDO.
- Cuántas personas ven el portal y con qué frecuencia: `[PENDIENTE]`.

## Dolor
- Compartir un prototipo exige un lugar navegable, estable y de acceso amplio. INFERIDO.
- Las fuentes de las maquetas suelen tener datos reales (nombres, RUT, bases de prueba) que no deben llegar al repositorio de acceso amplio; un force push no los borra (README). VERIFICADO como riesgo declarado.
- Hay que evitar que una maqueta nueva rompa las demás (README: «cada maqueta nueva se agrega sin tocar las demás»). VERIFICADO.

## Alcance
Hospedar maquetas ya compiladas, con datos ficticios o agregados, en GitHub Pages; registrarlas; bloquear la publicación si se detecta un RUT válido o un correo `@conaf.cl` real.

## Fuera de alcance
El código fuente y los datos reales de cada maqueta (viven en otros repos o en carpetas locales ignoradas); autenticación de los visitantes (el sitio es público o de acceso amplio según GitHub Pages: `[PENDIENTE]` confirmar visibilidad real); cualquier evaluación del contenido de cada maqueta.

## Criterios de éxito (derivados del repo)
- `python herramientas/construir_portal.py` termina OK (comprobado al escribir este documento, con 4 maquetas).
- `sitio/index.html` queda sin cambios tras validar (lo exige el CI).
- Ninguna carpeta de `sitio/` sin registro; ninguna maqueta sin declarar el tipo de datos.
- Cifras de uso o satisfacción: no existen en el repo; no las comprobé.
