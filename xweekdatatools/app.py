from xweekdatatools.controllers import Controller
from xweekdatatools.views import View
import logging
    
class App:
    def __init__(self) -> None:
        controller = Controller()
        view = View(controller)
        controller.set_view(view)
        controller.start_app()
        logging.info("App")
