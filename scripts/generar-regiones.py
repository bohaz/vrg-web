#!/usr/bin/env python3
"""Genera las páginas por región (regiones/<slug>.html) a partir de data/regiones.json.

El encabezado y el pie se copian de index.html, así hay una sola fuente para la
navegación. Para actualizar valores de una temporada: editar el JSON y correr

    python3 scripts/generar-regiones.py
"""
import html
import json
import re
from pathlib import Path
from urllib.parse import quote

RAIZ = Path(__file__).resolve().parent.parent
PEXELS = "https://images.pexels.com/photos/{id}/pexels-photo-{id}.jpeg?auto=compress&cs=tinysrgb&w={w}"


def bloque(fuente: str, inicio: str, fin: str) -> str:
    """Devuelve el HTML entre dos marcadores de index.html (incluidos)."""
    i = fuente.index(inicio)
    j = fuente.index(fin, i) + len(fin)
    return fuente[i:j]


def a_subcarpeta(fragmento: str) -> str:
    """Ajusta rutas de index.html para usarlas desde /regiones/."""
    fragmento = re.sub(r'href="#([\w-]+)"', r'href="../#\1"', fragmento)
    fragmento = fragmento.replace('src="img/', 'src="../img/').replace('srcset="img/', 'srcset="../img/')
    fragmento = fragmento.replace(' class="is-active"', "")
    fragmento = fragmento.replace('<a href="../#regiones">Planes</a>', '<a href="../#regiones" class="is-active">Planes</a>')
    return fragmento


def esc(t: str) -> str:
    return html.escape(t, quote=True)


def hitos(filas):
    primera = next(f for f in filas if f["compania"] > 0)
    final = filas[-1]
    return primera, final


def tabla(tramo) -> str:
    filas_html = []
    for f in tramo["filas"]:
        nota = f'<small>{esc(f["nota"])}</small>' if f.get("nota") else ""
        filas_html.append(f"""
          <li class="split__row">
            <div class="split__period">{esc(f["periodo"])}{nota}</div>
            <div class="split__bar" role="img" aria-label="VRG {f['vrg']}%, Compañía {f['compania']}%">
              <span class="split__vrg" style="--w:{f['vrg']}%">{f['vrg']}%</span>
              <span class="split__cia" style="--w:{f['compania']}%">{f['compania'] if f['compania'] else ''}{'%' if f['compania'] else ''}</span>
            </div>
          </li>""")
    zona = f'<h3 class="split__zone">{esc(tramo["zona"])}</h3>' if tramo["zona"] else ""
    return f"""
      <div class="split reveal">
        {zona}
        <div class="split__legend"><span class="dot dot--vrg"></span>VRG (financia la campaña) <span class="dot dot--cia"></span>Tu Compañía</div>
        <ol class="split__list">{''.join(filas_html)}
        </ol>
      </div>"""


