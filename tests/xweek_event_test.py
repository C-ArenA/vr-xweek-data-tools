from xweekdatatools.models.xweek_event import XweekEvent
from pathlib import Path
from pprint import pprint

def create_event_test():
    # Para crear un evento se deja el id sin especificar
    xwe = XweekEvent(
        name="Burger Week", 
        location="La Paz", 
        version=2, 
        domain="http", 
        src_path=Path("f:/Vreality/xweek"), 
        name_abbreviation="bw", 
        location_abbreviation="lp"
    )
    xwe.save()
    
def update_event_test():
    # Para actualizar un evento se especifica el ID del que se quiere actualizar
    xwe = XweekEvent(1, "Burger---Week", "La Paz", 1, "http", Path("f:/Vreality/xweek"), "bw", "lp")
    xwe.save()
    
def remove_event_test():
    XweekEvent.removeById(1)
    
def reset_events_test():
    XweekEvent.reset_all()

reset_events_test()