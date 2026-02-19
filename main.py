import spotipy
from spotipy.oauth2 import SpotifyOAuth
import base64
import os
from dotenv import load_dotenv
import random
from pathlib import Path

import schedule
import time


# Arreglo con los nombres de las imágenes (sin extensión)
imagenes = [
    "Alejandro Fernandez",
    "Camilo Sesto",
    "Chayanne",
    "Christian Nodal",
    "Cristian Castro",
    "Dinamicos Jr",
    "Diomedez Diaz",
    "El Fantasma",
    "El Frizian",
    "El Jincho",
    "Galy Galiano",
    "Grupo Frontera",
    "Ivan Cornejo",
    "Jasiel Nunez",
    "Julion Alvarez",
    "Junior H",
    "Karol G",
    "La Adictiva",
    "Liberación",
    "Los Angeles Azules",
    "Los Askis",
    "Los Cadiz",
    "Los Tucanes De Tijuana",
    "Luis Alfonso",
    "Marco Antonio Solis",
    "Natanael Cano",
    "Omar Camacho",
    "Oscar Maydon",
    "Panter Belico",
    "Pepe Aguilar",
    "Pesado",
    "Peso Pluma",
    "Ricky Martin",
    "Selena",
    "Silvestre Dangond",
    "Tito Double P",
    "Valentin Elizalde",
    "Victor Mendivil",
    "Xavi"
]


# Cargar variables desde .env
# Los valores están definidos directamente aquí según el orden proporcionado
SPOTIPY_CLIENT_ID = "4b10fefe1c2147368a67f66c32c15763"
SPOTIPY_CLIENT_SECRET = "590dfa0dcef24b5993d6607dc268ce93"
SPOTIPY_REDIRECT_URI = "https://www.google.com/"

# Verificar credenciales
if not all([SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI]):
    print("Error: Configura las credenciales en el archivo .env")
    exit()

# Autenticación con Spotify
scope = "playlist-modify-public playlist-modify-private user-library-read ugc-image-upload user-read-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope
))




# Obtener el país del usuario para búsquedas regionales
user_country = sp.current_user().get('country', 'US')

# Iterar sobre el arreglo de cantantes y crear una playlist para cada uno
def get_artist_tracks(artist_id, artist_name, country='US', num_tracks=50):
    """Obtiene hasta 50 canciones del artista combinando métodos"""
    # Obtener top 10 canciones
    top_tracks = sp.artist_top_tracks(artist_id, country=country)['tracks']
    track_uris = [track['uri'] for track in top_tracks]
    # Si necesitamos más canciones
    if len(track_uris) < num_tracks:
        # Buscar más canciones del artista
        search_query = f"artist:{artist_name}"
        results = sp.search(
            q=search_query,
            type='track',
            limit=50,
            market=country
        )
        # Filtrar canciones del artista principal
        for track in results['tracks']['items']:
            if len(track_uris) >= num_tracks:
                break
            if track['artists'][0]['id'] == artist_id and track['uri'] not in track_uris:
                track_uris.append(track['uri'])
    return track_uris[:num_tracks]

# Índice global para recorrer el arreglo de imagenes
current_index = 0

