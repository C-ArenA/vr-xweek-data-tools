# ----------------- EXTERNAL IMPORTS
from collect_images import collect_images
from gen_qr_codes import gen_qr_codes
from gen_url_csv_xlsx import gen_url_csv, gen_url_xlsx
from raw_data_to_dict import raw_data_to_dict
from docs2md import docs2md
from collect_docs import collect_docs
from get_rest_folders import get_rest_folders
from configparser import ConfigParser
import os
import json
from slugify import slugify
import datetime
import logging
# Para modificar el formato tenemos los atributos en: https://docs.python.org/3/library/logging.html#logrecord-attributes
logging.basicConfig(
    format='%(funcName)s(): %(levelname)s [%(lineno)s]:\n💮-> %(message)s', level=logging.DEBUG)

# ---------------- MY IMPORTS (In order of usage)
# --------------------------- RETRIEVING CONFIG  DATA -----------------

config = ConfigParser()
config.read("config-bw.ini") ######## <------- CONFIG FILE
xweekevent = {
    "name": config["event"]["name"],
    "domain": config["event"]["domain"],
    "version": config["event"]["version"],
    "directory": os.path.normpath(config["event"]["directory"]),
    "uploads_url": os.path.normpath(config["event"]["uploads_url"]),
}
# THESE ARE  DEFAULT VALUES that can be changed by the user
xweeknow = datetime.datetime.now().strftime("%d%m%y_%H%M%S")
xweekpaths = {
    # ---------------- Source folders
    "data_src": os.path.join(xweekevent["directory"], "ORIGIN_FILES"),
    "photos_src": os.path.join(xweekevent["directory"], "PHOTOS"),
    "logos_src": os.path.join(xweekevent["directory"], "ORIGIN_FILES"),
    # --------------- Destination folders
    "temp": os.path.join(xweekevent["directory"], "TEMP"),
    "docs_dst": os.path.join(xweekevent["directory"], "TEMP", xweeknow, "docs"),
    "txts_dst": os.path.join(xweekevent["directory"], "TEMP", xweeknow, "txts"),
    "photos_dst": os.path.join(xweekevent["directory"], "TEMP", xweeknow, "photos"),
    "logos_dst": os.path.join(xweekevent["directory"], "TEMP", xweeknow, "logos"),
    "qrs_dst": os.path.join(xweekevent["directory"], "TEMP", xweeknow, "qrs"),
    # --------------- Last processed folders
    "docs_dst": os.path.join(xweekevent["directory"], "TEMP", xweeknow, "docs"),
    "txts_dst": os.path.join(xweekevent["directory"], "TEMP", xweeknow, "txts"),
    "photos_dst": os.path.join(xweekevent["directory"], "TEMP", xweeknow, "photos"),
    "logos_dst": os.path.join(xweekevent["directory"], "TEMP", xweeknow, "logos"),
    "qrs_dst": os.path.join(xweekevent["directory"], "TEMP", xweeknow, "qrs"),
}

DOMAIN = config["event"]["DOMAIN"]
VERSION_SPECIFIER = config["event"]["VERSION_SPECIFIER"]
EVENT_DIRECTORY = os.path.normpath(config["event"]["EVENT_DIRECTORY"])
SRC_DIRECTORY = os.path.normpath(config["event"]["SRC_DIRECTORY"])
SRC_IMG_DIRECTORY = os.path.normpath(config["event"]["src_img_directory"])
WP_CONTENT_URL = config["event"]["WP_CONTENT_URL"]

# ---- Defino paths de archivos temporales
TEMP_DIRECTORY = os.path.join(EVENT_DIRECTORY, "TEMP2")

DOCS_DIRECTORY = os.path.join(
    TEMP_DIRECTORY, "docs-" + datetime.datetime.now().strftime("%d%m%y_%H%M%S"))
MDS_DIRECTORY = os.path.join(
    TEMP_DIRECTORY, "mds-" + datetime.datetime.now().strftime("%d%m%y_%H%M%S"))
