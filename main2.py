# ----------------- EXTERNAL IMPORTS
from collectors.collect_images import collect_images
from tools.gen_qr_codes import gen_qr_codes
from tools.gen_url_csv_xlsx import gen_url_csv, gen_url_xlsx
from converters.raw_data_to_dict import raw_data_to_dict
from converters.docs2txt import docs2txt
from collectors.collect_docs import collect_docs
from collectors.get_rest_folders import get_rest_folders
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
config.read("config-bw.ini")  # <------- CONFIG FILE
xweek = {
    "event_name": config["event"]["name"],
    "event_domain": config["event"]["domain"],
    "event_version": config["event"]["version"],
    "event_long_description": "Descripción larga, aún no definida",
    "event_short_description": "Descripción corta, aún no definida",
    "event_calendar": "Del x al y de m (por definir)",
    "event_media_url": config["event"]["uploads_url"],
    "restaurants": []
}
xweekevent = {
    "name": config["event"]["name"],
    "domain": config["event"]["domain"],
    "version": config["event"]["version"],
    "directory": os.path.normpath(config["event"]["directory"]),
    "uploads_url": os.path.normpath(config["event"]["uploads_url"]),
    "last_execution": os.path.normpath(config["history"]["last_execution"]),
}
# THESE ARE  DEFAULT VALUES that can be changed by the user
xweeknow = datetime.datetime.now().strftime("%d%m%y_%H%M%S")
xweekpaths = {
    # ---------------- Source folders
    "data_src": os.path.join(xweekevent["directory"], "ORIGIN_FILES"),
    "photos_src": os.path.join(xweekevent["directory"], "PHOTOS"),
    "logos_src": os.path.join(xweekevent["directory"], "ORIGIN_FILES"),
    # --------------- Destination folders and files
    "temp": os.path.join(xweekevent["directory"], "TEMP"),
    "docs_dst": os.path.join(xweekevent["directory"], "TEMP", xweeknow, "docs"),
    "txts_dst": os.path.join(xweekevent["directory"], "TEMP", xweeknow, "txts"),
    "photos_dst": os.path.join(xweekevent["directory"], "TEMP", xweeknow, "photos"),
    "logos_dst": os.path.join(xweekevent["directory"], "TEMP", xweeknow, "logos"),
    "qrs_dst": os.path.join(xweekevent["directory"], "TEMP", xweeknow, "qrs"),
    "json_dst": os.path.join(xweekevent["directory"], "TEMP", xweeknow + "-data.json"),
    # --------------- Last processed folders by default
    "docs_last": os.path.join(xweekevent["directory"], "TEMP", xweeknow, "docs"),
    "txts_last": os.path.join(xweekevent["directory"], "TEMP", xweeknow, "txts"),
    "photos_last": os.path.join(xweekevent["directory"], "TEMP", xweeknow, "photos"),
    "logos_last": os.path.join(xweekevent["directory"], "TEMP", xweeknow, "logos"),
    "qrs_last": os.path.join(xweekevent["directory"], "TEMP", xweeknow, "qrs"),
    "json_last": os.path.join(xweekevent["directory"], "TEMP", xweeknow + "-data.json"),
}
try:
    xweekpaths["docs_last"] = os.path.normpath(config["history"]["docs_last"])
    xweekpaths["txts_last"] = os.path.normpath(config["history"]["txts_last"])
except:
    pass
try:
    xweekpaths["photos_last"] = os.path.normpath(
        config["history"]["photos_last"])
    xweekpaths["logos_last"] = os.path.normpath(
        config["history"]["logos_last"])
    xweekpaths["qrs_last"] = os.path.normpath(config["history"]["qrs_last"])
except:
    pass
try:
    xweekpaths["json_last"] = os.path.normpath(config["history"]["json_last"])
except:
    pass

# -----------------------------------------------------------------------


def raw_data_collector(src_dir, docs_dir="", txts_dir="", collect_process=True) -> list:
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
        xweekpaths["docs_dst"] if collect_process else xweekpaths["docs_last"]) if docs_dir == "" else docs_dir
    txts_dir = (
        xweekpaths["txts_dst"] if collect_process else xweekpaths["txts_last"]) if txts_dir == "" else txts_dir

    if collect_process:
        # ----- SE RECOLECTAN ARCHIVOS ------
        # ----- Creo los directorios temporales y los guardo en el config file
        os.makedirs(docs_dir, exist_ok=True)
        os.makedirs(txts_dir, exist_ok=True)
        config["history"]["docs_last"] = docs_dir
        config["history"]["txts_last"] = txts_dir
        with open("config-bw.ini", "w") as cf:
            config.write(cf)
        # ----- Obtengo carpetas de restaurantes
        rest_folders = get_rest_folders(src_dir)
        # ----- Recolecto doc*s
        docs_list = collect_docs(rest_folders, docs_dir)["docs_new_paths"]
        # ----- Transformo docs en markdowns
        txts_list = docs2txt(docs_list, txts_dir)
    else:
        # ----- NO SE RECOLECTAN ARCHIVOS, sólo se busca los mds recolectados ------

        logging.debug(
            f'Se recupera la lista de mds de la última carpeta usada o especificada como: {txts_dir}')
        # Verifico que existan los directorios

        if not os.path.isdir(txts_dir):
            raise Exception("\n\n -> " + __name__ +
                            "(): El directorio de txts especificado no existe")
        # ----- Listo los mds existentes
        txts_list = [os.path.join(txts_dir, txtname)
                     for txtname in os.listdir(txts_dir)]
    return txts_list


