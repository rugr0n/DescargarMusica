# By rugron ^^

import tkinter as tk
from pytube import YouTube, Playlist
import spotdl
import scdl
import re
import os
import subprocess

# La carpeta donde iran las canciones
output_path = r'C:\Users\W10\Music\edits' #CAMBIA LA DIRECCION QUE ESTA ENTRE LAS COMILLAS SIMPLES

def obtener_nombre_valido(url):
    # Utilizar expresión regular para eliminar caracteres no permitidos
    nombre_valido = re.sub(r'[\/:*?"<>|]', '_', url)
    return nombre_valido

# Función para descargar el audio en MP3 de alta calidad
def descargar():
    url = url_entry.get()
    
    try:
        if 'playlist' in url:
            if 'spotify' in url:
                # Si es una URL de lista de reproducción de Spotify, descargar la lista completa
                playlist_id = url.split('/')[-1]
                playlist_folder = os.path.join(output_path, obtener_nombre_valido(playlist_id))
                
                # Cambiar el nombre si la carpeta ya existe
                while os.path.exists(playlist_folder):
                    playlist_id += "_duplicate"
                    playlist_folder = os.path.join(output_path, obtener_nombre_valido(playlist_id))
                
                os.makedirs(playlist_folder)
                
                command = ['spotdl', url, '--output', playlist_folder]
                subprocess.run(command, check=True)
            elif 'youtube.com' in url:
                # Si es una URL de lista de reproducción de YouTube, descargar la lista completa
                playlist_id = url.split('=')[-1]
                playlist_folder = os.path.join(output_path, obtener_nombre_valido(playlist_id))
                
                # Cambiar el nombre si la carpeta ya existe
                while os.path.exists(playlist_folder):
                    playlist_id += "_duplicate"
                    playlist_folder = os.path.join(output_path, obtener_nombre_valido(playlist_id))
                
                os.makedirs(playlist_folder)
                
                pl = Playlist(url)  # Crear la lista de reproducción
                for video_url in pl.video_urls:
                    yt = YouTube(video_url)
                    video_title = obtener_nombre_valido(yt.title)
                    audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
                    audio_stream.download(output_path=playlist_folder, filename=f'{video_title}.mp3')
            elif 'soundcloud.com' in url:
                # Si es una lista de reproducción de SoundCloud, descargar la lista completa
                command = ['scdl', '-l', url, '--path', output_path]
                subprocess.run(command, check=True)
        else:
            if 'spotify' in url:
                # Si es una URL o nombre de canción de Spotify, descargar la canción correspondiente
                command = ['spotdl', url, '--output', output_path]
                subprocess.run(command, check=True)
            elif 'soundcloud.com' in url:
                # Si es una URL o nombre de canción de SoundCloud, descargar la canción correspondiente
                command = ['scdl', '-l', url, '--path', output_path]
                subprocess.run(command, check=True)
            else:
                # Si es un URL o nombre de canción de Youtube, descargar la canción correspondiente
                yt = YouTube(url)
                video_title = obtener_nombre_valido(yt.title)
                audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
                audio_stream.download(output_path=output_path, filename=f'{video_title}.mp3')
        
        status_label.config(text='Descarga completada')
    except Exception as e:
        status_label.config(text=f'Error: {str(e)}')

#Crear la interfaz del codigo con tkinter
window = tk.Tk()
window.title("Descargador de Música")
window.geometry("400x200")  # Establece el tamaño de la ventana

# Personaliza colores y fuentes
window.configure(bg="#f2f2f2")  # Cambia el color de fondo
font_style = ("Helvetica", 12)  # Establece la fuente y el tamaño

# Etiqueta y entrada para la URL del video o lista de reproducción
url_label = tk.Label(window, text="URL del video o lista de reproducción:", font=font_style, bg="#f2f2f2")
url_label.pack()
url_entry = tk.Entry(window, font=font_style)
url_entry.pack()

# Botón para iniciar la descarga
download_button = tk.Button(window, text="Descargar", command=descargar, font=font_style, bg="#4CAF50", fg="white")
download_button.pack()

# Etiqueta para mostrar el estado de la descarga
status_label = tk.Label(window, text="", font=font_style, bg="#f2f2f2")
status_label.pack()

window.mainloop()