"""Valida sitio/ contra maquetas.json y genera la portada sitio/index.html.

Falla (código 1) si:
  - una carpeta de sitio/ no está registrada en maquetas.json, o una registrada no tiene index.html;
  - una maqueta no declara datos publicables («ficticios», «agregados» o «sin_datos»);
  - algún archivo publicado contiene un valor con forma de RUT o una casilla @conaf.cl real.

Uso:  python herramientas/construir_portal.py
"""
import html
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITIO = os.path.join(RAIZ, 'sitio')
DATOS_OK = {'ficticios': 'Datos ficticios', 'agregados': 'Solo datos agregados', 'sin_datos': 'Sin datos'}
CAMPOS = ('carpeta', 'titulo', 'descripcion', 'cliente', 'estado', 'datos', 'actualizado')
RUT = re.compile(r'(?<![\d.])\d{1,2}\.?\d{3}\.?\d{3}-[\dkK](?![\w])')
CORREO = re.compile(r'[\w.+-]+@conaf\.cl', re.I)
PERMITIDOS = {'12345678-K', '12.345.678-K', 'nombre@conaf.cl', 'casilla@conaf.cl'}  # ejemplos de formato en el código
TEXTO = ('.html', '.js', '.json', '.css', '.csv', '.txt', '.md', '.svg')


def revisar_archivos(errores):
    for dirpath, _, archivos in os.walk(SITIO):
        for a in archivos:
            ruta = os.path.join(dirpath, a)
            if not a.endswith(TEXTO):
                continue
            txt = open(ruta, encoding='utf-8', errors='replace').read()
            hallados = {m.group(0) for p in (RUT, CORREO) for m in p.finditer(txt)} - PERMITIDOS
            if hallados:
                errores.append(f'{os.path.relpath(ruta, RAIZ)}: posibles datos personales {sorted(hallados)[:5]}')


def main():
    for f in (sys.stdout, sys.stderr):
        f.reconfigure(encoding='utf-8')
    maquetas = json.load(open(os.path.join(RAIZ, 'maquetas.json'), encoding='utf-8'))
    errores = []
    registradas = set()
    for m in maquetas:
        faltan = [c for c in CAMPOS if not m.get(c)]
        if faltan:
            errores.append(f'maquetas.json: «{m.get("carpeta", "?")}» sin {faltan}')
            continue
        registradas.add(m['carpeta'])
        if m['datos'] not in DATOS_OK:
            errores.append(f'maquetas.json: «{m["carpeta"]}» datos="{m["datos"]}"; debe ser uno de {sorted(DATOS_OK)}')
        if not os.path.isfile(os.path.join(SITIO, m['carpeta'], 'index.html')):
            errores.append(f'sitio/{m["carpeta"]}/index.html no existe')
    carpetas = {d for d in os.listdir(SITIO) if os.path.isdir(os.path.join(SITIO, d))} if os.path.isdir(SITIO) else set()
    for d in sorted(carpetas - registradas):
        errores.append(f'sitio/{d}/ no está registrada en maquetas.json')
    revisar_archivos(errores)
    if errores:
        print('ERROR: el sitio no se puede publicar\n  - ' + '\n  - '.join(errores), file=sys.stderr)
        sys.exit(1)

    tarjetas = '\n'.join(
        f'''    <a class="card" href="{html.escape(m['carpeta'])}/">
      <div class="meta"><span class="tag">{html.escape(m['cliente'])}</span><span class="tag">{html.escape(m['estado'])}</span><span class="tag datos">{DATOS_OK[m['datos']]}</span></div>
      <h2>{html.escape(m['titulo'])}</h2>
      <p>{html.escape(m['descripcion'])}</p>
      <span class="fecha">Actualizado {html.escape(m['actualizado'])}</span>
    </a>''' for m in sorted(maquetas, key=lambda m: m['actualizado'], reverse=True))
    plantilla = open(os.path.join(RAIZ, 'herramientas', 'portal.html'), encoding='utf-8').read()
    assert plantilla.count('<!--TARJETAS-->') == 1
    with open(os.path.join(SITIO, 'index.html'), 'w', encoding='utf-8') as fh:
        fh.write(plantilla.replace('<!--TARJETAS-->', tarjetas))
    print(f'OK: {len(maquetas)} maqueta(s) validadas; portada en sitio/index.html')


if __name__ == '__main__':
    main()
