import os
from pathlib import Path
from sys import flags
import pypandoc # install version with pandoc included
import unicodedata
import re

# Dict con las reglas de normalización del txt antes de ser mostrado al usuario
# Debe tener pares regex_exp - string
prenormalization_rules = {
    
}

def docs2txt(docs_paths_list: list[Path], collected_txts_dir: Path) -> list[Path]:
    """Convierte una lista de docs a txt y los guarda en una carpeta especificada

    Args:
        docs_paths_list (list[Path]): Lista de Paths de archivos .doc*
        collected_txts_dir (Path): Path del directorio donde se guardaran los txts

    Raises:
        FileNotFoundError: Si el directorio de destino no existe
        NotADirectoryError: Si el directorio de destino no es un directorio válido

    Returns:
        list[Path]: Lista de Paths de los txts generados
    """
    # -------------- Verifico que el directorio de destino existe
    if not collected_txts_dir.exists():
        raise FileNotFoundError("\n-> " + __name__ +
                        "(): El directorio destino de txts no existe")
    # -------------- Verifico que el directorio de destino es un directorio válido
    if not collected_txts_dir.is_dir():
        raise NotADirectoryError("\n-> " + __name__ +
                        "(): El directorio destino de txts no es un directorio válido")
    
    

    # -------------- Convertimos todos los documentos de la lista
    txts_paths_list = []
    for doc_path in docs_paths_list:
        # NOTE: name = stem + suffix (Over final path component)
        output_path = collected_txts_dir.joinpath(doc_path.stem + ".txt")
        output_path = collected_txts_dir.joinpath(doc_path.name).with_suffix(".txt")
        # Aparently, pypandoc uses the old path management system of Python, so we will not sen our Path object
        pypandoc.convert_file(str(doc_path.absolute()), 'plain', outputfile=str(output_path.absolute())) # Convertimos
        print(f'-> {__name__}: {doc_path.name} -> CONVERTED to .txt')
        txts_paths_list.append(output_path)
        # Normalizamos el archivo a utf-8 y quitamos espacios arriba, abajo y dobles saltos de línea
        # Todo esto para que luego el usuario pueda hacecr las modificaciones manuales más facilmente
        # general_nomalization(output_path)
        general_nomalization_template_version(output_path)
    return txts_paths_list

def general_nomalization(file_path:Path):
    """
    Normaliza los textos previo a la normalización manual. Aquí no se pierden datos
    Esto no debería cambiar mucho con el tiempo
    
    VER: [para mayor referencia sobre regex](regex101.com)
    
    """
    emojis = ['🍽️', '🍕', '🍔', '🍟', '🍺', '🥤', '💵', '📍', '☎️', '⏰', '🚚']
    with file_path.open('r+', encoding="utf-8") as f:
        text = f.read()
        text = unicodedata.normalize('NFKD', text) # Normalizamos el tipo de texto
        text = text.strip() # Quitamos espacios y saltos de línea al principio y final
        # Remplazamos texto por emoji en los casos dados
        text = re.sub(r' *🍔 *Descripci.n *:', '🍔', text) 
        text = re.sub(r' *🍺 ?🥤 *Bebidas *:', '🍺', text) 
        text = re.sub(r' *Maridaje *sugerido *:', '🥤', text)
        text = re.sub(r' *MARIDAJE *SUGERIDO *:', '🥤', text)
        text = re.sub(r' *🍟 *Acompañamiento *:', '🍟', text)
        text = re.sub(r' *🍟 *A.*o *:', '🍟', text)
        text = re.sub(r'🍟 Acompañamiento:', '🍟', text) 
        text = text.replace("🍟 Acompañamiento:", "🍟")
        # Creamos excedente de saltos de línea antes de los emojis para que luego no se pierdan al quitar saltos de línea excedentes
        for emoji in emojis:
            text = re.sub(rf'^ *{emoji}', f'\n{emoji}', text, flags=re.M)
        # Ajustamos los saltos de línea para que separen secciones
        text = re.sub(r'^\n+', '*------*', text, flags=re.M)
        text = re.sub('\n', ' ', text)
        text = re.sub('\*------\*', '\n', text)
        # Le damos identificador al nombre de cada comida
        text = re.sub(r'\n(.*)\n🍕', r'\n🍽️ \1\n🍕', text)
        text = re.sub(r'\n(.*)\n🍔', r'\n🍽️ \1\n🍔', text)
        
        # -----------------------------------------------------------------
        # ------- Sobreescribimos el archivo con todo normalizaado --------
        # -----------------------------------------------------------------
        f.seek(0) # Primero apuntamos a la posición inicial del archivo (Para sobreescribir)
        f.write(text) # Escribimos desde esa posición (el puntero de posición se actualiza)
        # Si es que lo que había antes era más grande de lo que ahora se escribió, dejará remanentes
        # Truncamos el archivo a la posición actual apuntada tras el write() 
        # para eliminar esos remanentes
        f.truncate() 
        
