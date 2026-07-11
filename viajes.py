# viaje_graphhopper_final.py
# Script que mide distancia, duración y narrativa de viaje usando GraphHopper

import requests

API_KEY = "7d96c1ac-81ee-42ec-b670-c4b31f831edd"  # Reemplaza con tu API key de GraphHopper

# Diccionario de ciudades con coordenadas
ciudades = {
    "Santiago": (-33.4489, -70.6693),
    "Valparaíso": (-33.0472, -71.6127),
    "Concepción": (-36.8201, -73.0444),
    "La Serena": (-29.9027, -71.2510),
    "Antofagasta": (-23.6509, -70.3975),
    "Puerto Montt": (-41.4693, -72.9424),
    "Temuco": (-38.7397, -72.5984),
    "Buenos Aires": (-34.6037, -58.3816),
    "Mendoza": (-32.8908, -68.8272),
    "Córdoba": (-31.4201, -64.1888),
    "Rosario": (-32.9587, -60.6930),
    "San Juan": (-31.5375, -68.5364),
    "Salta": (-24.7821, -65.4232),
    "Bariloche": (-41.1335, -71.3103)
}

def calcular_viaje(origen, destino, transporte):
    if origen not in ciudades or destino not in ciudades:
        return "Error: Ciudad no encontrada."

    coord_origen = ciudades[origen]
    coord_destino = ciudades[destino]

    # Si transporte es avión, calculamos directo (sin narrativa)
    if transporte == "avion":
        from geopy.distance import geodesic
        distancia_km = geodesic(coord_origen, coord_destino).kilometers
        distancia_mi = geodesic(coord_origen, coord_destino).miles
        duracion_horas = distancia_km / 800  # velocidad promedio avión
        return f"""
El viaje desde {origen} hasta {destino} en avión cubre {distancia_km:.2f} km ({distancia_mi:.2f} millas).
Duración aproximada: {duracion_horas:.2f} horas.
(No hay narrativa disponible para vuelos)
"""

    # Para auto/bus usamos GraphHopper
    url = (
        f"https://graphhopper.com/api/1/route?"
        f"point={coord_origen[0]},{coord_origen[1]}&"
        f"point={coord_destino[0]},{coord_destino[1]}&"
        f"vehicle=car&locale=es&instructions=true&key={API_KEY}"
    )
    response = requests.get(url)
    data = response.json()

    distancia_km = data["paths"][0]["distance"] / 1000
    distancia_mi = distancia_km * 0.621371
    duracion_horas = data["paths"][0]["time"] / (1000 * 60 * 60)

    narrativa = "\nNarrativa del viaje:\n"
    for paso in data["paths"][0]["instructions"]:
        narrativa += "- " + paso["text"] + "\n"

    return f"""
El viaje desde {origen} hasta {destino} en {transporte} cubre {distancia_km:.2f} km ({distancia_mi:.2f} millas).
Duración aproximada: {duracion_horas:.2f} horas.
{narrativa}
"""

def main():
    while True:
        origen = input("Ingrese Ciudad de Origen (o 's' para salir): ")
        if origen.lower() == "s":
            break
        destino = input("Ingrese Ciudad de Destino (o 's' para salir): ")
        if destino.lower() == "s":
            break
        transporte = input("Ingrese medio de transporte (auto, bus, avion): ")
        print(calcular_viaje(origen, destino, transporte))

if __name__ == "__main__":
    main()
