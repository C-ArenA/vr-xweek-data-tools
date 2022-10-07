# For TYPE CHECKING ------------------
from __future__ import annotations
from typing import TYPE_CHECKING

from xweekdatatools.models.xweek_restaurant import XweekRestaurant
if TYPE_CHECKING:
    from xweekdatatools.views import View
    from xweekdatatools.models import Model
# ------------------------------------

# ----------- IMPORTS ---------------
# ---------- PYTHON IMPORTS
import datetime
from pathlib import Path
# ---------- THIRD PARTY IMPORTS

# ---------- LOCAL IMPORTS
from xweekdatatools.app_constants import AppActions
from xweekdatatools.models.xweek_event import XweekEvent
from xweekdatatools.utils import docs2txt


class Controller:
    """Controlador Principal de XWEEKTOOLS
    """

    def __init__(self, view: View = None, model: Model = None) -> None:
        self.view = view
        self.model = model
        self.current_action = None
        self.current_event_id = None

    def set_view(self, view):
        self.view = view

    def set_model(self, model):
        self.model = model

    def start_app(self):
        self.view.select_main_action()

    def choose_action(self, action: AppActions, event):
        """#Router of the application.
        It gets an action from the view and transforms it to some functionality
        or shows a pending_functionality message if no functionality is available yet

        Args:
            action (AppActions): acción que se desea traducir en una funcionalidad
        """
        # By default all actions relate to a pending_functionality
        actions = {
            appAction: self.view.pending_functionality for appAction in AppActions
        }
        # Here we manually define the bindings: action-functionality
        actions[AppActions.SELECT_ACTION] = self.view.select_main_action
        actions[AppActions.CREATE_NEW_EVENT] = self.create_new_event
        actions[AppActions.UPDATE_EVENT_DATA] = self.update_event
        actions[AppActions.FIND_EVENT_DOCS] = self.find_event_docs
        actions[AppActions.UPDATE_EVENT_DOCS_LIST] = self.find_event_docs
        actions[AppActions.FIND_EVENT_IMAGES] = self.find_event_images
        actions[AppActions.COLLECT_EVENT_IMAGES] = self.collect_event_images
        actions[AppActions.CONVERT_DOCS2TXT] = self.convert_docs2txt
        actions[AppActions.NORMALIZE_TXT] = self.normalize_txt
        actions[AppActions.CONVERT_TXT2DATA] = self.convert_txt2data
        actions[AppActions.GEN_EVENT_JSON] = self.gen_event_json
        actions[AppActions.GEN_EVENT_CSV] = self.gen_event_csv
        actions[AppActions.GEN_EVENT_XLSX] = self.gen_event_xlsx
        actions[AppActions.GEN_EVENT_QRS] = self.gen_event_qrs
        actions[AppActions.EXIT] = self.exit
        # Once the functionality is available we execute it
        if type(action) is AppActions:
            self.current_action = action
            actions[action](event)
        else:
            self.view.pending_functionality()

    # ------------------------- APP ACTIONS -------------------------

    def create_new_event(self, dumb_event=None):

        new_xwe_dict = self.view.insert_event_data(
            self.model.db["xweekconfig"], XweekEvent.getAll()[-1].json_serializable_dict())
        new_xwe = XweekEvent(**new_xwe_dict)
        new_xwe.save()
        self.view.go_to_next_action_prompt(AppActions.FIND_EVENT_DOCS, new_xwe)

    def update_event(self, event: XweekEvent = None):
        if event is None:
            event = XweekEvent.getById(
                self.view.select_event(XweekEvent.getAll()))
        new_xwe_dict = self.view.insert_event_data(
            self.model.db["xweekconfig"], event.json_serializable_dict())
        new_xwe_dict["id"] = event.id
        new_xwe = XweekEvent(**new_xwe_dict)
        self.view.show_event_data(new_xwe.json_serializable_dict())
        new_xwe.save()
        self.view.go_to_next_action_prompt(AppActions.FIND_EVENT_DOCS, new_xwe)

    def find_event_docs(self, event: XweekEvent = None):
        if event is None:
            event = XweekEvent.getById(
                self.view.select_event(XweekEvent.getAll()))
        docs = self.view.find_docs_ui(event)
        event.docs_path_list = docs
        event.save()
        self.view.go_to_next_action_prompt(AppActions.CONVERT_DOCS2TXT, event)

    def convert_docs2txt(self, event: XweekEvent = None):

        if event is None:
            event = XweekEvent.getById(
                self.view.select_event(XweekEvent.getAll()))
        if self.view.convert_docs2txt_ui(event):
            overwrite = self.view.overwrite_folder_prompt(event.txts_path_list)
            if overwrite:
                temp_path = overwrite
            else:
                temp_path = Path(
                    "./TEMP/txts/" + datetime.datetime.now().strftime("%d%m%Y_%H%M%S") + "/")
            try:
                temp_path.mkdir(parents=True)
            except FileExistsError:
                print("Sobreescribiendo txts en: " + str(temp_path.absolute))

            event.txts_path_list = docs2txt(event.docs_path_list, temp_path)
            event.save()
        self.view.go_to_next_action_prompt(AppActions.NORMALIZE_TXT, event)

    def normalize_txt(self, event: XweekEvent = None):

        if event is None:
            event = XweekEvent.getById(
                self.view.select_event(XweekEvent.getAll()))
        for txt in event.txts_path_list:
            if txt.exists:
                pass
            else:
                raise ("No existe el archivo al que se apunta en la base de datos")
        normalized = self.view.normalize_txts(event)
        if normalized:
            self.view.go_to_next_action_prompt(
                AppActions.CONVERT_TXT2DATA, event)
            return
        self.view.select_main_action(None, "No habían txts para normalizar")

    def convert_txt2data(self, event: XweekEvent = None):
        if event is None:
            event = XweekEvent.getById(
                self.view.select_event(XweekEvent.getAll()))
        # Vacío el evento de restaurantes
        self.view.write_confirmation()
        event.restaurants = []
        event.save()
        for txt in event.txts_path_list:
            with txt.open('r', encoding='utf-8') as f:
                new_rest = XweekRestaurant.from_text(event, f.read())
                try:
                    new_rest.order = txt.stem.split(".")[0]
                except:
                    new_rest.order = None                    
                event.restaurants.append(new_rest)
                event.save()
        # self.view.show_rest_data(rest, event)
        # input("txt2data: Continuar?")
        self.view.go_to_next_action_prompt(AppActions.GEN_EVENT_JSON, event)

    def gen_event_json(self, event: XweekEvent = None):
        import json
        if event is None:
            event = XweekEvent.getById(
                self.view.select_event(XweekEvent.getAll()))
            
        json_container = self.view.gen_event_json_prompt(event)
        if not json_container.exists():
            self.view.go_to_next_action_prompt(AppActions.GEN_EVENT_JSON, event, "La carpeta no existe, pero puede volver a itentar:")
        if not json_container.is_dir():
            self.view.go_to_next_action_prompt(AppActions.GEN_EVENT_JSON, event, "Debe darme la dirección de una carpeta, no de un archivo. Puede volver a intentar:")
        json_name = datetime.datetime.now().strftime("%d%m%y_%H%M%S") + "-" + event.name_abbreviation + "-" + event.get_version() + ".json"
        json_path = json_container / json_name
        json_dict = event.json_serializable_dict()
        json_dict["restaurants"] = sorted(json_dict["restaurants"], key=lambda r: r["name"])
        with json_path.open("w", encoding="utf-8") as json_file:
            json.dump(json_dict, json_file, ensure_ascii=False, indent=4)
        
        self.view.go_to_next_action_prompt(AppActions.GEN_EVENT_CSV, event, "JSON Generado exitosamente en: " + str(json_path.absolute()))

    def gen_event_csv(self, event: XweekEvent = None):
        if event is None:
            event = XweekEvent.getById(
                self.view.select_event(XweekEvent.getAll()))
        self.view.pending_functionality()

    def gen_event_xlsx(self, event: XweekEvent = None):
        if event is None:
            event = XweekEvent.getById(
                self.view.select_event(XweekEvent.getAll()))
        self.view.pending_functionality()

    def gen_event_qrs(self, event: XweekEvent = None):
        if event is None:
            event = XweekEvent.getById(
                self.view.select_event(XweekEvent.getAll()))
        self.view.pending_functionality()
    def find_event_images(self, event: XweekEvent = None):
        if event is None:
            event = XweekEvent.getById(
                self.view.select_event(XweekEvent.getAll()))
        self.view.pending_functionality()
    def collect_event_images(self, event: XweekEvent = None):
        if event is None:
            event = XweekEvent.getById(
                self.view.select_event(XweekEvent.getAll()))
        self.view.pending_functionality()

    def exit(self, dumb=None):
        import sys

        sys.exit("Programa finalizado")