def general_nomalization_template_version(file_path:Path):
    """
    Normaliza los textos previo a la normalización manual. Aquí no se pierden datos
    Esto no debería cambiar mucho con el tiempo
    
    VER: [para mayor referencia sobre regex](regex101.com)
    
    """
    emojis = ['🍽️', '🍕', '🍔', '🍟', '🍺', '🥤', '💵', '📍', '☎️', '⏰', '🚚']
    with file_path.open('r+', encoding="utf-8") as f:
        text = f.read()
        text = unicodedata.normalize('NFKD', text) # Normalizamos el tipo de texto
        text = text.strip() # Quitamos espacios y saltos de línea al principio y final
        # Remplazamos texto por emoji en los casos dados
        # TODO: El template y mi programa no llevan los mismo estándares
        # Debo repensar eso
        text = re.sub(r' *🍽️ *Opci.*n *.* *:', '🍽️', text) 
        text = re.sub(r' *🍽️ *Nombre del plato', '🍽️', text) 
        text = re.sub(r' *🍔 *Descripci.*n *:', '🍔', text) 
        text = re.sub(r' *🍟 *Acompañamiento *:', '🍟', text)
        text = re.sub(r' *🍟 *A.*o *:', '🍟', text)
        text = re.sub(r' *🥤 *Bebidas *:', '🍺', text) 
        text = re.sub(r' *🍺 *Maridaje *sugerido *:', '🥤', text)
        text = re.sub(r' *🍺 *MARIDAJE *SUGERIDO *:', '🥤', text)
        text = re.sub(r' *📍 *Direcci.*n.* *:', '📍', text)
        text = re.sub(r' *☎️ *Tel.*fono.* *:', '☎️', text)
        text = re.sub(r' *⏰ *Horarios *:', '⏰', text)
        text = re.sub(r' *🚚 *Delivery *:', '🚚', text)
        
        text = re.sub(r'^\*{3} *.+', '', text, flags=re.M)
        # Creamos excedente de saltos de línea antes de los emojis para que luego no se pierdan al quitar saltos de línea excedentes
        for emoji in emojis:
            text = re.sub(rf'^ *{emoji}', f'\n{emoji}', text, flags=re.M)
        # Ajustamos los saltos de línea para que separen secciones
        text = re.sub(r'^\n+', '*------*', text, flags=re.M)
        text = re.sub('\n', ' ', text)
        text = re.sub('\*------\*', '\n', text)
        
        # -----------------------------------------------------------------
        # ------- Sobreescribimos el archivo con todo normalizaado --------
        # -----------------------------------------------------------------
        f.seek(0) # Primero apuntamos a la posición inicial del archivo (Para sobreescribir)
        f.write(text) # Escribimos desde esa posición (el puntero de posición se actualiza)
        # Si es que lo que había antes era más grande de lo que ahora se escribió, dejará remanentes
        # Truncamos el archivo a la posición actual apuntada tras el write() 
        # para eliminar esos remanentes
        f.truncate() 

if __name__ == "__main__":
    general_nomalization('F:\\VReality\\PizzaWeek\\PW_LP_1ra\\TEMP\\mds-010922_003110\\13. Masa.txt')