from dataclasses import dataclass, fields
from xweekdatatools.models.xweek_event import XweekEvent
from pathlib import Path
from pprint import pprint
from yachalk import chalk

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
    xwe = XweekEvent(1, "Burger---Week", "La Paz", 1, "http",
                     Path("f:/Vreality/xweek"), "bw", "lp")
    xwe.save()


def remove_event_test():
    XweekEvent.removeById(1)


def reset_events_test():
    XweekEvent.reset_all()


def json_serializable_test():
    xwe = XweekEvent.getAll()[-1]
    pprint(xwe.json_serializable_dict())
    
def general():
    xwe = XweekEvent()
    print(repr(xwe))

def json_correspondance_test():
    xwe = XweekEvent.getAll()[-1]
    pprint(xwe.print_fields_of_parent())
    
def check_xweek_event_fields():
    for field in fields(XweekEvent):
        print(chalk.red.bold(f'\n{field.name}:'))
        print(chalk.blue("------------------------------"))
        pprint(field)

def read_by_id_test():
    xwe = XweekEvent.getById(0)
    print(xwe)

read_by_id_test()