IMGS_DIRECTORY = os.path.join(
    TEMP_DIRECTORY, "imgs-" + datetime.datetime.now().strftime("%d%m%y_%H%M%S"))
QRS_DIRECTORY = os.path.join(
    TEMP_DIRECTORY, "qrs-" + datetime.datetime.now().strftime("%d%m%y_%H%M%S"))
try:
    LAST_DOCS_DIRECTORY = os.path.normpath(
        config["event"]["LAST_DOCS_DIRECTORY"])
    LAST_MDS_DIRECTORY = os.path.normpath(
        config["event"]["LAST_MDS_DIRECTORY"])
except:
    LAST_DOCS_DIRECTORY = ""
    LAST_MDS_DIRECTORY = ""
try:
    LAST_IMGS_DIRECTORY = os.path.normpath(
        config["event"]["last_imgs_directory"])
except:
    LAST_IMGS_DIRECTORY = ""
try:
    LAST_JSON_FILE = os.path.normpath(config["event"]["LAST_JSON_FILE"])
except:
    LAST_JSON_FILE = ""

# -----------------------------------------------------------------------
logging.debug(DOMAIN)


def raw_data_collector(docs_dir="", mds_dir="", collect_process=True) -> list:
    """
    # Recolecta datos de restaurantes en markdown
    ** El flag collect_process es útil porque el proceso de recolección es lento y es cómodo poder evitarlo si ya se hizo la recolección y se quiere usar esta función para obtener la lista de markdowns antes recolectados

    Si el collect_process es True, se realiza la recolección como tal, se busca entre los archivos de los restaurantes hasta extraer todo en una carpeta temporal
    Si el collect_process es False, se revisan los archivos ya recolectados en los archivos especificado o en el último usado si no se especifica

    :param docs_dir -> Directorio donde guardar los docs recolectados (collect_process=True) o del cual se revisa lo antes recolectado (collect_process=False)
    :param mds_dir -> Directorio donde guardar los mds recolectados (collect_process=True) o del cual se revisa lo antes recolectado (collect_process=False)
    :param collect_process -> Flag para ver si se realiza todo el proceso o se revisa algo previo
    :return -> Retorna la lista de markdowns recolectados (sus paths completos)
    """
    # Si se especificó docs_dir y mds_dir se usa eso, pero sino se usan los directorios por defecto de acuerdo al caso:
    # - Si se recolectan archivos, por defecto se usa un nuevo directorio
    # - Si no se recolectan, por defecto se usa el último directorio en que se guardó
    docs_dir = (
        DOCS_DIRECTORY if collect_process else LAST_DOCS_DIRECTORY) if docs_dir == "" else docs_dir
    mds_dir = (
        MDS_DIRECTORY if collect_process else LAST_MDS_DIRECTORY) if mds_dir == "" else mds_dir

    if collect_process:
        # ----- SE RECOLECTAN ARCHIVOS ------
        # ----- Creo los directorios temporales
        os.makedirs(docs_dir, exist_ok=True)
        os.makedirs(mds_dir, exist_ok=True)
        config["event"]["LAST_DOCS_DIRECTORY"] = docs_dir
        config["event"]["LAST_MDS_DIRECTORY"] = mds_dir
        with open("config.ini", "w") as cf:
            config.write(cf)
        # ----- Obtengo carpetas de restaurantes
        rest_folders = get_rest_folders(SRC_DIRECTORY)
        # ----- Recolecto doc*s
        docs_list = collect_docs(rest_folders, docs_dir)["docs_new_paths"]
        # ----- Transformo docs en markdowns
        mds_list = docs2md(docs_list, mds_dir)
    else:
        # ----- NO SE RECOLECTAN ARCHIVOS, sólo se busca los mds recolectados ------

        logging.debug(
            f'Se recupera la lista de mds de la última carpeta usada o especificada como: {mds_dir}')
        # Verifico que existan los directorios

        if not os.path.isdir(mds_dir):
            raise Exception("\n\n -> " + __name__ +
                            "(): El directorio de mds especificado no existe")
        # ----- Listo los mds existentes
        mds_list = [os.path.join(mds_dir, mdname)
                    for mdname in os.listdir(mds_dir)]
    return mds_list


