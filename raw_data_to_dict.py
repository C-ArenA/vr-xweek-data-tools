import logging
import os
import pprint
import re
from slugify import slugify

# Para convertir el archivo a dict, necesito reconocer patrones, los cuales están determinados por los emojis, así que los debo relacionar con el key correspondiente del dict resultante
emojis_list = [
    {"for":"dish", "key": "name", "emoji": '🍽️'},
    {"for":"dish", "key": "name", "emoji": '🍽'},
    {"for":"dish", "key": "description", "emoji": '🍕'}, # For Pizza Week
    {"for":"dish", "key": "description", "emoji": '🍔'}, # For Burger Week
    {"for":"dish", "key": "accompaniment", "emoji": '🍟'}, # For Burger Week
    {"for":"dish", "key": "drinks", "emoji": '🍺'},
    {"for":"dish", "key": "pairing", "emoji": '🥤'},
    {"for":"dish", "key": "price", "emoji": '💵'},
    {"for":"restaurant", "key": "address", "emoji": '📍'},
    {"for":"restaurant", "key": "phone", "emoji": '☎️'},
    {"for":"restaurant", "key": "phone", "emoji": '☎'},
    {"for":"restaurant", "key": "opening_hours", "emoji": '⏰'},
    {"for":"restaurant", "key": "delivery", "emoji": '🚚'},
]

def convert_file_to_dict(file_path, event_domain, uploads_url="/", event_version_specifier="", photos_format="jpg", logos_format="png"):
    """
    # Texto plano a JSON
    Se saca todo lo que se puede sacar de información al texto plano que cumple el patrón específico pensado para esta función
    Se crean las keys que irán al JSON final, incluso si no tenemos información con la cual rellenarlas
    """
    # El texto plano del archivo lo convierto en un array para poder analizar de forma más sencilla
    with open(file_path, 'r', encoding='utf-8') as f:
        text_str = f.read()
        # Para evitar problemas de compatibilidad:
        text_str = text_str.replace('🍽️','🍽')
        text_str = text_str.replace('☎️','☎')
        regex = r"(["
        for emoji in emojis_list:
            regex += emoji["emoji"]
        regex += "])"
        text_array = re.split(regex, text_str)
    
    # Inicializo el dict porque en un futuro haré que sea necesario tener los keys ya presentes
    # Por qué? -> Porque si hay varias lineas de información las iré concatenando, necesito donde concatenar
    # Por qué? -> Porque si lleno manualmente algunas partes del JSON me es más fácil que los keys ya estén ahí
    restaurant_data = {
        # Devuelve el número inicial del nombre del archivo (El orden de 17.Loop.txt es 17)
        "order": int(os.path.basename(file_path).split(".")[0]),
        "name": text_array[0].strip(),
        "address": "",
        "phone": "",
        "opening_hours": "",
        "delivery": "",
        "slugified_name": "",
        "post_title": "",
        "post_name": "",
        "post_url": "",
        "logo_name": "",
        "logo_url": "",
        "dishes": []
    }

    # Datos del post del restaurante
    restaurant_data["slugified_name"] = slugify(restaurant_data["name"])
    restaurant_data["post_title"] = restaurant_data["name"] + " " + event_version_specifier
    restaurant_data["post_name"] = slugify(restaurant_data["post_title"])
    restaurant_data["post_url"] = event_domain + "/" + restaurant_data["post_name"]
    restaurant_data["logo_name"] = restaurant_data["post_name"] + "." + logos_format
    restaurant_data["logo_url"] = uploads_url + restaurant_data["logo_name"]
    
    logging.debug("Extrayendo datos de: " + restaurant_data["name"])

    dish_data = {}
    for i in range(len(text_array)):
        new_emoji = is_emoji(text_array[i], emojis_list)
        if new_emoji and i+1 < len(text_array):
            if new_emoji["for"] == "restaurant":
                restaurant_data[new_emoji["key"]] = text_array[i+1].strip()
            else:
                if new_emoji["key"] == "name":
                    # Cada vez que se encuentre el nombre de un dish se comienza recolectando otro dish desde cero
                    
                    dish_data={
                        "name":"",
                        "description":"",
                        "accompaniment":"",
                        "drinks":"",
                        "pairing":"",
                        "price":"",
                        "photo_name":"",
                        "photo_url":"",
                    }
                dish_data[new_emoji["key"]] = text_array[i+1].strip()
                if new_emoji["key"] == "price":
                    # El dish se guarda en los datos del restaurante si es que tiene hasta el precio asignado
                    # Se pone un nombre posible a la foto y su respectiva URL antes de guardar
                    if "price" in dish_data:
                        if dish_data["price"]:
                            dish_data["photo_name"] = restaurant_data["post_name"] + "_" + slugify(dish_data["name"]) + "." + photos_format
                            dish_data["photo_url"] =  uploads_url + dish_data["photo_name"]
                            restaurant_data["dishes"].append(dish_data)
    return restaurant_data

def raw_data_to_dict(text_files_paths, event_domain, uploads_url="/", event_version_specifier="", photos_format="jpg", logos_format="png"):
    restaurants = []
    for text_path in text_files_paths:
        restaurant = convert_file_to_dict(text_path, event_domain, uploads_url, event_version_specifier, photos_format, logos_format)
        restaurants.append(restaurant)
    return restaurants

def is_emoji(string, emojis_list):
    for emoji in emojis_list:
        if string == emoji["emoji"]:
            return emoji
    return False

if __name__ == "__main__":
    txt_for_testing_path = os.path.normpath("f:\VReality\PizzaWeek\PW_LP_1ra\TEMP\mds-010922_030753 - copia\9. Khofisuyo.txt")
    txts_for_testing_path = [os.path.normpath("f:\VReality\PizzaWeek\PW_LP_1ra\TEMP\mds-010922_030753 - copia\9. Khofisuyo.txt")]
    pprint.pprint(convert_file_to_dict(txt_for_testing_path, "pizzaweek.com", "/", "lp-1ra"))
