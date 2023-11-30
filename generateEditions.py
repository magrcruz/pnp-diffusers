#Run all editions in config folders, if latents do not exits preprocess the image
import os
import subprocess
import time
from tqdm import tqdm
import yaml
import logging

# Configurar el sistema de registro
logging.basicConfig(filename='tiempos_procesamiento200.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def check_and_create_latents_folder(image_path):
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    latents_folder_path = os.path.join("latents_forward", image_name)

    if not os.path.exists(latents_folder_path):
        print(f"Carpeta latents para {image_name} no encontrada. Ejecutando preprocess.py...")
        start_time = time.time()
        subprocess.run(["python", "preprocess.py", "--data_path", image_path])
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Registrar el tiempo en el archivo de registro
        logging.info(f"Preprocesamiento: {latents_folder_path}, Tiempo de inversion: {elapsed_time:.2f} segundos")
        time.sleep(120)
    else:
        print(f"Carpeta latents para {image_name} encontrada.")

def run_pnp_with_config(config_path):
    print(f"Ejecutando pnp.py con el archivo de configuración: {config_path}")
    subprocess.run(["python", "pnp.py", "--config_path", config_path])

def process_yaml_file(yaml_file):
    config_path = os.path.join(config_folder, yaml_file)

    # Extraer la ruta de la imagen del archivo YAML
    with open(config_path, 'r') as yaml_file:
        yaml_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
        image_path = yaml_data.get('image_path', '')

    if image_path:
        #check_and_create_latents_folder(image_path)

        start_time = time.time()
        run_pnp_with_config(config_path)
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Registrar el tiempo en el archivo de registro
        logging.info(f"Archivo YAML: {yaml_file}, Tiempo de edicion: {elapsed_time:.2f} segundos")

        # Evitar sobrecalentamiento
        if (yaml_data.get('iterations', 0) + 1) % 5 == 0:
            print("Dejando descansar la computadora")
            time.sleep(30)
            if (yaml_data.get('iterations', 0) + 1) % 10 == 0:
                time.sleep(120)
    

def main():
    # Lista de archivos YAML en la carpeta de configuración
    yaml_files = [file for file in os.listdir(config_folder) if file.endswith(".yaml")]

    for i, yaml_file in enumerate(tqdm(yaml_files, desc="Progreso")):
        process_yaml_file(yaml_file)

if __name__ == "__main__":
    # Carpeta de configuración
    config_folder = "C:/Tesis/pnp-diffusers/config/200_steps"

    # Ejecutar el programa principal
    main()
