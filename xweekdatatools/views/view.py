# For TYPE CHECKING ------------------
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from xweekdatatools.controllers import Controller
# ------------------------------------

import os
import json
from pathlib import Path
from yachalk import chalk
from InquirerPy import inquirer, get_style, validator
from InquirerPy.base.control import Choice
style = get_style({"question": "#ff3355", "questionmark": "#ff3355",
                  "answer": "#0055ff"}, style_override=False)


class View:
    def __init__(self, controller: Controller) -> None:
        self.controller = controller

    def init_ui(self):
        """
        Genera el encabezado de la UI
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

    def show_event_data(self, event_data: dict):
        self.init_ui()
        print(
            f'Estos son los datos del evento "{event_data["event_name"]}" - "{event_data["event_location"]}" Versión {event_data["event_version"]}, creado el {event_data["event_created"]}:')
        print(chalk.green(json.dumps(event_data, indent=2, ensure_ascii=False)))

    def select_main_action(self):
        self.init_ui()
        action = inquirer.select(
            message="Elija una opción para proceder:",
            choices=[
                Choice(0, "REALIZAR PROCESO COMPLETO", enabled=True),
                Choice(1, "Crear nuevo evento"),
                Choice(2, "Actualizar datos del evento"),
                Choice(3, "Encontrar docs del evento"),
                Choice(30, "Actualizar lista de docs del evento"),
                Choice(4, "Encontrar y copiar docs del evento"),
                Choice(5, "Encontrar imágenes del evento"),
                Choice(6, "Encontrar y copiar imágenes del evento"),
                Choice(7, "Convertir docs a texto plano"),
                Choice(8, "Normalizar textos planos manualmente"),
                Choice(9, "Convertir texto plano a datos de restaurantes del evento"),
                Choice(10, "Generar JSON del evento"),
                Choice(11, "Generar CSV y XLSX de urls de los restaurantes"),
                Choice(12, "Generar QRs los restaurantes")
            ],
            default=0,
            style=style
        ).execute()
        if action == 1:
            print("CREAR!!!\n")
            self.controller.create_event()

    def insert_event_data(self, xweekconfig, xweekevent, xweekpastevent):
        """Ayuda al usuario a actualizar los datos del evento

        Args:
            xweekconfig (_type_): Objeto config de la aplicación
            xweekevent (_type_): Evento nuevo
            xweekpastevent (_type_): Último evento registrado
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
            completer={dom: None for dom in xweekconfig["event_domains"]},
            multicolumn_complete=True
        ).execute()

    def no_model(self, db_path: Path):
        self.init_ui()
        print(chalk.red.bold(
            "ERROR GRAVE: No se pudo conectar con la base de datos en " + str(db_path)))
        print(chalk.red("Ejecución abortada"))

    def has_model(self, db_path: Path):
        self.init_ui()
        print(chalk.green.bold(
            "Base de datos conectada exitosamente en: " + str(db_path)))


if __name__ == "__main__":
    view = View()
    view.init_ui()
