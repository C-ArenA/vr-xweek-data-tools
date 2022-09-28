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
last_event = xweeklast["xweekevent"]
xweekcurrent = copy.deepcopy(xweeklast)
current_event = xweekcurrent["xweekevent"]
xweekcurrent["xweeknow"] = datetime.datetime.now().strftime("%d%m%y_%H%M%S")


def main():
    while True:
        initrender()
        print("Estos son los datos actuales del evento:")
        print(chalk.green(json.dumps(
            current_event, indent=2, ensure_ascii=False)))

        if inquirer.confirm(message="Deseas actualizar estos datos?", style=style).execute():
            initrender()
            update_data(current_event)

        else:
            break


def initrender():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(chalk.blue.bold(
        "\n-------------------------------------------------------------"))
    print(chalk.blue.bold(
        "|😀 Bienvenido. Esta pequeña aplicación te ayudará a extraer |"))
    print(chalk.blue.bold(
        "|los datos de tu siguiente evento en un archivo JSON         |"))
    print(chalk.blue.bold(
        "-------------------------------------------------------------\n"))


def update_data(xweekevent):
    xweekevent["event_name"] = inquirer.text(
        message="Nombre del Evento:",
        default=last_event["event_name"],
        completer={name: None for name in xweekconfig["event_names"]},
        multicolumn_complete=True).execute()
    xweekevent["event_location"] = inquirer.text(
        message="Lugar del evento:",
        default=last_event["event_location"],
        completer={
            location: None for location in xweekconfig["event_locations"]},
        multicolumn_complete=True).execute()
    try:
        default = xweekconfig["event_locations_abbreviations"][xweekconfig["event_locations"].index(
            xweekevent["event_location"])]
    except:
        default = ""
    xweekevent["event_location_abbreviation"] = inquirer.text(
        message="Forma abreviada del lugar del evento:",
        default=default,
        completer={
            location_abb: None for location_abb in xweekconfig["event_locations_abbreviations"]},
        multicolumn_complete=True).execute()

    xweekevent["event_version"] = inquirer.number(
        message="Versión del evento (Número)",
        validate=validator.EmptyInputValidator()
    ).execute()


if __name__ == "__main__":
    main()