def main():
    collect_process_input = input(
        "Desea recolectar archivos desde cero? (Y/N)")
    collect_process_input = True if collect_process_input == "Y" else False
    raw_txts = raw_data_collector(
        src_dir=xweekpaths["data_src"], collect_process=collect_process_input)
    # Ahora el usuario debe verificar que los markdowns cumplan el formato deseado:
    """
    COZZOLOSSI 
    🍽️ La Serrana 
    🍔 Jamón serrano, rúcula y queso parmesano. 
    🍺 Huari Tradicional o Huari Miel o Huari Chocolate o Pepsi o Pepsi Light o 7Up 
    🥤 Huari Tradicional 
    💵 Bs. 55 
    🍽️ INTENSA 
    🍔 Salame, tomate, choclo y aceitunas negras. 
    🍺 Huari Tradicional o Huari Miel o Huari Chocolate o Pepsi o Pepsi Light o 7Up 
    🥤 Huari Miel 
    💵 Bs. 55 
    🍽️ DELICATA 
    🍔 Tocino, alcachofa y aceituna verde. 
    🍺 Huari Tradicional o Huari Miel o Huari Chocolate o Pepsi o Pepsi Light o 7Up 
    🥤 Huari Chocolate 
    💵 Bs. 55 
    📍 San Miguel: Calle E. Peñaranda bloque L-30 - Sopocachi: 20 de octubre, 2347 entre Belisario Salinas y Rosendo Gutiérrez 
    ☎️ San Miguel: 76761819 - 2772773- 2773333. Sopocachi: 69859246- 2414106 
    ⏰ Lunes de 16:30 a 22:00. De martes de jueves de 12:00 a 22:00. Viernes y sábado de 12:00 a 23:00. Domingo de 12:00 a 22:00 
    🚚 Yaigo y Pedidos Ya
    """
    if input("Ya verificó que los archivos de texto como " +
             raw_txts[0] + " generados cumplan el formato? (Y/N)") != "Y":
        print("Esperamos a la siguiente ejecución, hasta pronto")
        return
    # Ahora genero el diccionario con los restaurantes
    rest_list = raw_data_to_dict(
        raw_txts, xweekevent["domain"], xweekevent["uploads_url"], xweekevent["version"])
    rest_list.sort(key=lambda r: r["name"])

    xweek["restaurants"] = rest_list
    # Lo exporto en JSON si se quiere o uso el último JSON
    gen_json_input = input(
        "Desea generar JSON nuevo (o usar el último existente)? (Y/N)")
    gen_json_input = True if gen_json_input == "Y" else False

    if gen_json_input:
        json_file_path = xweekpaths["json_dst"]
        with open(xweekpaths["json_dst"], "w", encoding='utf-8') as jsonf:
            json.dump(xweek, jsonf, ensure_ascii=False, indent=4)
            # Guardo el archivo JSON
            config["history"]["json_last"] = xweekpaths["json_dst"]
            with open("config-bw.ini", "w") as cf:
                config.write(cf)
    else:
        json_file_path = xweekpaths["json_last"]

    for rest in rest_list:
        print("---------------------------")
        print(rest["name"])
        print("---------------------------")
        for dish in rest["dishes"]:
            print(dish["photo_name"][:-4])

    # Ahora genero los archivos que necesita el resto del equipo
    # Genero csv y xlsx de URLs
    gen_csvxlsx_input = input("Desea generar csv y xlsx nuevo? (Y/N)")
    gen_csvxlsx_input = True if gen_csvxlsx_input == "Y" else False
    if gen_csvxlsx_input:
        new_csv_path = os.path.join(
            xweekpaths["temp"], "urls_pw_"+xweekevent["version"]+"_"+datetime.datetime.now().strftime("%d%m%y_%H%M%S")+".csv")
        new_xlsx_path = os.path.join(
            xweekpaths["temp"], "urls_pw_"+xweekevent["version"]+"_"+datetime.datetime.now().strftime("%d%m%y_%H%M%S")+".xlsx")
        gen_url_csv(json_file_path, new_csv_path)
        gen_url_xlsx(json_file_path, new_xlsx_path)
    # Genero QRs
    gen_qrs_input = input("Desea generar QRs? (Y/N)")

    gen_qrs_input = True if gen_qrs_input=="Y" else False

    if gen_qrs_input:
        print("QRS a ->" + xweekpaths["qrs_dst"])
        os.makedirs(xweekpaths["qrs_dst"], exist_ok=True)
        gen_qr_codes("L", xweekpaths["qrs_dst"], json_path=json_file_path)
        gen_qr_codes("M", xweekpaths["qrs_dst"], json_path=json_file_path)
        gen_qr_codes("Q", xweekpaths["qrs_dst"], json_path=json_file_path)
        gen_qr_codes("H", xweekpaths["qrs_dst"], json_path=json_file_path)


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
    # xweekpaths["json_dst"] = os.path.join(TEMP_DIRECTORY, "imgs_pw_"+VERSION_SPECIFIER+"_"+datetime.datetime.now().strftime("%d%m%y_%H%M%S")+".json")
    # with open(xweekpaths["json_dst"], "w", encoding='utf-8') as jsonf:
    #     json.dump(data, jsonf, ensure_ascii=False, indent=4)
