from xweekdatatools.models import XweekEvent
from xweekdatatools.app_constants import AppActions

class XweekEventController:
    def __init__(self) -> None:
        pass
    
    def create_new_event(self) -> XweekEvent:
        self.view.insert_event_data(
            self.model.xweekconfig, self.model.last_event)

        if self.chosen_action == AppActions.COMPLETE_PROCESS:
            # Do the next thing
            pass

    def find_event_docs(self, event_id=None):
        if event_id is None:
            # Debo encontrar un id por mi cuenta
            # Si no se puede obtener id, regreso a la vista main
            pass
        # Con el event_id procedo a buscar los documentos
        print("Encontrando documentos en el último evento trabajado\n")
        current_event = XweekEvent.getAll()[-1]
        print("Dentro de la carpeta ", current_event.src_path.absolute())
        current_event.docs_path_list = current_event.src_path.rglob("*.doc*")
        current_event.save()