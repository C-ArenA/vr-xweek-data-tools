from xweekdatatools.controllers import Controller
from xweekdatatools.models import Model
from xweekdatatools.views import View

    
class App:
    def __init__(self) -> None:
        controller = Controller()
        view = View(controller)
        model = Model()
        model.set_view(view)
        controller.set_view(view)
        controller.set_model(model)
        controller.start_app()