def process_images(overwrite=False):
    imgs_dir = IMGS_DIRECTORY
    if overwrite:
        imgs_dir = LAST_IMGS_DIRECTORY if LAST_IMGS_DIRECTORY != "" else IMGS_DIRECTORY

    # ----- SE RECOLECTAN ARCHIVOS ------
    # ----- Creo los directorios temporales
    os.makedirs(imgs_dir, exist_ok=True)

    config["event"]["LAST_IMGS_DIRECTORY"] = imgs_dir
    with open("config.ini", "w") as cf:
        config.write(cf)

    img_rest_folders = get_rest_folders(SRC_IMG_DIRECTORY)
    imgs_list = collect_images(
        VERSION_SPECIFIER, img_rest_folders, imgs_dir, extension="jpg")["imgs_new_paths"]
    # TODO Comprimir imágenes
    # Iteramos sobre los restaurantes y sus platos para añadir las imágenes
    json_path = LAST_JSON_FILE
    with open(json_path, "r", encoding="utf-8") as jsonf:
        data = json.load(jsonf)
    restaurants = data["restaurants"]
    for r in restaurants:
        for plate in r["food"]:
            print(plate["plate_name"])


def main():
    collect_process_input = input(
        "Desea recolectar archivos desde cero? (Y/N)")
    collect_process_input = True if collect_process_input == "Y" else False
    raw_mds = raw_data_collector(collect_process=collect_process_input)
    # Ahora el usuario debe verificar que los markdowns cumplan el formato deseado:
    """
    COZZOLOSSI 
    🍽️ La Serrana 
    🍕 Jamón serrano, rúcula y queso parmesano. 
    🍺 Huari Tradicional o Huari Miel o Huari Chocolate o Pepsi o Pepsi Light o 7Up 
    🥤 Huari Tradicional 
    💵 Bs. 55 
    🍽️ INTENSA 
    🍕 Salame, tomate, choclo y aceitunas negras. 
    🍺 Huari Tradicional o Huari Miel o Huari Chocolate o Pepsi o Pepsi Light o 7Up 
    🥤 Huari Miel 
    💵 Bs. 55 
    🍽️ DELICATA 
    🍕 Tocino, alcachofa y aceituna verde. 
    🍺 Huari Tradicional o Huari Miel o Huari Chocolate o Pepsi o Pepsi Light o 7Up 
    🥤 Huari Chocolate 
    💵 Bs. 55 
    📍 San Miguel: Calle E. Peñaranda bloque L-30 - Sopocachi: 20 de octubre, 2347 entre Belisario Salinas y Rosendo Gutiérrez 
    ☎️ San Miguel: 76761819 - 2772773- 2773333. Sopocachi: 69859246- 2414106 
    ⏰ Lunes de 16:30 a 22:00. De martes de jueves de 12:00 a 22:00. Viernes y sábado de 12:00 a 23:00. Domingo de 12:00 a 22:00 
    🚚 Yaigo y Pedidos Ya
    """
    input("Ya verificó que los archivos de texto como " +
          raw_mds[0] + " generados cumplan el formato? (Y/N)")
    # Ahora genero el diccionario con los restaurantes
    rest_list = raw_data_to_dict(
        raw_mds, DOMAIN, WP_CONTENT_URL, VERSION_SPECIFIER)
    rest_list.sort(key=lambda r: r["name"])

    data = {
        "event_name": "Pizza Week",
        "event_domain": DOMAIN,
        "event_version": VERSION_SPECIFIER,
        "event_long_description": "Descripción larga, aún no definida",
        "event_short_description": "Descripción corta, aún no definida",
        "event_calendar": "Del x al y de m (por definir)",
        "event_media_url": "/ (por definir)",
        "restaurants": rest_list
    }
    # Lo exporto en JSON si se quiere o uso el último JSON
    gen_json_input = input(
        "Desea generar JSON nuevo (o usar el último existente)? (Y/N)")
    gen_json_input = True if gen_json_input == "Y" else False
    if gen_json_input:
        new_json_path = os.path.join(TEMP_DIRECTORY, "pw_"+VERSION_SPECIFIER +
                                     "_"+datetime.datetime.now().strftime("%d%m%y_%H%M%S")+".json")
        with open(new_json_path, "w", encoding='utf-8') as jsonf:
            json.dump(data, jsonf, ensure_ascii=False, indent=4)
            # Guardo el archivo JSON
            config["event"]["LAST_JSON_FILE"] = new_json_path
            with open("config.ini", "w") as cf:
                config.write(cf)
    else:
        new_json_path = LAST_JSON_FILE

    for rest in rest_list:
        print("---------------------------")
        print(rest["name"])
        print("---------------------------")
        for dish in rest["dishes"]:
            print(dish["photo_name"][:-4])

    # Ahora genero los archivos que necesita el resto del equipo
    # Genero csv y xlsx de URLs
    # gen_csvxlsx_input = input("Desea generar csv y xlsx nuevo? (Y/N)")
    # gen_csvxlsx_input = True if gen_csvxlsx_input=="Y" else False
    # if gen_csvxlsx_input:
    #     new_csv_path = os.path.join(TEMP_DIRECTORY, "urls_pw_"+VERSION_SPECIFIER+"_"+datetime.datetime.now().strftime("%d%m%y_%H%M%S")+".csv")
    #     new_xlsx_path = os.path.join(TEMP_DIRECTORY, "urls_pw_"+VERSION_SPECIFIER+"_"+datetime.datetime.now().strftime("%d%m%y_%H%M%S")+".xlsx")
    #     gen_url_csv(new_json_path, new_csv_path)
    #     gen_url_xlsx(new_json_path, new_xlsx_path)
    # # Genero QRs
    # gen_qrs_input = input("Desea generar QRs? (Y/N)")

    # gen_qrs_input = True if gen_qrs_input=="Y" else False

    # if gen_qrs_input:
    #     print("QRS a ->" + QRS_DIRECTORY)
    #     os.makedirs(QRS_DIRECTORY, exist_ok=True)
    #     gen_qr_codes("L", QRS_DIRECTORY, json_path=new_json_path)
    #     gen_qr_codes("M", QRS_DIRECTORY, json_path=new_json_path)
    #     gen_qr_codes("Q", QRS_DIRECTORY, json_path=new_json_path)
    #     gen_qr_codes("H", QRS_DIRECTORY, json_path=new_json_path)


if __name__ == "__main__":
    main()
    # process_images()
    # img = input("Suelte una imagen")
    # print(img)
    # Iteramos sobre los restaurantes y sus platos para añadir las imágenes
    # json_path = LAST_JSON_FILE
    # with open(json_path, "r", encoding="utf-8") as jsonf:
    #     data = json.load(jsonf)
    # restaurants = data["restaurants"]
    # for r in restaurants:
    #     print("\n---------------------\n")
    #     for plate in r["food"]:
    #         print(r["order"] + " - " + r["name"] + " -> " + plate["plate_name"].strip() + "\n")
    #         plate["img_name"] = os.path.basename(input("Arrastre la imagen correspondiente: "))
    # new_json_path = os.path.join(TEMP_DIRECTORY, "imgs_pw_"+VERSION_SPECIFIER+"_"+datetime.datetime.now().strftime("%d%m%y_%H%M%S")+".json")
    # with open(new_json_path, "w", encoding='utf-8') as jsonf:
    #     json.dump(data, jsonf, ensure_ascii=False, indent=4)
