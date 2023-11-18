#Generate configs from json file containing img_name and target_text
import os
import json
import yaml

def create_yaml_file(json_data, n_timesteps):
    img_name = json_data['img_name']
    target_text = json_data['target_text']
    img_name_without_extension = os.path.splitext(img_name)[0]  # Elimina la extensión del nombre de la imagen
    yaml_filename = f"{img_name_without_extension}__{target_text[:20].replace(' ', '_')}__steps{str(n_timesteps)}.yaml"
    yaml_path = os.path.join("C:/Tesis/pnp-diffusers/config/", yaml_filename)

    data = {
        'seed': 1,
        'device': 'cuda',
        'output_path': f'PNP-results/{img_name_without_extension}_{n_timesteps}',  # Añade el número de pasos al nombre de la imagen
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

    for json_data in json_data_array:
        # Crear YAML con 100 pasos en n_timesteps
        create_yaml_file(json_data, n_timesteps=100)

        # Crear YAML con 50 pasos en n_timesteps
        create_yaml_file(json_data, n_timesteps=50)

if __name__ == "__main__":
    json_filename = "C:/Tesis/imagic-editing.github.io/tedbench/input_list.json"
    process_json_file(json_filename)
