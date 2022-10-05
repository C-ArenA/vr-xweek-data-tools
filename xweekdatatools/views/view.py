# For TYPE CHECKING ------------------
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from xweekdatatools.controllers import Controller
    from xweekdatatools.models import XweekEvent
# ------------------------------------

import os
import json
from pathlib import Path
from yachalk import chalk
from InquirerPy import inquirer, get_style, validator
from InquirerPy.base.control import Choice
style = get_style({"question": "#ff3355", "questionmark": "#ff3355",
                  "answer": "#0055ff"}, style_override=False)

from xweekdatatools.app_constants import AppActions

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
        print('Estos son los datos del evento',
              f'"{event_data["event_name"]}" - "{event_data["event_location"]}"',
              f'Versión {event_data["event_version"]}, creado el {event_data["event_created"]}:')
        print(chalk.green(json.dumps(event_data, indent=2, ensure_ascii=False)))

    def select_main_action(self):

        self.init_ui()
        action = inquirer.select(
            message="Elija una opción para proceder:",
            choices=[
                Choice(AppActions.COMPLETE_PROCESS,
                       "REALIZAR PROCESO COMPLETO", enabled=True),
                Choice(AppActions.CREATE_NEW_EVENT, "Crear nuevo evento"),
                Choice(AppActions.UPDATE_EVENT_DATA,
                       "Actualizar datos del evento"),
                Choice(AppActions.FIND_EVENT_DOCS,
                       "Encontrar docs del evento"),
                Choice(AppActions.UPDATE_EVENT_DOCS_LIST,
                       "Actualizar lista de docs del evento"),
                Choice(-1, "Encontrar y copiar docs del evento"),
                Choice(AppActions.FIND_EVENT_IMAGES,
                       "Encontrar imágenes del evento"),
                Choice(AppActions.COLLECT_EVENT_IMAGES,
                       "Encontrar y copiar imágenes del evento"),
                Choice(AppActions.CONVERT_DOCS2TXT,
                       "Convertir docs a texto plano"),
                Choice(AppActions.NORMALIZE_TXT,
                       "Normalizar textos planos manualmente"),
                Choice(AppActions.CONVERT_TXT2DATA,
                       "Convertir texto plano a datos de restaurantes del evento"),
                Choice(AppActions.GEN_EVENT_JSON, "Generar JSON del evento"),
                Choice(AppActions.GEN_EVENT_XLSX,
                       "Generar CSV y XLSX de urls de los restaurantes"),
                Choice(AppActions.GEN_EVENT_QRS,
                       "Generar QRs los restaurantes"),
                Choice(AppActions.EXIT, "SALIR")
            ],
            default=AppActions.COMPLETE_PROCESS,
            style=style
        ).execute()
        self.controller.choose_action(action)

    def pending_functionality(self):
        print("No podemos hacer eso aún :(")
        print("Elija otra opción por favor")
        self.select_main_action()

    def insert_event_data(self, xweekconfig, xweeklastevent):
        """Ayuda al usuario a actualizar los datos del evento

        Args:
            xweekconfig (_type_): Objeto config de la aplicación
            xweekpastevent (_type_): Último evento registrado
        """
        xweekevent = {}
        # --- 1. Nombre del Evento
        xweekevent["name"] = inquirer.text(
            message="Nombre del Evento:",
            default=xweeklastevent["name"],
            completer={
                default["name"]: None for default in xweekconfig["event_defaults"]},
            multicolumn_complete=True).execute()
        # --- 2. Lugar del Evento
        xweekevent["event_location"] = inquirer.text(
            message="Lugar del evento:",
            default=xweeklastevent["event_location"],
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
            default_domain = xweeklastevent["event_domain"]
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

    def select_event(self, events_list: list[XweekEvent]) -> int:
        """UI para seleccionar (por ID) un evento de una lista de eventos

        Args:
            events_list (list[XweekEvent]): Lista de eventos sobre los cuales seleccionar

        Returns:
            int: ID del evento seleccionado o None si nada fue seleccionado
        """
        choices = [Choice(event.id, event.summary()) for event in events_list]
        return inquirer.select(
            message="Seleccione el evento sobre el cual trabajar",
            choices=choices,
            default=events_list[-1].id
        ).execute()
        

    def find_docs_ui(self, current_event=None):
        if current_event is None:
            current_event = self.select_event()

        print(
            "Este es el asistente para encontrar los archivos word dentro de una carpeta")
        src_path = inquirer.filepath(
            message="Dentro de qué carpeta desea buscar los archivos de word (Puede arrastrar y soltar):",
            only_directories=True
        ).execute()
        found_docs = current_event.src_path.rglob("*.doc*")
        accepted_docs = []
        print(
            f'Se encontraron {len(found_docs)} documentos de word dentro de la carpeta {src_path}\n')
        if len(found_docs) > 0:
            print(
                f'A continuación deseleccione los documentos que están por demás (con tecla espacio), deje seleccionados los demás\n')

            accepted_docs = inquirer.checkbox(
                message="Deseleccione docs innecesarios:",
                choices=[Choice(doc, name=doc["file"], enabled=True)
                         for doc in found_docs]
            ).execute()

        extradoc = inquirer.confirm(
            message="Desea ingresar doc extra manualmente?"
        ).execute()
        while extradoc:
            new_file = inquirer.filepath(
                message="Ingrese doc extra manualmente (Puede arrastrar):",
                only_files=True,
            ).execute()
            file_name, file_ext = os.path.splitext(new_file)
            if file_ext[:4] == ".doc":
                accepted_docs.append({
                    "path": new_file,
                    "file": os.path.basename(new_file),
                    "name": file_name,
                    "ext": file_ext
                })
            else:
                print(
                    "El archivo no es de tipo documento de word, no se acepta\n")
            extradoc = inquirer.confirm(
                message="Desea ingresar otro doc extra manualmente?"
            ).execute()
        print("Los documentos encontrados finales son:\n")
        for doc in accepted_docs:
            print(doc["path"])
        return accepted_docs


if __name__ == "__main__":
    view = View()
    view.init_ui()
