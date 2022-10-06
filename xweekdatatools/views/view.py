# For TYPE CHECKING ------------------
from __future__ import annotations
import datetime
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
from xweekdatatools.utils.path_helpers import make_valid_path

class View:
    def __init__(self, controller: Controller = None) -> None:
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
        xweekevent["location"] = inquirer.text(
            message="Lugar del evento:",
            default=xweeklastevent["location"],
            completer={
                location["name"]: None for location in xweekconfig["event_default_locations"]},
            multicolumn_complete=True).execute()
        # --- 3. Abreviación del lugar del Evento
        try:
            default_loc_abb = ""
            for def_loc in xweekconfig["event_default_locations"]:
                if def_loc["name"] == xweekevent["location"]:
                    default_loc_abb = def_loc["abbreviation"]
        except:
            default_loc_abb = ""
        xweekevent["location_abbreviation"] = inquirer.text(
            message="Forma abreviada del lugar del evento:",
            default=default_loc_abb,
            completer={
                location["abbreviation"]: None for location in xweekconfig["event_default_locations"]},
            multicolumn_complete=True).execute()
        # --- 4. Versión del Evento
        xweekevent["version"] = inquirer.number(
            message="Versión del evento (Número)",
            validate=validator.EmptyInputValidator()
        ).execute()
        # --- 5. Dominio del Evento
        try:
            default_domain = xweeklastevent["domain"]
            for event_def in xweekconfig["event_defaults"]:
                if event_def["name"] == xweekevent["name"]:
                    default_domain = event_def["domain"]
        except:
            default_domain = xweeklastevent["domain"]
        xweekevent["domain"] = inquirer.text(
            message="Dominio Web del evento:",
            default=default_domain,
            completer={ev_def["domain"]: None for ev_def in xweekconfig["event_defaults"]},
            multicolumn_complete=True
        ).execute()
        
        # --- 5. URL de medios
        
        default_domain = xweekevent["domain"] + "/wp-content/uploads/" + datetime.datetime.now().strftime("%Y/%m")
        xweekevent["media_url"] = inquirer.text(
            message="URL de medios (Imágenes):",
            default=default_domain,
            completer={ev_def["domain"] + "/wp-content/uploads/" + datetime.datetime.now().strftime("%Y/%m"): None for ev_def in xweekconfig["event_defaults"]},
            multicolumn_complete=True
        ).execute()
        print(xweekevent)
        return xweekevent

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
        

    def find_docs_ui(self, current_event:XweekEvent) -> list[Path]:
        print(
            "Este es el asistente para encontrar los archivos word dentro de una carpeta")
        current_event.src_path = make_valid_path(inquirer.filepath(
            message="Dentro de qué carpeta desea buscar los archivos de word (Puede arrastrar y soltar):",
            only_directories=True
        ).execute())
        found_docs:list[Path] = list(current_event.src_path.rglob("*.doc*"))
        accepted_docs = []
        print(
            f'Se encontraron {len(found_docs)} documentos de word dentro de la carpeta {current_event.src_path}\n')
        if len(found_docs) > 0:
            print(
                f'A continuación deseleccione los documentos que están por demás (con tecla espacio), deje seleccionados los demás\n')

            accepted_docs = inquirer.checkbox(
                message="Deseleccione docs innecesarios:",
                choices=[Choice(doc, name=str(doc), enabled=True)
                         for doc in found_docs]
            ).execute()

        extradoc = inquirer.confirm(
            message="Desea ingresar doc extra manualmente?"
        ).execute()
        while extradoc:
            new_file = make_valid_path(inquirer.filepath(
                message="Ingrese doc extra manualmente (Puede arrastrar):",
                only_files=True,
            ).execute())
            file_name, file_ext = os.path.splitext(new_file)
            if new_file.suffix[:4] == ".doc":
                accepted_docs.append(new_file)
            else:
                print(
                    "El archivo no es de tipo documento de word, no se acepta\n")
            extradoc = inquirer.confirm(
                message="Desea ingresar otro doc extra manualmente?"
            ).execute()
        print("Los documentos encontrados finales son:\n")
        for doc in accepted_docs:
            print(str(doc))
        return accepted_docs

    def convert_docs2txt_ui(self, event: XweekEvent)-> bool:
        self.init_ui()
        print("Ahora se procede a convertir los siguientes docs en txts:")
        for doc in event.docs_path_list:
            print(str(doc.absolute()))
        return inquirer.confirm(
            message="Proceder? O Cancelar? (Y/n)"
        ).execute()
        
    def overwrite_folder_prompt(self, folder_children_list: list[Path]) -> bool:
        """Ayuda a decidir si se sobreescribe la carpeta en la que están los 
        elementos de la lista

        Args:
            folder_children_list (list[Path]): lista de paths cuyo padre decidimos

        Returns:
            Path: path donde escribir finalmente
        """
        if len(folder_children_list) <= 0:
            return False
        old_parent = folder_children_list[0].parent
        overwrite = inquirer.confirm(
            message="Desea sobreescribir los archivos en "  + str(old_parent.absolute()) + "?",
        ).execute()
        if overwrite:
            return old_parent
        return False
            
        
        

if __name__ == "__main__":
    view = View()
    view.init_ui()
