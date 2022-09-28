import json

# Se puede añadir info cambiando esta constante, pero los nombres deben coincidir con el json
URL_CSV_HEADERS = ["name", "post_name", "slugified_name", "post_name", "post_url"]

def gen_url_csv(json_path, csv_dir):
    import csv
    with open(csv_dir, encoding='utf-8', mode='w', newline="") as csvf:
        csv_writer = csv.writer(csvf)
        csv_writer.writerow(URL_CSV_HEADERS)
        csv_writer.writerows([getRestaurantUrlData(r) for r in getRestaurantsList(json_path)]) # Genero una lista de listas, cada sublista es un row en CSV
        csvf.close()

def gen_url_xlsx(json_path, xlsx_dir):
    from openpyxl import Workbook
    wb= Workbook()
    ws = wb.active # ws = active sheet
    ws.append(URL_CSV_HEADERS) # añado los headers
    # Adquiero la lista de restaurantes
    restaurants = getRestaurantsList(json_path)
    # Añado cada restaurante a cada fila del excel
    for r in restaurants:
        ws.append(getRestaurantUrlData(r))
    # Guardo el archivo excel
    wb.save(xlsx_dir)

def getRestaurantsList(json_path)-> list:
    """
    Devuelve la lista de restaurantes ordenada
    """
    with open(json_path, "r", encoding="utf-8") as jsonf:
        data = json.load(jsonf)
    restaurants = data["restaurants"]
    return sorted(restaurants, key=lambda restaurant: restaurant["order"])

def getRestaurantUrlData(restaurant_dict)-> list:
    """
    Devuelve la info del restaurante en forma de lista/fila
    """
    rest_data_list = [restaurant_dict[key] for key in URL_CSV_HEADERS]
    return rest_data_list

if __name__ == "__main__":
    rests = getRestaurantsList("F:\VReality\PizzaWeek\PW_LP_1ra\TEMP\pw_lp-1ra_010922_113548.json")