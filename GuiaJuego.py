import os
import sys
import subprocess


def abrir_guia_pdf():
    try:
        # Obtenemos el directorio donde está 'GuiaJuego.py'
        #
        directorio_script = os.path.dirname(os.path.abspath(__file__))
        print(f"DEBUG: Directorio del script: {directorio_script}")

        nombre_carpeta_media = 'Media'
        nombre_pdf = 'Guia del juego.pdf'

        ruta_absoluta_pdf = os.path.join(directorio_script, nombre_carpeta_media, nombre_pdf)

        # Normalizamos la ruta para que sea limpia
        ruta_absoluta_pdf = os.path.normpath(ruta_absoluta_pdf)

        print(f"RUTA FINAL que se intentará abrir: {ruta_absoluta_pdf}")

        if os.path.exists(ruta_absoluta_pdf):
            print("¡ÉXITO! Archivo encontrado. Enviando orden DIRECTA para abrir...")

            if sys.platform == "win32":
                os.startfile(ruta_absoluta_pdf) # En windows

            elif sys.platform == "darwin":
                subprocess.run(["open", ruta_absoluta_pdf]) # En MacOS
            else:
                subprocess.run(["xdg-open", ruta_absoluta_pdf]) # En Linux
        else:
            print(f"--- ERROR: No se encontró el archivo en: {ruta_absoluta_pdf}")
            print("Revisa la ruta que aparece arriba y tu estructura de carpetas.")

    except Exception as e:
        print(f"Error inesperado al intentar abrir el PDF: {e}")