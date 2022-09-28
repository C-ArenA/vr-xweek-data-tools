from posixpath import basename


def collect_images(event_version, rest_folders_paths: list, collected_imgs_dir: str, delete_old: bool = True, extension: str = "jpg") -> list:
    """
    # Recolecta imágenes en una carpeta

    La creación de la carpeta no depende de esta función y si no existe se retorna un error
        Si el parámetro delete_old es True se borra el contenido anterior de la carpeta de destino (si existe)



    Retorna un objeto con dos listas:
        imgs path antiguo
        imgs path nuevo
    """

    import os  # For OS operations
    import glob
    import shutil  # To make operations on many files (os on steroids)
    from slugify import slugify

    # -------------- Verifico que el directorio de destino existe
    if not os.path.isdir(collected_imgs_dir):
        raise Exception("\n\n -> " + __name__ +
                        "(): El directorio destino no existe")

    # -------------- Borro contenido anterior de la carpeta destino si delete_old es True
    if delete_old:
        print(__name__ + ": Borrando archivos de carpeta destino: " +
              collected_imgs_dir)
        old_files = os.listdir(collected_imgs_dir)
        for old_file in old_files:
            old_file_path = os.path.join(collected_imgs_dir, old_file)
            if os.path.isfile(old_file_path):
                os.remove(old_file_path)

    imgs_old_paths = []  # Acumulador de paths de imgs originales
    imgs_new_paths = []  # Acumulador de paths de imgs viejos

    # ------------- Busco archivos img* dentro de las carpetas de los restaurantes
    for rest_folder_path in rest_folders_paths:
        # glob devuelve el path completo, no solo el nombre
        imgs_inside = glob.glob(os.path.join(
            rest_folder_path, "*." + extension))
        # --------- Copio los img* encontrados
        for img in imgs_inside:
            imgs_old_paths.append(img)
            old_image_name, old_image_ext = os.path.splitext(os.path.basename(img))
            new_img_name = slugify(os.path.basename(rest_folder_path)) + "_" + event_version + slugify(old_image_name) + old_image_ext
            new_img_path = os.path.join(collected_imgs_dir, new_img_name)
            imgs_new_paths.append(new_img_path)
            # ----- Copiando
            print(f'{__name__}: Copiando: {img} -----> {new_img_path}')
            shutil.copy(img, new_img_path)

    return {
        "imgs_old_paths": imgs_old_paths,
        "imgs_new_paths": imgs_new_paths
    }
