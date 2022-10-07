# For TYPE CHECKING ------------------
from __future__ import annotations
from xweekdatatools.utils.path_helpers import make_valid_path
from xweekdatatools.app_constants import TXT_FORMAT, AppActions
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
              f'"{event_data["name"]}" - "{event_data["location"]}"',
              f'Versión {event_data["version"]}, creado el {event_data["created"]}:')
        print(chalk.green(json.dumps(event_data, indent=2, ensure_ascii=False)))

    def select_main_action(self, event:XweekEvent=None, extra_message:str=""):

        self.init_ui()
        print(chalk.green(extra_message))
        action = inquirer.select(
            message="Elija una opción para proceder:",
            choices=[Choice(app_action, app_action.message()) for app_action in AppActions if app_action != AppActions.SELECT_ACTION],
            default=AppActions.CREATE_NEW_EVENT,
            style=style
        ).execute()
        self.controller.choose_action(action, event)

    def pending_functionality(self, *args):
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
            completer={
                ev_def["domain"]: None for ev_def in xweekconfig["event_defaults"]},
            multicolumn_complete=True
        ).execute()

        # --- 5. URL de medios

        default_domain = xweekevent["domain"] + "/wp-content/uploads/" + \
            datetime.datetime.now().strftime("%Y/%m")
        xweekevent["media_url"] = inquirer.text(
            message="URL de medios (Imágenes):",
            default=default_domain,
            completer={ev_def["domain"] + "/wp-content/uploads/" + datetime.datetime.now(
            ).strftime("%Y/%m"): None for ev_def in xweekconfig["event_defaults"]},
            multicolumn_complete=True
        ).execute()
        
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

    def find_docs_ui(self, current_event: XweekEvent) -> list[Path]:
        print(
            "Este es el asistente para encontrar los archivos word dentro de una carpeta")
        current_event.src_path = make_valid_path(inquirer.filepath(
            message="Dentro de qué carpeta desea buscar los archivos de word (Puede arrastrar y soltar):",
            only_directories=True
        ).execute())
        found_docs: list[Path] = list(current_event.src_path.rglob("*.doc*"))
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

    def convert_docs2txt_ui(self, event: XweekEvent) -> bool:
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
            message="Desea sobreescribir los archivos en " +
            str(old_parent.absolute()) + "?",
        ).execute()
        if overwrite:
            return old_parent
        return False

    def normalize_txts(self, event:XweekEvent) -> bool:
        self.init_ui()
        print(chalk.red.bold("Bienvenido al asistente para normalizar los txts del evento (manualmente)"))
        print("Recuerde que el programa prenormaliza los txts y que")
        print("si los docs siguen la plantilla, la normalización automática es suficiente")
        print("Recuerde que se debe seguir el siguiente formato:")
        print(chalk.blue(TXT_FORMAT))
        print(chalk.red.bold("\n----------------\n"))
        if inquirer.confirm(
            message="Comenzar la normalización? O abortar"
        ).execute():
            if len(event.txts_path_list) <= 0:
                print("No existen txts para normalizar")
                return False
            for txt in event.txts_path_list:
                #editor.edit(filename=str(txt.absolute()))    
                if os.system("code -w " + '"' + str(txt.absolute()) + '"') == 1:
                   print("-> VsCode no instalado en su máquina. Edite manualmente:") 
                   print(chalk.red(str(txt.absolute()))) 
            return True
        return True
    
    def go_to_next_action_prompt(self, next_action: AppActions, event: XweekEvent = None):
        print(chalk.red("-------------------------------"))
        action = inquirer.select(
            message="Elija una acción para continuar:",
            choices=[
                Choice(next_action, next_action.message()),
                Choice(AppActions.SELECT_ACTION, "Prompt inicial"),
                Choice(AppActions.EXIT, "Salir")
            ]
        ).execute()
        self.controller.choose_action(action, event)


if __name__ == "__main__":
    view = View()
    view.init_ui()
