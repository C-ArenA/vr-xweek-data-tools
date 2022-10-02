import datetime

class Controller:
    def __init__(self, view=None, model=None) -> None:
        self.view = view
        self.model = model
    def set_view(self, view):
        self.view = view
    def set_model(self, model):
        self.model = model
    
    def create_event(self):
        new_event = {
            "event_created": datetime.datetime.now().strftime("%d%m%y_%H%M%S")
        }
        self.view.insert_event_data(self.model.get_config(), new_event, self.model.get_last_event_data())
        self.view.show_event_data(new_event)
        
if __name__ == "__main__":
    from xweekdatatools.views.view import View
    from xweekdatatools.models.model import Model

    controller = Controller()
    view = View(controller)
    model = Model(view, "db.json")
    controller.set_view(view)
    controller.set_model(model)
    
    view.select_main_action()
    
    
    