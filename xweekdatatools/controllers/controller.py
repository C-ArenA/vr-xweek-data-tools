# For TYPE CHECKING ------------------
from __future__ import annotations
import datetime
import os
from pathlib import Path
from typing import TYPE_CHECKING
from tools.converters.docs2txt import docs2txt

if TYPE_CHECKING:
    from xweekdatatools.views import View
    from xweekdatatools.models import Model
# ------------------------------------

# ----------- IMPORTS ---------------
from xweekdatatools.app_constants import AppActions
from xweekdatatools.models.xweek_event import XweekEvent


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
        actions[AppActions.CONVERT_DOCS2TXT] = self.convert_docs2txt
        actions[AppActions.EXIT] = self.exit
        # Once the functionality is available we execute it
        if type(action) is AppActions:
            self.current_action = action
            actions[action](event)
        else:
            self.view.pending_functionality()


    # ------------------------- APP ACTIONS -------------------------

    def create_new_event(self, dumb_event = None):

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

    def exit(self, dumb=None):
        import sys

        sys.exit("Programa finalizado")
