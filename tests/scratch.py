from configparser import ConfigParser
config = ConfigParser()
config.read("config-bw.ini")  # <------- CONFIG FILE
try:
    a = config["event"]["no"]
except:
    a = ""

b = config["event"]["no"] if config["event"]["no"] else ""

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