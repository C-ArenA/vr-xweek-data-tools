from xweekdatatools.views import View
from xweekdatatools.controllers import Controller
from xweekdatatools.models import XweekEvent

def select_event_test():
    view = View(Controller())
    print(view.select_event(XweekEvent.getAll()))
    
select_event_test()