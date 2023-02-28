# For TYPE CHECKING ------------------
from __future__ import annotations
import shutil
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from xweekdatatools.controllers import Controller
    from xweekdatatools.models import XweekRestaurant
    from xweekdatatools.models import XweekEvent
    from xweekdatatools.models import Model
# ------------------------------------

# ----------- IMPORTS ---------------
# ---------- PYTHON IMPORTS
import os
import json
import datetime
from pathlib import Path
# ---------- THIRD PARTY IMPORTS
from yachalk import chalk
from InquirerPy import inquirer, get_style, validator
from InquirerPy.base.control import Choice
# ---------- LOCAL IMPORTS
from xweekdatatools.utils.path_helpers import make_valid_path
from xweekdatatools.app_constants import TXT_FORMAT, AppActions
# -----------------------------------

# ---------- GLOBALS
style = get_style({"question": "#ff3355", "questionmark": "#ff3355",
                  "answer": "#0055ff"}, style_override=False)


class View:
    def __init__(self, controller: Controller = None) -> None:
        self.controller = controller

    def init_ui(self):
        """Genera el encabezado de la UI
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

    def show_rest_data(self, rest: XweekRestaurant, event: XweekEvent):
        print(chalk.red("Datos del restaurante para el evento:"))
        print(chalk.red(event.summary()))
        print(chalk.green(json.dumps(
            rest.json_serializable_dict(), indent=2, ensure_ascii=False)))

    def pending_functionality(self, *args):
        self.select_main_action(extra_message="Esa funcionalidad aún no está disponible 😓\nElija otra acción por favor")
    
    def write_confirmation(self):
        import sys
        print(chalk.red.bold("Está a punto de guardar algo en la base de datos"))
        if not inquirer.confirm(
            message="Desea continuar?"
        ).execute():
            sys.exit("Saliendo para no dañar la base de datos")
            
    #--------------------------------------------------------------
    # SECTION: ActionsUI ------------------------------------------
    #--------------------------------------------------------------
      
    def select_main_action(self, event: XweekEvent = None, extra_message: str = ""):
        self.init_ui()
        print(chalk.green(extra_message))
        action = inquirer.select(
            message="Elija una opción para proceder:",
            choices=[Choice(value=app_action, name=app_action.message())
                     for app_action in AppActions
                     if app_action != AppActions.SELECT_ACTION],
            default=AppActions.CREATE_NEW_EVENT,
            style=style
        ).execute()
        self.controller.choose_action(action, event)


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
            validate=validator.EmptyInputValidator(),
            default=xweeklastevent["version"]
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

    def select_entry(self, entries_list: list[Model]) -> int:
        """UI para seleccionar (por ID) una entrada de datos de una lista

        Args:
            entries_list (list[Model]): Lista de datos sobre los cuales seleccionar

        Returns:
            int: ID de la entrada seleccionado o None si nada fue seleccionado
        """
        choices = [Choice(entry.id, entry.summary()) for entry in entries_list]
        if len(entries_list) <= 0:
            return None
        return inquirer.select(
            message="Elija un " + entries_list[0].ENTRY_NAME,
            choices=choices,
            default=entries_list[-1].id,
            style=style
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
    
    def get_txts_lists(self) -> list[Path]:
        print(
            "En caso de ya tener los txts normalizados en una carpeta:")
        txts_folder = make_valid_path(inquirer.filepath(
            message="Dentro de qué carpeta desea buscar estos txts (Puede arrastrar y soltar):",
            only_directories=True
        ).execute())
        found_txts: list[Path] = list(txts_folder.rglob("*.txt"))
        return found_txts
    
    def show_rest_dishes_img_data(self, rest:XweekRestaurant):
        import pyperclip
        print(chalk.yellow("Existen " + str(len(rest.dishes)) + " Platos en " + rest.name))
        for dish in rest.dishes:
            print(chalk.blue.bold("---------------------------------"))
            print(chalk.blue.bold(dish["photo_name"]))
            print(chalk.blue.bold("---------------------------------"))
            pyperclip.copy(dish["photo_name"])
            print("Copiado al portapapeles")
            inquirer.confirm(
                message="Siguiente plato?"
            ).execute()
    
    def show_rest_logo_img_data(self, rest:XweekRestaurant):
        import pyperclip
        print(chalk.blue.bold("---------------------------------"))
        print(chalk.blue.bold(rest.logo_name))
        print(chalk.blue.bold("---------------------------------"))
        pyperclip.copy(rest.logo_name)
        print("Copiado al portapapeles")
        inquirer.confirm(
            message="Siguiente logo?"
        ).execute()
        
    def show_dishes_img_data(self, event:XweekEvent):
        self.init_ui()
        dish_counter = 0
        for rest in event.restaurants:
            dish_counter += len(rest.dishes)
        print(chalk.green("Existen " + str(len(event.restaurants)) + " Restaurantes en este evento"))
        print(chalk.red("Existen " + str(dish_counter) + " Platos en este evento"))
        event.restaurants = sorted(
            event.restaurants, key=lambda r: r.name)
        for rest in event.restaurants:
            self.show_rest_dishes_img_data(rest)
            
        inquirer.confirm(
            message="Continuar?"
        ).execute()
            
    
            
    
    def collect_images_ui(self) -> tuple[Path, list[Path]]:
        print(
            "Este es el asistente para recolectar imágenes dentro de una carpeta")
        img_src = make_valid_path(inquirer.filepath(
            message="Dentro de qué carpeta desea buscar las imágenes (Puede arrastrar y soltar):",
            only_directories=True
        ).execute())
        img_dst = make_valid_path(inquirer.filepath(
            message="En qué carpeta desea guadarlas (Puede arrastrar y soltar):",
            only_directories=True
        ).execute())
        found_imgs: list[Path] = list(img_src.rglob("*.jp*g")) + \
                                 list(img_src.rglob("*.png")) + \
                                 list(img_src.rglob("*.ai")) + \
                                 list(img_src.rglob("*.pdf")) + \
                                 list(img_src.rglob("*.psd"))
        if inquirer.confirm(
            message="Copiar los " + str(len(found_imgs)) + " archivos de imagen?"
        ):
            return img_dst, found_imgs                                 
        return img_dst, list()

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

    def normalize_txts(self, event: XweekEvent) -> bool:
        self.init_ui()
        print(chalk.red.bold(
            "Bienvenido al asistente para normalizar los txts del evento (manualmente)"))
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
                # editor.edit(filename=str(txt.absolute()))
                if os.system("code -w " + '"' + str(txt.absolute()) + '"') == 1:
                    print("-> VsCode no instalado en su máquina. Edite manualmente:")
                    print(chalk.red(str(txt.absolute())))
            return True
        return True

    def gen_event_json_prompt(self, event: XweekEvent) -> Path:
        self.init_ui()
        print(chalk.blue("Ahora generaremos el JSON del evento para usted"))
        print(event.summary())
        json_dst = make_valid_path(inquirer.filepath(
            message="Dentro de qué carpeta desea guardar el JSON del evento (Puede arrastrar y soltar):",
            only_directories=True
        ).execute())
        return json_dst

    def go_to_next_action_prompt(self, next_action: AppActions, event: XweekEvent = None, extra_message: str = ""):
        print(chalk.red(extra_message))
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
