# For TYPE CHECKING ------------------
from __future__ import annotations
from re import A
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from xweekdatatools.views import View
    from xweekdatatools.models import Model
# ------------------------------------

# ----------- IMPORTS ---------------
import datetime
from xweekdatatools.app_constants import AppActions


class Controller:
    """Controlador Principal de XWEEKTOOLS
    """

    def __init__(self, view: View = None, model: Model = None) -> None:
        self.view = view
        self.model = model
        self.chosen_action = None

    def set_view(self, view):
        self.view = view

    def set_model(self, model):
        self.model = model

    def start_app(self):
        self.view.select_main_action()

    def create_new_event(self):
        new_event = {
            "event_created": datetime.datetime.now().strftime("%d%m%y_%H%M%S")
        }
        self.view.insert_event_data(self.model.get_config(
        ), new_event, self.model.get_last_event_data())
        self.view.show_event_data(new_event)

    def choose_action(self, action: AppActions):
        actions = {
            appAction: self.view.pending_functionality for appAction in AppActions
        }
        actions[AppActions.CREATE_NEW_EVENT] = self.create_new_event
        if type(action) is AppActions:
            self.chosen_action = action
            actions[action]()
        else:
            self.view.pending_functionality()
