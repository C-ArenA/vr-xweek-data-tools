# For TYPE CHECKING ------------------
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from xweekdatatools.views import View
    from xweekdatatools.models import Model
# ------------------------------------

# ----------- IMPORTS ---------------
import datetime


class Controller:
    """Controlador Principal de XWEEKTOOLS
    """

    def __init__(self, view: View = None, model: Model = None) -> None:
        self.view = view
        self.model = model

    def set_view(self, view):
        self.view = view

    def set_model(self, model):
        self.model = model

    def start_app(self):
        self.view.select_main_action()

    def create_event(self):
        new_event = {
            "event_created": datetime.datetime.now().strftime("%d%m%y_%H%M%S")
        }
        self.view.insert_event_data(self.model.get_config(
        ), new_event, self.model.get_last_event_data())
        self.view.show_event_data(new_event)
