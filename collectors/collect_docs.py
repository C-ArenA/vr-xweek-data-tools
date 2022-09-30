from email import message
import os  # For OS operations
import glob
import shutil  # To make operations on many files (os on steroids)


def collect_docs(rest_folders_paths: list, collected_docs_dir: str, delete_old: bool = True) -> list:
    """
    # Recolecta documentos word en una carpeta

    La creación de la carpeta no depende de esta función y si no existe se retorna un error
        Si el parámetro delete_old es True se borra el contenido anterior de la carpeta de destino (si existe)



        Retorna un objeto con dos listas:
        docs path antiguo
        docs path nuevo
    """

    # -------------- Verifico que el directorio de destino existe
    if not os.path.isdir(collected_docs_dir):
        raise Exception("\n\n -> " + __name__ +
                        "(): El directorio destino no existe")

    # -------------- Borro contenido anterior de la carpeta destino si delete_old es True
    if delete_old:
        print(__name__ + ": Borrando archivos de carpeta destino: " +
              collected_docs_dir)
        old_files = os.listdir(collected_docs_dir)
        for old_file in old_files:
            old_file_path = os.path.join(collected_docs_dir, old_file)
            if os.path.isfile(old_file_path):
                os.remove(old_file_path)

    docs_old_paths = []  # Acumulador de paths de docs originales
    docs_new_paths = []  # Acumulador de paths de docs viejos

    # ------------- Busco archivos doc* dentro de las carpetas de los restaurantes
    for rest_folder_path in rest_folders_paths:
        # glob devuelve el path completo, no solo el nombre
        docs_inside = glob.glob(os.path.join(rest_folder_path, "*.doc*"))
        # --------- Copio los doc* encontrados
        for doc in docs_inside:
            docs_old_paths.append(doc)
            new_doc_path = os.path.join(
                collected_docs_dir, os.path.basename(doc))
            docs_new_paths.append(new_doc_path)
            # ----- Copiando
            print(f'{__name__}: Copiando: {doc} -----> {new_doc_path}')
            shutil.copy(doc, collected_docs_dir)

    return {
        "docs_old_paths": docs_old_paths,
        "docs_new_paths": docs_new_paths
    }


def find_docs_in_folder(folder: str) -> list:
    """Encuentro recursivamente todos los documentos de word dentro de una carpeta y sus subcarpetas

    Args:
        folder (str): Carpeta dentro de la cual se buscará de forma recursiva

    Returns:
        list: Lista de documentos encontrados. Cada item es un objeto de tipo:
            {"path": El path completo del documento encontrado,
            "file": Nombre completo del archivo
            "name": Nombre del archivo sin extensión,
            "ext": Extensión del archivo}
    """
    found_docs = []  # Acumulador de docs encontrados
    # ------------- Busco archivos doc* dentro de las carpetas de los restaurantes
    for dir_file in os.listdir(folder):
        if os.path.isdir(os.path.join(folder,dir_file)):
            found_docs += find_docs_in_folder(os.path.join(folder, dir_file))
        elif os.path.isfile(os.path.join(folder,dir_file)):
            file_name, file_ext = os.path.splitext(dir_file)
            if file_ext[:4] == ".doc":
                found_docs.append({"path": os.path.join(
                    folder, dir_file), "file": dir_file, "name": file_name, "ext": file_ext})
        else:
            pass
    return found_docs


def find_docs_in_folder_ui_wrapper():
    from InquirerPy import inquirer, get_style, validator
    from InquirerPy.base.control import Choice
    style = get_style({"questionmark": "#ff3355", "answer": "#0055ff"}, style_override=False)
    print("Este es el asistente para encontrar los archivos word dentro de una carpeta")
    src_path = inquirer.filepath(
        message="Dentro de qué carpeta desea buscar los archivos de word (Puede arrastrar y soltar):",
        only_directories=True
    ).execute()
    found_docs = find_docs_in_folder(src_path)
    accepted_docs = []
    print(f'Se encontraron {len(found_docs)} documentos de word dentro de la carpeta {src_path}\n')
    if len(found_docs) > 0:
        
        print(f'A continuación deseleccione los documentos que están por demás (con tecla espacio), deje seleccionados los demás\n')
        
        accepted_docs = inquirer.checkbox(
            message="Deseleccione docs innecesarios:",
            choices=[Choice(doc, name=doc["file"], enabled=True) for doc in found_docs]
        ).execute()
    
    extradoc = inquirer.confirm(
        message="Desea ingresar doc extra manualmente?"
    ).execute()
    while extradoc:
        new_file = inquirer.filepath(
            message="Ingrese doc extra manualmente (Puede arrastrar):",
            only_files=True,
        ).execute()
        file_name, file_ext = os.path.splitext(new_file)
        if file_ext[:4] == ".doc":
            accepted_docs.append({
                "path": new_file,
                "file": os.path.basename(new_file),
                "name": file_name,
                "ext": file_ext
            })
        else:
            print("El archivo no es de tipo documento de word, no se acepta\n")
        extradoc = inquirer.confirm(
            message="Desea ingresar otro doc extra manualmente?"
        ).execute()
    print("Los documentos encontrados finales son:\n")
    for doc in accepted_docs:
        print(doc["path"])
    return accepted_docs

def collect_docs_with_help():
    """
    # Recolecta documentos word en una carpeta

    Retorna un objeto con dos listas:
    docs path antiguo
    docs path nuevo
    """
    pass
    # Recibo el directorio dentro del cual debo buscar archivos de word
    # Verifico que sea correcto
    # Recolecto una lista de todos los documentos de Word encontrados
    # Le indico al usuario cuántos hay
    # Le pido al usuario que haga check en los documentos que son menús de restaurantes
    # Le pido al usuario el directorio de destino (Le recomiendo uno)
    # Le indico el resultado y el enlace a la carpeta donde están los archivos de Word


if __name__ == "__main__":
    find_docs_in_folder_ui_wrapper()
