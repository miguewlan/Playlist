# Playlist Creator App

Esta aplicación permite automatizar y personalizar la creación de playlists de Spotify, integrando un backend en Python (FastAPI) y un frontend en React. Además, gestiona imágenes de artistas y permite la creación de playlists tanto manual como automáticamente.

## Funcionalidades principales

- **Creación de playlists en Spotify**: Puedes crear playlists de forma manual (seleccionando artista y canciones) o automática (para varios artistas a la vez) desde el frontend.
- **Gestión de imágenes de artistas**:
  - Las imágenes subidas desde el frontend se guardan en la carpeta `images/` y se registran en la base de datos SQLite.
  - La lista de artistas e imágenes se gestiona dinámicamente a través del archivo `imagenes.json`.
- **Integración full-stack**:
  - El backend expone endpoints para crear playlists y subir imágenes.
  - El frontend permite subir imágenes, seleccionar artistas y crear playlists con una interfaz amigable.
- **Validación y robustez**:
  - El sistema evita crear playlists si no hay canciones encontradas para un artista, previniendo errores con la API de Spotify.
  - La lógica de artistas e imágenes es dinámica: cualquier cambio en `imagenes.json` se refleja automáticamente en la app.
- **Base de datos**:
  - Se utiliza SQLite para registrar las imágenes subidas y asociarlas con los artistas.
- **Actualización automática**:
  - Al subir una nueva imagen, se actualiza automáticamente el archivo `imagenes.json` y la base de datos.

## Estructura del proyecto

- `backend/`
  - `main.py`: Lógica principal para crear playlists, lee artistas desde `imagenes.json`.
  - `image_service.py`: Lógica para guardar imágenes, actualizar `imagenes.json` y registrar en la base de datos.
  - `imagenes.json`: Lista dinámica de artistas e imágenes.
  - `images.db`: Base de datos SQLite para registrar imágenes.
  - `images/`: Carpeta donde se almacenan las imágenes de los artistas.
  - `app.py`: Endpoints de la API (FastAPI).
- `frontend/`
  - `src/App.js`: Interfaz para subir imágenes y crear playlists.
- Archivos de imágenes de artistas en la raíz o en la carpeta `images/`.

## Cómo funciona

1. **Subida de imágenes**: Desde el frontend, puedes subir una imagen y asociarla a un artista. Esto actualiza la base de datos y el archivo `imagenes.json`.
2. **Creación de playlists**:
   - Manual: Selecciona un artista y crea una playlist con sus canciones.
   - Automática: Crea playlists para todos los artistas listados en `imagenes.json`.
3. **Gestión dinámica**: La lista de artistas e imágenes se actualiza automáticamente al subir nuevas imágenes.
4. **Prevención de errores**: El backend valida que existan canciones antes de crear una playlist, evitando errores con la API de Spotify.

## Tecnologías utilizadas

- **Backend**: Python, FastAPI, Spotipy, SQLite, JSON
- **Frontend**: React
- **Otros**: dotenv, pathlib, shutil

## Requisitos

- Cuenta de Spotify y credenciales de API
- Python 3.x
- Node.js y npm para el frontend

## Instalación y uso

### 1. Clona el repositorio

```bash
git clone <URL-del-repositorio>
cd Playlist
```

### 2. Configura el entorno del backend

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Crea un archivo `.env` en la carpeta `backend/` con tus credenciales de Spotify:

```
SPOTIPY_CLIENT_ID=tu_client_id
SPOTIPY_CLIENT_SECRET=tu_client_secret
SPOTIPY_REDIRECT_URI=tu_redirect_uri
```

### 3. Inicia el backend

```bash
uvicorn app:app --reload
```

### 4. Configura e inicia el frontend

```bash
cd frontend
npm install
npm start
```

### 5. Uso

- Accede al frontend en tu navegador (usualmente en http://localhost:3000).
- Sube imágenes de artistas y crea playlists manual o automáticamente.

---

¿Dudas o sugerencias? ¡Contribuye o abre un issue!
# playlist
