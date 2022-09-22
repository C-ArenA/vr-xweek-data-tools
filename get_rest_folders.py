import os
import logging


def get_rest_folders(origin_files_dir):
    """
    # Recolecta paths de las carpetas de cada restaurante siguiendo la estructura:

    origin_files
    |- 1. Restaurant 1
    |   |- ...
    |   |- *.doc*
    |- 2. Restaurant 2
    |   |- ...
    |   |- *.doc*
    |- 3. Restaurant 3
    |   |- ...
    |   |- *.doc*
    |- 4. Restaurant 4
    |   |- ...
    |   |- *.doc*
    |
    |- ... (rest_folders)
    |- ... (child_dirs | child_folders)

    - Ignora los archivos que no empiecen numerados
    - El número debe estar seguido de un punto y un espacio
    """
    # -------------- Verifico que el directorio de origen exista
    if not os.path.isdir(origin_files_dir):
        raise Exception(__name__ + ": El directorio de origen no existe")

    # ------------- Obtengo la lista de hijos dentro del origin files
    print_origin_files_structure()
    child_dirs = os.listdir(origin_files_dir)
    # ------------- Obtengo sólo las carpetas
    child_folders = list(filter(
        lambda child_dir: os.path.isdir(
            os.path.join(origin_files_dir, child_dir)),
        child_dirs))
    # Obtengo sólo las carpetas que cumplen la condición de estar numeradas con algo como "5. " y asumo que son carpetas de restaurantes
    rest_folders = list(filter(
        lambda folder: (len(folder.split(". ", 1)) > 1),
        child_folders))
    logging.warning(
        f'Encontradas {len(rest_folders)} carpetas de restaurantes:')
    logging.debug(rest_folders)

    return [os.path.join(origin_files_dir, rest_folder) for rest_folder in rest_folders]


def print_origin_files_structure():
    print(f'''-> {__name__}: ANALIZANDO - La estructura del origin_files debe ser para que funcione:

        origin_files
        |- 1. Restaurant 1
        |   |- ...
        |   |- *.doc*
        |- 2. Restaurant 2
        |   |- ...
        |   |- *.doc*
        |- 3. Restaurant 3
        |   |- ...
        |   |- *.doc*
        |- 4. Restaurant 4
        |   |- ...
        |   |- *.doc*
        |
        |- ... (rest_folders)
        |- ... (child_dirs | child_folders)
    ''')
