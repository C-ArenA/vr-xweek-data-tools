from pprint import pprint
import datetime
import copy
import json
import os
from traceback import print_tb
from yachalk import chalk
from InquirerPy import inquirer, get_style, validator
style = get_style({"questionmark": "#ff3355",
                  "answer": "#0055ff"}, style_override=False)

with open("db.json", "r", encoding='utf-8') as jsonfile:
    XWEEK_DB = json.load(jsonfile)
xweekconfig = XWEEK_DB["xweekconfig"]
xweeklast = XWEEK_DB["xweekdata"][-1]
past_event = xweeklast["xweekevent"]
xweekcurrent = copy.deepcopy(xweeklast)
current_event = xweekcurrent["xweekevent"]
xweekcurrent["xweeknow"] = datetime.datetime.now().strftime("%d%m%y_%H%M%S")


def main():
    initrender()
    while True:
        initrender()
        print("Estos son los datos actuales del evento:")
        print(chalk.green(json.dumps(
            current_event, indent=2, ensure_ascii=False)))

        if inquirer.confirm(message="Deseas actualizar estos datos?", style=style).execute():
            initrender()
            update_data(xweekconfig, current_event, past_event)
        else:
            break


def initrender():
    """
    Genera el encabezado del CLI
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print(chalk.blue.bold(
        "\n-------------------------------------------------------------"))
    print(chalk.blue.bold(
        "|😀 Bienvenido. Esta pequeña aplicación te ayudará a extraer |"))
    print(chalk.blue.bold(
        "|los datos de tu siguiente evento en un archivo JSON         |"))
    print(chalk.blue.bold(
        "-------------------------------------------------------------\n"))


def update_data(xweekconfig, xweekevent, xweekpastevent):
    """Ayuda al usuario a actualizar los datos del evento

    Args:
        xweekconfig (_type_): _description_
        xweekevent (_type_): _description_
        xweekpastevent (_type_): _description_
    """
    # --- 1. Nombre del Evento
    xweekevent["event_name"] = inquirer.text(
        message="Nombre del Evento:",
        default=xweekpastevent["event_name"],
        completer={name: None for name in xweekconfig["event_names"]},
        multicolumn_complete=True).execute()
    # --- 2. Lugar del Evento
    xweekevent["event_location"] = inquirer.text(
        message="Lugar del evento:",
        default=xweekpastevent["event_location"],
        completer={
            location: None for location in xweekconfig["event_locations"]},
        multicolumn_complete=True).execute()
    # --- 3. Abreviación del lugar del Evento
    try:
        default_loc_abb = xweekconfig["event_locations_abbreviations"][xweekconfig["event_locations"].index(
            xweekevent["event_location"])]
    except:
        default_loc_abb = ""
    xweekevent["event_location_abbreviation"] = inquirer.text(
        message="Forma abreviada del lugar del evento:",
        default=default_loc_abb,
        completer={
            location_abb: None for location_abb in xweekconfig["event_locations_abbreviations"]},
        multicolumn_complete=True).execute()
    # --- 4. Versión del Evento
    xweekevent["event_version"] = inquirer.number(
        message="Versión del evento (Número)",
        validate=validator.EmptyInputValidator()
    ).execute()
    # --- 5. Dominio del Evento
    try:
        default_domain = xweekconfig["event_domains"][xweekconfig["event_names"].index(
            xweekevent["event_name"])]
    except:
        default_domain = xweekpastevent["event_domain"]
    xweekevent["event_domain"] = inquirer.text(
        message="Dominio Web del evento:",
          default=default_domain,
        completer={dom:None for dom in xweekconfig["event_domains"]},
        multicolumn_complete=True
    ).execute()

def create_event(xweekconfig, xweekevent, xweekpastevent):
    """Ayuda al usuario a crear el evento
    Args:
        xweekconfig (_type_): _description_
        xweekevent (_type_): _description_
        xweekpastevent (_type_): _description_
    """
    # --- 1. Nombre del Evento
    xweekevent["event_name"] = inquirer.text(
        message="Nombre del Evento:",
        default=xweekpastevent["event_name"],
        completer={name: None for name in xweekconfig["event_names"]},
        multicolumn_complete=True).execute()
    # --- 2. Lugar del Evento
    xweekevent["event_location"] = inquirer.text(
        message="Lugar del evento:",
        default=xweekpastevent["event_location"],
        completer={
            location: None for location in xweekconfig["event_locations"]},
        multicolumn_complete=True).execute()
    # --- 3. Abreviación del lugar del Evento
    try:
        default_loc_abb = xweekconfig["event_locations_abbreviations"][xweekconfig["event_locations"].index(
            xweekevent["event_location"])]
    except:
        default_loc_abb = ""
    xweekevent["event_location_abbreviation"] = inquirer.text(
        message="Forma abreviada del lugar del evento:",
        default=default_loc_abb,
        completer={
            location_abb: None for location_abb in xweekconfig["event_locations_abbreviations"]},
        multicolumn_complete=True).execute()
    # --- 4. Versión del Evento
    xweekevent["event_version"] = inquirer.number(
        message="Versión del evento (Número)",
        validate=validator.EmptyInputValidator()
    ).execute()
    # --- 5. Dominio del Evento
    try:
        default_domain = xweekconfig["event_domains"][xweekconfig["event_names"].index(
            xweekevent["event_name"])]
    except:
        default_domain = xweekpastevent["event_domain"]
    xweekevent["event_domain"] = inquirer.text(
        message="Dominio Web del evento:",
          default=default_domain,
        completer={dom:None for dom in xweekconfig["event_domains"]},
        multicolumn_complete=True
    ).execute()    

if __name__ == "__main__":
    main()
