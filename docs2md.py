import os
from sys import flags
import pypandoc # install version with pandoc included
import unicodedata
import re

def docs2md(docs_paths_list, collected_mds_dir):

    # -------------- Verifico que el directorio ded destino existe
    if not os.path.isdir(collected_mds_dir):
        raise Exception("\n\n -> " + __name__ +
                        "(): El directorio destino de markdowns no existe")

    # -------------- Convertimos todos los documentos de la lista
    mds_paths_list = []
    for doc_path in docs_paths_list:
        name = os.path.splitext(os.path.basename(doc_path))[0] # Extraemos el nombre (sin extensión ni path) del doc origen
        output_path = os.path.join(collected_mds_dir, name + ".txt") # Definimos el path del nuevo md generado para este doc
        pypandoc.convert_file(doc_path, 'plain', outputfile=output_path) # Convertimos
        mds_paths_list.append(output_path)
        print(f'-> {__name__}: {name} -> CONVERTED')
        # Normalizamos el archivo a utf-8 y quitamos espacios arriba, abajo y dobles saltos de línea
        # Todo esto para que luego el usuario pueda hacecr las modificaciones manuales más facilmente
        general_nomalization(output_path)


    return mds_paths_list

def general_nomalization(file_path):
    """
    Normaliza los textos previo a la normalización manual. Aquí no se pierden datos
    Esto no debería cambiar mucho con el tiempo
    """
    emojis = ['🍽️', '🍕', '🍺', '🥤', '💵', '📍', '☎️', '⏰', '🚚']
    with open(file_path, 'r+', encoding="utf-8") as f:
        text = f.read()
        text = unicodedata.normalize('NFKD', text) # Normalizamos el tipo de texto
        text = text.strip() # Quitamos espacios y saltos de línea al principio y final
        # Remplazamos texto por emoji en los dos casos dados
        text = re.sub(r' *🍺 ?🥤 *Bebidas *:', '🍺', text) 
        text = re.sub(r' *Maridaje *sugerido *:', '🥤', text)
        # Creamos excedente de saltos de línea antes de los emojis para que luego no se pierdan al quitar saltos de línea excedentes
        for emoji in emojis:
            text = re.sub(rf'^ *{emoji}', f'\n{emoji}', text, flags=re.M)
        # Ajustamos los saltos de línea para que separen secciones
        text = re.sub(r'^\n+', '*------*', text, flags=re.M)
        text = re.sub('\n', ' ', text)
        text = re.sub('\*------\*', '\n', text)
        # Le damos identificador al nombre de cada comida
        text = re.sub(r'\n(.*)\n🍕', r'\n🍽️ \1\n🍕', text)
        # Sobreescribimos el archivo con todo normalizaado
        f.seek(0)
        f.write(text)
        f.truncate()

if __name__ == "__main__":
    general_nomalization('F:\\VReality\\PizzaWeek\\PW_LP_1ra\\TEMP\\mds-010922_003110\\13. Masa.txt')