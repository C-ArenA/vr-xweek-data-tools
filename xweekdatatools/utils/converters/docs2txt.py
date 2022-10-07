from pathlib import Path
import re
from docx import Document
# Dict con las reglas de normalización del txt antes de ser mostrado al usuario
# Debe tener pares regex_exp - string
prenormalization_rules = {

}


def doc2str(doc_path: Path) -> str:
    document = Document(str(doc_path.absolute()))
    doc_str = ""
    for para in document.paragraphs:
        text_line = para.text.strip()
        if text_line == "*** Si no tiene opción 3 puede dejar en blanco los espacios":
            continue
        if text_line == "*** Separar direcciones/teléfonos/horarios distintos con saltos de línea":
            continue
        if text_line != "":
            doc_str += text_line + "\n"
    return doc_str


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
        output_path = collected_txts_dir.joinpath(
            doc_path.name).with_suffix(".txt")
        # Aparently, pypandoc uses the old path management system of Python, so we will not sen our Path object
        # pypandoc.convert_file(str(doc_path.absolute()), 'plain', outputfile=str(output_path.absolute())) # Convertimos
        txt_str = doc2str(doc_path)
        # Normalizamos el archivo a utf-8 y quitamos espacios arriba, abajo y dobles saltos de línea
        # Todo esto para que luego el usuario pueda hacecr las modificaciones manuales más facilmente
        # general_nomalization(output_path)
        txt_str = general_nomalization_template_version(txt_str)
        # Guardamos en un txt
        output_path.write_text(txt_str, encoding="utf-8")
        txts_paths_list.append(output_path)
        print(f'-> {__name__}: {output_path.absolute()} -> GENERATED .txt')
    return txts_paths_list



def general_nomalization_template_version(text) -> str:
    """
    Normaliza los textos previo a la normalización manual. Aquí no se pierden datos

    Esta prenormalización sirve para cuando se usan las plantillas de word

    VER: [para mayor referencia sobre regex](regex101.com)

    """
    # Normalizamos el tipo de texto
    text = text.strip()  # Quitamos espacios y saltos de línea al principio y final
    # Remplazamos texto por emoji en los casos dados
    # TODO: El template y mi programa no llevan los mismo estándares
    # Debo repensar eso
    text = re.sub(r'^Restaurante *: *', '', text)
    text = re.sub(r' *🍽️ *Opci.*n *.* *: *', '🍽️ ', text)
    text = re.sub(r' *🍽️ *Nombre del plato *', '🍽️', text)
    text = re.sub(r' *🍔 *Descripci.*n *: *', '🍔 ', text)
    text = re.sub(r' *🍟 *Acompañamiento *: *', '🍟 ', text)
    text = re.sub(r' *🍟 *A.*o *: *', '🍟 ', text)
    text = re.sub(r' *🥤 *Bebidas *: *', '🍺 ', text)
    text = re.sub(r' *🍺 *Maridaje *sugerido *: *', '🥤 ', text)
    text = re.sub(r' *🍺 *MARIDAJE *SUGERIDO *: *', '🥤 ', text)
    text = re.sub(r' *📍 *Direcci.*n.* *: *', '📍 ', text)
    text = re.sub(r' *☎️ *Tel.*fono.* *: *', '☎️ ', text)
    text = re.sub(r' *⏰ *Horarios *: *', '⏰ ', text)
    text = re.sub(r' *🚚 *Delivery *: *', '🚚 ', text)
    return text

