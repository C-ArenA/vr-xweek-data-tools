def collect_docs(rest_folders_paths: list, collected_docs_dir: str, delete_old: bool = True) -> list:
    """
    # Recolecta documentos word en una carpeta

    La creación de la carpeta no depende de esta función y si no existe se retorna un error
        Si el parámetro delete_old es True se borra el contenido anterior de la carpeta de destino (si existe)

    

        Retorna un objeto con dos listas:
        docs path antiguo
        docs path nuevo
    """

    import os  # For OS operations
    import glob
    import shutil  # To make operations on many files (os on steroids)
    from slugify import slugify

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

    
    docs_old_paths = [] # Acumulador de paths de docs originales
    docs_new_paths = [] # Acumulador de paths de docs viejos
    
    # ------------- Busco archivos doc* dentro de las carpetas de los restaurantes 
    for rest_folder_path in rest_folders_paths:
        docs_inside = glob.glob(os.path.join(rest_folder_path, "*.doc*")) # glob devuelve el path completo, no solo el nombre
        # --------- Copio los doc* encontrados
        for doc in docs_inside:
            docs_old_paths.append(doc)
            new_doc_path = os.path.join(collected_docs_dir, os.path.basename(doc))
            docs_new_paths.append(new_doc_path)
            # ----- Copiando
            print(f'{__name__}: Copiando: {doc} -----> {new_doc_path}')
            shutil.copy(doc, collected_docs_dir)
    
    return {
        "docs_old_paths": docs_old_paths,
        "docs_new_paths": docs_new_paths
    }

def collect_docs_with_help():
    """
    # Recolecta documentos word en una carpeta
	
	Retorna un objeto con dos listas:
	docs path antiguo
	docs path nuevo
    """
    # Recibo el directorio dentro del cual debo buscar archivos de word
    # Verifico que sea correcto
    # Recolecto una lista de todos los documentos de Word encontrados
    # Le indico al usuario cuántos hay
    # Le pido al usuario que haga check en los documentos que son menús de restaurantes
    # Le pido al usuario el directorio de destino (Le recomiendo uno)
    # Le indico el resultado y el enlace a la carpeta donde están los archivos de Word
    
       
if __name__ == "__main__":
	pass