from xweekdatatools.views import XweekEventView
from xweekdatatools.models import XweekEvent

def show_event_test():
    xwev = XweekEventView()
    xwev.show_event(XweekEvent.getAll()[-1])
    
show_event_test()