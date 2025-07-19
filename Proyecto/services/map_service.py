# services/map_service.py

import folium
import pathlib
from models.ubicacion_para_mapa import obtener_ubicaciones, obtener_eventos_activos

def generar_mapa():
    # 1. Crear el mapa centrado en el campus UNAL Bogotá
    mapa = folium.Map(
        location=[4.636207, -74.083201],  # coordenadas aproximadas de la UN
        zoom_start=16,
        tiles='cartodbpositron'
    )

    # 2. Obtener ubicaciones desde la base de datos
    ubicaciones = obtener_ubicaciones()

    for ubic in ubicaciones:
        lat, lon = map(float, ubic["coordenadas"].split(","))  # ej: "4.63,-74.08"

        # Obtener eventos activos para esta ubicación
        eventos = obtener_eventos_activos(ubic["id_ubicacion"])
        if eventos:
            listado = "<ul>" + "".join(f"<li>{e['titulo']}</li>" for e in eventos) + "</ul>"
            popup_html = f"<b>{ubic['nombre']}</b>{listado}"
        else:
            popup_html = f"<b>{ubic['nombre']}</b><br>Sin eventos activos"

        # Agregar marcador
        folium.CircleMarker(
            location=[lat, lon],
            radius=7,
            color='blue',
            fill=True,
            fill_color='lightblue',
            fill_opacity=0.8,
            tooltip=ubic['nombre'],
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(mapa)

    # 3. Guardar el mapa en la carpeta web/
    ruta_output = pathlib.Path(__file__).parent.parent / "web" / "map.html"
    mapa.save(str(ruta_output))

    return ruta_output
