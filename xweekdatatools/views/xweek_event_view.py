# For TYPE CHECKING ------------------
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from xweekdatatools.models import XweekEvent
# ------------------------------------
from yachalk import chalk

class XweekEventView:
    def __init__(self, app_controller=None) -> None:
        self.app_controller = app_controller
    
    # SHOW METHODS
    def show_event_summary(self, event:XweekEvent):
        print(chalk.blue.bold(event.summary() + "\n"))
        
    def show_event(self, event:XweekEvent):
        self.show_event_summary(event)
        for key in event.to_end_dict():
            print(key, "\n")
            
        if self.app_controller is None:
            print("Sin controlador esta vista es tonta, abortando aplicación")
            raise("Controlador de aplicación no asociado")
        else:
            self.app_controller.show_actions()
        
    