def crear_playlist_programada():
    global current_index
    if not imagenes:
        print("No hay nombres en el arreglo de imagenes.")
        return
    artist_name = imagenes[current_index]
    print(f"\nProcesando artista: {artist_name}")
    # Buscar el artista en Spotify
    results = sp.search(q='artist:' + artist_name, type='artist', limit=1)
    if not results['artists']['items']:
        print(f"\n❌ Error: No se encontró el artista '{artist_name}' en Spotify")
        current_index = (current_index + 1) % len(imagenes)
        return
    artist = results['artists']['items'][0]
    print(f"\n✅ Artista encontrado: {artist['name']}")

    # Obtener las canciones
    track_uris = get_artist_tracks(artist['id'], artist['name'], user_country, 50)

    # Crear nombre para la playlist
    playlist_name = f"{artist['name']} Éxitos de {artist['name']} MIX Mejores canciones de {artist['name']}"

    # Obtener ID del usuario actual
    user_id = sp.current_user()['id']

    # Crear la playlist
    playlist = sp.user_playlist_create(
        user=user_id,
        name=playlist_name,
        public=True,
        description=f"{artist['name']} Éxitos de {artist['name']} MIX Mejores canciones de {artist['name']}"
    )
    playlist_id = playlist['id']
    playlist_url = playlist['external_urls']['spotify']

    print(f"\n✅ Playlist creada: {playlist_name}")
    print(f"🔗 URL: {playlist_url}")


    # Agregar canciones a la playlist
    sp.playlist_add_items(playlist_id, track_uris)

    # Obtener nombres de las canciones agregadas
    track_names = []
    for uri in track_uris:
        track = sp.track(uri)
        track_names.append(track['name'])
    # Crear la descripción separada por comas
    descripcion = ", ".join(track_names)
    # Actualizar la descripción de la playlist
    sp.playlist_change_details(playlist_id, description=descripcion)

    # Agregar tracks extra proporcionados por el usuario en posiciones específicas
    extra_tracks = [
        "4egu0b0FJ09sYRHqnLXh1D",
        "1LuqDROKgJ5hKwnr2D84xF",
        "2oWDhLeOeJMkKlQpehIDov",
        "4b4sxbyErmhiSopyqsmNmL",
        "49K3n4e6T9JUxfb7wJXN8Y",
        "0k7tT63LtxjBLMS3YKl0wh"
    ]
    posiciones = [5, 7, 9, 12, 15, 17]
    for track, pos in zip(extra_tracks, posiciones):
        try:
            sp.playlist_add_items(playlist_id, [track], position=pos)
        except Exception as e:
            print(f"Error al agregar el track extra {track} en la posición {pos}: {e}")
    print(f"🎵 Se agregaron {len(track_uris)} canciones a la playlist y los tracks extra en posiciones específicas")


    # Buscar imagen del artista en el mismo directorio
    SCRIPT_DIR = Path(__file__).parent
    IMAGE_PATH = SCRIPT_DIR / f"{artist_name}.jpg"

    # Si no encuentra la imagen exacta, intentar con formato insensible a mayúsculas
    if not IMAGE_PATH.exists():
        matching_images = list(SCRIPT_DIR.glob(f"{artist_name}.*"))
        if not matching_images:
            matching_images = list(SCRIPT_DIR.glob(f"{artist_name.lower()}.*"))
            if not matching_images:
                matching_images = list(SCRIPT_DIR.glob(f"{artist_name.upper()}.*"))
        if matching_images:
            IMAGE_PATH = matching_images[0]
            print(f"ℹ️ Se encontró la imagen: {IMAGE_PATH.name}")
        else:
            print(f"\n⚠️ Advertencia: No se encontró imagen para '{artist_name}.jpg'")
            print("Se creó la playlist sin imagen de portada")
            IMAGE_PATH = None

    # Procesar y subir la imagen si existe
    if IMAGE_PATH and IMAGE_PATH.exists():
        try:
            with open(IMAGE_PATH, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            sp.playlist_upload_cover_image(playlist_id, encoded_image)
            print(f"\n🖼️ ¡Imagen '{IMAGE_PATH.name}' asignada como portada!")
        except Exception as e:
            print(f"\n❌ Error al subir la imagen: {e}")

    # Avanzar al siguiente artista
    current_index = (current_index + 1) % len(imagenes)



# Pedir al usuario cuántas veces ejecutar la función
veces = int(input("¿Cuántas playlists quieres crear? "))
print(f"Se crearán {veces} playlists, una tras otra.")
for _ in range(veces):
    crear_playlist_programada()

def crear_playlist_para_artista(artist_name, num_tracks=50):
    # Buscar el artista en Spotify
    results = sp.search(q='artist:' + artist_name, type='artist', limit=1)
    if not results['artists']['items']:
        return {"status": "error", "message": f"No se encontró el artista '{artist_name}' en Spotify"}
    artist = results['artists']['items'][0]

    # Obtener las canciones
    track_uris = get_artist_tracks(artist['id'], artist['name'], user_country, num_tracks)

    # Crear nombre para la playlist
    playlist_name = f"{artist['name']} Éxitos de {artist['name']} MIX Mejores canciones de {artist['name']}"

    # Obtener ID del usuario actual
    user_id = sp.current_user()['id']

    # Crear la playlist
    playlist = sp.user_playlist_create(
        user=user_id,
        name=playlist_name,
        public=True,
        description=f"{artist['name']} Éxitos de {artist['name']} MIX Mejores canciones de {artist['name']}"
    )
    playlist_id = playlist['id']
    playlist_url = playlist['external_urls']['spotify']

    # Agregar canciones a la playlist
    sp.playlist_add_items(playlist_id, track_uris)

    # Agregar tracks extra proporcionados por el usuario en posiciones específicas
    extra_tracks = [
        "4egu0b0FJ09sYRHqnLXh1D",
        "1LuqDROKgJ5hKwnr2D84xF",
        "2oWDhLeOeJMkKlQpehIDov",
        "4b4sxbyErmhiSopyqsmNmL",
        "49K3n4e6T9JUxfb7wJXN8Y",
        "0k7tT63LtxjBLMS3YKl0wh"
    ]
    posiciones = [5, 7, 9, 12, 15, 17]
    for track, pos in zip(extra_tracks, posiciones):
        try:
            sp.playlist_add_items(playlist_id, [track], position=pos)
        except Exception as e:
            pass  # No interrumpir el flujo

    # Buscar imagen del artista en el mismo directorio
    SCRIPT_DIR = Path(__file__).parent
    IMAGE_PATH = SCRIPT_DIR / f"{artist_name}.jpg"
    if not IMAGE_PATH.exists():
        matching_images = list(SCRIPT_DIR.glob(f"{artist_name}.*"))
        if not matching_images:
            matching_images = list(SCRIPT_DIR.glob(f"{artist_name.lower()}.*"))
            if not matching_images:
                matching_images = list(SCRIPT_DIR.glob(f"{artist_name.upper()}.*"))
        if matching_images:
            IMAGE_PATH = matching_images[0]
    if IMAGE_PATH.exists():
        try:
            with open(IMAGE_PATH, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            sp.playlist_upload_cover_image(playlist_id, encoded_image)
        except Exception as e:
            pass
    return {"status": "success", "playlist_url": playlist_url, "playlist_name": playlist_name}

