import qrcode  # pip install qrcode[pil]
import os
import json

def gen_qr_codes(error_level, dst_dir, urls_list=[], json_path=""):
    """
    Genera QRs basado en una lista de URLs o en un JSON
    Si se especifican ambos, la lista tiene precedencia
    Sólo especifique uno para evitar confusiones
    """
    if len(urls_list)==0:
        #check json
        # TODO: Revisar si el JSON existe
        restaurants = getRestaurantsList(json_path)
        urls_list = [r["url"] for r in restaurants]
    
    error_levels_dict = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H,
    }

    qr = qrcode.QRCode(
        version=1,
        error_correction=error_levels_dict[error_level],
        box_size=10,
        border=4
    )

    parent_directory = dst_dir
    child_directory = "QRCodesGenerated_" + error_level
    directory = parent_directory + "\\" + child_directory
    path = os.path.join(parent_directory, child_directory)

    try:
        os.mkdir(path)
    except:
        print("El directorio ya existe, se sobrescriben las imágenes")

    for url in urls_list:
        qr.add_data(url)
        qr.make(fit=True)
        image = qr.make_image(fill_color="black", back_color="white")
        image.save(directory + "\\" + url.split('.com/')[1] + ".png")
        qr.clear()

def getRestaurantsList(json_path)-> list:
    """
    Devuelve la lista de restaurantes ordenada
    """
    with open(json_path, "r", encoding="utf-8") as jsonf:
        data = json.load(jsonf)
    restaurants = data["restaurants"]
    return sorted(restaurants, key=lambda restaurant: restaurant["order"])