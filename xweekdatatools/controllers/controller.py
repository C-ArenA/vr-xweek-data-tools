# For TYPE CHECKING ------------------
from __future__ import annotations
from typing import TYPE_CHECKING

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
        self.chosen_action = None
        self.current_event_id = None

    def set_view(self, view):
        self.view = view

    def set_model(self, model):
        self.model = model

    def start_app(self):
        self.view.select_main_action()

    def choose_action(self, action: AppActions):
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
        actions[AppActions.CREATE_NEW_EVENT] = self.create_new_event
        # Once the functionality is available we execute it
        if type(action) is AppActions:
            self.chosen_action = action
            actions[action]()
        else:
            self.view.pending_functionality()

    # ------------------------- APP ACTIONS -------------------------
    def create_new_event(self):
        
        self.view.insert_event_data(
            self.model.xweekconfig, self.model.last_event)

        if self.chosen_action == AppActions.COMPLETE_PROCESS:
            # Do the next thing
            pass

    def find_event_docs(self):
        print("Encontrando documentos en el último evento trabajado\n")
        current_event = XweekEvent.getAll()[-1]
        print("Dentro de la carpeta ", current_event.src_path.absolute())
        current_event.docs_path_list = current_event.src_path.rglob("*.doc*")
        current_event.save()
        
        
