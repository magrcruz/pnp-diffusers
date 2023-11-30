import argparse
import os
import pandas as pd
import subprocess
from tqdm import tqdm
import time

def procesar_filas(csv_path, col_name, images_file_prefix, pausa_entre_iteraciones):
    # Cargar el DataFrame desde el archivo CSV
    df = pd.read_csv(csv_path)

    # Iterar sobre las filas y ejecutar el comando preprocess.py
    for _, fila in tqdm(df.iterrows(), total=len(df), desc="Procesando filas"):
        data_path = os.path.join(images_file_prefix, fila['img'])
        inversion_prompt = fila[col_name]

        # Construir el comando preprocess.py
        comando = [
            "python", "preprocess.py",
            "--data_path", data_path,
            "--inversion_prompt", inversion_prompt
        ]

        subprocess.run(comando)

        # Introducir una pausa si se especifica
        if pausa_entre_iteraciones:
            time.sleep(60) #60 segundos

if __name__ == "__main__":
    # Configurar los argumentos de línea de comandos
    parser = argparse.ArgumentParser(description="Procesar un archivo CSV y ejecutar preprocess.py para cada fila.")
    parser.add_argument("--input", required=True, help="Ruta al archivo CSV de entrada.")
    parser.add_argument("--col", required=True, help="Nombre de la columna a utilizar como inversion prompt.")
    parser.add_argument("--images_file", required=True, help="Prefijo a agregar al data_path.")
    parser.add_argument("--pausa", action="store_true", help="Incluir una pausa entre iteraciones.")

    # Analizar los argumentos de línea de comandos
    args = parser.parse_args()

    # Llamar a la función para procesar filas
    procesar_filas(args.input, args.col, args.images_file, args.pausa)

#python run_preprocess.py --input tu_archivo.csv --col tu_columna --images_file ruta/a/tu/carpeta_de_imagenes/ --pausa
#python run_preprocess.py --input C:\Tesis\Metrics-Image-Edition-with-Natural-Language\captionings.csv --col blip2 --images_file C:\Tesis\imagic-editing.github.io\tedbench\originals --pausa