def pagina(r, todas, temporada, cabecera, pie) -> str:
    primera, final = hitos(r["tramos"][0]["filas"])
    img_hero = PEXELS.format(id=r["imagen"], w=1920)
    tablas = "".join(tabla(t) for t in r["tramos"])
    enlaces = []
    for o in todas:
        actual = o["slug"] == r["slug"]
        clase = "region region--hl" if actual else "region"
        aria = ' aria-current="page"' if actual else ""
        enlaces.append(f'<a class="{clase}" href="{o["slug"]}.html"{aria}><span>{esc(o["prefijo"])}</span>{esc(o["corto"])}</a>')
    otras = "".join(enlaces)
    wa = "https://wa.me/56991787727?text=" + quote("Hola VRG, quiero agendar un diagnóstico para la " + r["nombre"])
    nota_rm = ""
    if len(r["tramos"]) > 1:
        nota_rm = '<p class="plan__hint">La Provincia de Santiago tiene condiciones propias. Revisa el tramo que corresponde a tu Cuerpo.</p>'
    titulo = f'Plan de campaña {r["nombre"]} {temporada}'
    desc = (f'Condiciones de la campaña de captación de socios cooperadores de VRG para Bomberos de la {r["nombre"]}: '
            f'{final["compania"]}% para la Compañía desde el {final["periodo"].lower().replace(" en adelante", "")}, contrato indefinido y sin inversión.')

    return f"""<!DOCTYPE html>
<html lang="es-CL">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)} | VRG Gestión de Recursos</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#0f1d4a">
<link rel="icon" type="image/png" href="../img/favicon.png">
<link rel="apple-touch-icon" href="../img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://images.pexels.com">
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Barlow:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/styles.css">
</head>
<body>

<!-- Página generada por scripts/generar-regiones.py: editar data/regiones.json, no este archivo. -->
<a class="skip" href="#contenido">Saltar al contenido</a>
{cabecera}

<main id="contenido">

<section class="page-hero" style="--img:url('{img_hero}')">
  <div class="wrap">
    <nav class="crumbs" aria-label="Ruta"><a href="../">Inicio</a><span>/</span><a href="../#regiones">Planes</a><span>/</span>{esc(r["corto"])}</nav>
    <p class="eyebrow eyebrow--gold">Plan de campaña {temporada}</p>
    <h1>{esc(r["nombre"])}</h1>
    <p>Condiciones de la campaña de captación de socios cooperadores para Cuerpos y Compañías de Bomberos de la región.</p>
  </div>
</section>

<section class="section plan">
  <div class="wrap">
    <ul class="facts">
      <li class="reveal"><b>30</b><span>días de campaña</span><small>Se extiende a 35 si no se alcanza la meta</small></li>
      <li class="reveal"><b>{primera["compania"]}%</b><span>para tu Compañía</span><small>{esc(primera["periodo"])}: primer aporte</small></li>
      <li class="reveal facts__hl"><b>{final["compania"]}%</b><span>para tu Compañía</span><small>{esc(final["periodo"])}, pagado el día 5 de cada mes</small></li>
      <li class="reveal"><b>∞</b><span>contrato indefinido</span><small>Cláusulas de término en el contrato</small></li>
    </ul>

    <div class="plan__grid">
      <div class="plan__main">
        <p class="eyebrow">Distribución de la recaudación</p>
        <h2>Cómo se reparte lo que se recauda, mes a mes</h2>
        <p>Los primeros meses financian la campaña completa: equipo en terreno, diseño, logística y registro de socios. Por eso tu Compañía no pone un peso. Desde ahí, la mayor parte de cada aporte llega directo a tu institución.</p>
        {nota_rm}
        {tablas}
        <p class="plan__iva">La comisión de mantención incluye IVA: {"14,25% + IVA equivale a cerca del 17%" if final["compania"] == 83 else "16,8% + IVA equivale a cerca del 20%"} de lo recaudado.</p>
      </div>

      <aside class="plan__side">
        <div class="note-card reveal">
          <h3>Información importante</h3>
          <ul>
            <li>Se estima una caída de socios cercana al 6% mensual durante los primeros 6 meses, a partir del segundo mes.</li>
            <li>Recomendamos una nueva campaña desde el mes 13 para consolidar ingresos y aumentar la recaudación total.</li>
            <li>La mantención y fidelización de socios se hace con campañas digitales y telefónicas.</li>
          </ul>
        </div>
        <div class="note-card note-card--red reveal">
          <h3>Tu Compañía aporta</h3>
          <p>Material mayor y voluntarios para la presencia en calle, y las autorizaciones de los puntos de captación acordados entre las partes.</p>
          <a class="btn btn--gold btn--sm" href="../#contacto">Agendar diagnóstico</a>
        </div>
      </aside>
    </div>
  </div>
</section>

<section class="section process">
  <div class="wrap">
    <div class="center reveal">
      <p class="eyebrow">Etapas del proceso</p>
      <h2>De la primera conversación al lanzamiento</h2>
    </div>
    <ol class="process__list">
      <li class="reveal"><h3>Contacto</h3><p>Conversamos con tu Cuerpo o Compañía.</p></li>
      <li class="reveal"><h3>Propuesta</h3><p>Presentamos la propuesta para tu territorio.</p></li>
      <li class="reveal"><h3>Coordinación</h3><p>Reuniones con la institución; al menos una es presencial.</p></li>
      <li class="reveal"><h3>Plan estratégico</h3><p>Plazos, puntos de captación, apoyo de medios locales y fecha de inicio.</p></li>
      <li class="reveal"><h3>Contrato</h3><p>Firma entre la Superintendencia del Cuerpo y VRG Gestión de Recursos SpA.</p></li>
      <li class="reveal"><h3>Lanzamiento</h3><p>Comienza la campaña en terreno.</p></li>
      <li class="reveal"><h3>Fidelización</h3><p>Seguimiento de socios con campañas digitales y telefónicas.</p></li>
    </ol>
  </div>
</section>

<section class="regions section regions--soft">
  <div class="wrap">
    <div class="center reveal">
      <p class="eyebrow">Otras regiones</p>
      <h2>Condiciones de campaña por región</h2>
    </div>
    <div class="regions__grid">{otras}</div>
  </div>
</section>

<section class="cta" style="--img:url('{PEXELS.format(id='11688879', w=1920)}')">
  <div class="wrap cta__in">
    <h2>¿Tu Compañía está en la {esc(r["nombre"])}?<br>Veamos cómo se vería la campaña en tu comuna.</h2>
    <a class="btn btn--gold" href="{esc(wa)}" target="_blank" rel="noopener">Escribir por WhatsApp</a>
  </div>
</section>

</main>
{pie}

</body>
</html>
"""


def main():
    datos = json.loads((RAIZ / "data/regiones.json").read_text(encoding="utf-8"))
    index = (RAIZ / "index.html").read_text(encoding="utf-8")
    cabecera = a_subcarpeta(bloque(index, "<!-- Barra superior -->", "</header>"))
    pie = a_subcarpeta(bloque(index, '<footer class="footer">', "</a>\n\n</body>").replace("\n\n</body>", ""))

    salida = RAIZ / "regiones"
    salida.mkdir(exist_ok=True)
    for r in datos["regiones"]:
        (salida / f'{r["slug"]}.html').write_text(
            pagina(r, datos["regiones"], datos["temporada"], cabecera, pie), encoding="utf-8"
        )
        print("ok", r["slug"])


if __name__ == "__main__":
    main()
