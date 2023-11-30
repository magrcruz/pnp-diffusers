#Generate configs from json file containing img_name and target_text
import os
import json
import yaml

def create_yaml_file(json_data, n_timesteps):
    img_name = json_data['img_name']
    target_text = json_data['target_text']
    img_name_without_extension = os.path.splitext(img_name)[0]  # Elimina la extensión del nombre de la imagen
    yaml_filename = f"{img_name_without_extension}__{target_text[:20].replace(' ', '_')}__steps{str(n_timesteps)}.yaml"
    yaml_path = os.path.join("C:/Tesis/pnp-diffusers/config/"+str(n_timesteps)+"_steps/", yaml_filename)

    data = {
        'seed': 1,
        'device': 'cuda',
        'output_path': f'PNP-results/{n_timesteps}_steps/{img_name_without_extension}',  # Añade el número de pasos al nombre de la imagen
        'image_path': f'C:/Tesis/imagic-editing.github.io/tedbench/originals/{img_name}',
        'latents_path': 'latents_forward',
        'sd_version': '2.1',
        'guidance_scale': 7.5,
        'n_timesteps': n_timesteps,
        'prompt': target_text,
        'negative_prompt': 'realistic',
        'pnp_attn_t': 0.5,
        'pnp_f_t': 0.8
    }

    with open(yaml_path, 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False)

def process_json_file(json_filename):
    with open(json_filename, 'r') as json_file:
        json_data_array = json.load(json_file)

    timeSteps = [50]

    for timeStep in timeSteps:
        folder_path = "C:/Tesis/pnp-diffusers/config/"+str(timeStep)+"_steps/"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f'Se ha creado la carpeta en {folder_path}')
        else:
            print(f'La carpeta {folder_path} ya existe')

        for json_data in json_data_array:
            create_yaml_file(json_data, n_timesteps=timeStep)

if __name__ == "__main__":
    json_filename = "C:/Tesis/imagic-editing.github.io/tedbench/input_list.json"
    process_json_file(json_filename)
