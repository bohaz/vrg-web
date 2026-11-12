# VRG Gestión de Recursos — sitio web (muestra)

Sitio de una sola página para VRG Gestión de Recursos SpA, empresa de captación de socios cooperadores para Bomberos de Chile y fundaciones.

## Estructura

```
index.html        Página única (HTML semántico)
css/styles.css    Estilos; animaciones y menú móvil solo con CSS
img/              Logo, favicon e ícono para móviles
regiones/         Una página por región (generadas, no editar a mano)
data/regiones.json  Condiciones de campaña por región y temporada
scripts/generar-regiones.py  Genera regiones/*.html desde el JSON
```

## Actualizar las condiciones por región

1. Editar `data/regiones.json` (porcentajes por mes, temporada, zonas).
2. Ejecutar `python3 scripts/generar-regiones.py`.
3. Hacer commit de `data/` y `regiones/`.

El encabezado y el pie de las páginas por región se copian de `index.html`, así que un cambio en la navegación se aplica a todas al volver a generar.

## Notas

- Sin JavaScript: el menú móvil usa un checkbox y las animaciones usan `animation-timeline: view()` con respaldo sin animación.
- Fotografías de Pexels (licencia libre), cargadas desde su CDN. Para producción conviene descargarlas y servirlas optimizadas desde `img/`.
- Contenido tomado de vrg.cl y de las publicaciones de @vrg_recaudaciones.

## Despliegue

Sitio estático: se publica tal cual en Vercel (sin comando de build).

---
Desarrollado por [Tu Plan Digital](https://tuplandigital.cl).
