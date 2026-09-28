"""Publica la maqueta «Atrasos y Justificativos · GEDEP» en sitio/personal/ con datos FICTICIOS.

Lee el app_data.json real (fuente local, fuera del repo), reemplaza nombres y apellidos por
nombres inventados y compila la app con build.py. Falla si algún nombre real completo
queda en el HTML publicado.

Uso:  python herramientas/publicar_personal.py [--fuente=personal/app]
"""
import json
import os
import random
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OPTS = dict(a[2:].split('=', 1) for a in sys.argv[1:] if a.startswith('--') and '=' in a)
FUENTE = os.path.abspath(OPTS.get('fuente', os.path.join(RAIZ, 'personal', 'app')))
DESTINO = os.path.join(RAIZ, 'sitio', 'personal', 'index.html')
DEMO = os.path.join(FUENTE, 'app_data_demo.json')

NOMBRES = ('Ana Andrea Antonia Beatriz Camila Carla Carolina Catalina Claudia Constanza Daniela Fernanda '
           'Francisca Gabriela Isabel Javiera Josefa Karina Laura Lorena Macarena Marcela María Natalia '
           'Paola Patricia Paula Sofía Valentina Verónica Alejandro Andrés Benjamín Carlos Cristián Diego '
           'Eduardo Felipe Francisco Gonzalo Hernán Ignacio Jaime Javier Jorge José Juan Luis Manuel '
           'Martín Matías Nicolás Pablo Pedro Rodrigo Sebastián Tomás Vicente').split()
APELLIDOS = ('Acuña Aguilera Alarcón Araya Arenas Bravo Bustos Cáceres Campos Cárdenas Castillo Castro '
             'Contreras Cortés Díaz Espinoza Farías Figueroa Flores Fuentes Gallardo Garrido Gómez González '
             'Guzmán Henríquez Herrera Jara Lagos Leiva Martínez Medina Méndez Miranda Molina Morales Muñoz '
             'Navarro Núñez Olivares Orellana Ortiz Parra Pérez Pizarro Quiroz Ramírez Reyes Riquelme Rivera '
             'Rojas Salazar Sandoval Sepúlveda Silva Soto Tapia Torres Valdés Valenzuela Vargas Vega Vera '
             'Vergara Yáñez Zúñiga').split()


def anonimizar(datos):
    for p in datos['personas']:
        r = random.Random(p['c'])  # determinista: la misma persona recibe siempre el mismo nombre ficticio
        p['no'] = ' '.join(r.sample(NOMBRES, r.choice((1, 2, 2))))
        p['ap'] = ' '.join(r.sample(APELLIDOS, 2))
    m = datos['meta']
    m['fuente'] = 'DATOS FICTICIOS · maqueta de demostración (nombres inventados)'
    m['usuario'] = None
    return datos


def main():
    for f in (sys.stdout, sys.stderr):
        f.reconfigure(encoding='utf-8')
    real = json.load(open(os.path.join(FUENTE, 'app_data.json'), encoding='utf-8'))
    reales = {f"{p['ap']}, {p['no']}" for p in real['personas'] if p.get('ap') and p.get('no')}
    demo = anonimizar(json.loads(json.dumps(real)))
    with open(DEMO, 'w', encoding='utf-8') as fh:
        json.dump(demo, fh, ensure_ascii=False, separators=(',', ':'))

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    subprocess.run([sys.executable, os.path.join(FUENTE, 'build.py'), DESTINO, f'--datos={DEMO}'], check=True)

    html = open(DESTINO, encoding='utf-8').read()
    publicado = json.loads(html.split('<script type="application/json" id="datos">', 1)[1].split('</script>', 1)[0].replace('<\\/', '</'))
    fugas = [n for n in (f"{p['ap']}, {p['no']}" for p in publicado['personas']) if n in reales]
    if fugas:
        os.remove(DESTINO)
        sys.exit(f'ERROR: {len(fugas)} nombres reales en la salida (p. ej. {fugas[:3]}); se borró {DESTINO}')
    print(f'OK: {len(publicado["personas"])} personas con nombres ficticios; ningún nombre real en {DESTINO}')


if __name__ == '__main__':
    main()
