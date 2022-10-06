from __future__ import annotations
from dataclasses import asdict, dataclass, field, fields
from mimetypes import init
from pathlib import Path

from xweekdatatools.models.xweek_restaurant import XweekRestaurant
from xweekdatatools.models import Model
from xweekdatatools.utils import make_valid_path, json_serializable_path
from xweekdatatools.utils.data_helpers import cardinal_to_ordinal

@dataclass
class XweekEvent(Model):
    MODEL_NAME_IN_JSON = "xweekevents"
    # ********* Mandatory ***********:
    name: str = field(
        default="", 
        metadata={
            "input_msg": "Ingrese el nombre del Evento",
            "default": "Burger Week",
            "config": "xweekconfig"
            })
    location: str = ""
    version: int = 0
    domain: str = ""
    src_path: Path = None
    # Can be calculated
    name_abbreviation: str = ""
    location_abbreviation: str = ""
    # Can work without it
    media_url: str = ""
    long_description: str = "Disfruta de este evento"
    short_description: str = "Disfruta"
    calendar: str = "Del x al y del z"
    # Optional or should be defined after creation
    restaurants: list[XweekRestaurant] = field(default_factory=list)
    
    dst_path: Path = None
    docs_path_list: list[Path] = field(default_factory=list, metadata="a")
    txts_path_list: list[Path] = field(default_factory=list, metadata={"a":5})
        
    # SECTION ------------ DB OPERATIONS -----------------

    @classmethod
    def getAll(cls) -> list[XweekEvent]:
        cls.db_load()
        events = []
        for event in cls.db[XweekEvent.MODEL_NAME_IN_JSON]:
            # Sólo se añaden a la lista si son datos válidos
            try:
                events.append(cls(**event))
            except:
                pass                
        return events


    @classmethod
    def removeById(cls, id):
        cls.db_load()
        index_to_remove = None
        for i, event in enumerate(cls.db[XweekEvent.MODEL_NAME_IN_JSON]):
            if event["id"] == id:
                index_to_remove = i
        cls.db[XweekEvent.MODEL_NAME_IN_JSON].pop(index_to_remove)
        cls.db_save()

    @classmethod
    def reset_all(cls):
        """Resetea toda la lista de eventos (CUIDADO!)
        """
        cls.db_load()
        cls.db[XweekEvent.MODEL_NAME_IN_JSON] = [cls(id=0).to_end_dict()]
        cls.db_save()

    def save(self):
        """Guarda la instancia del evento (nuevo o actualizado) en la base de datos
        * Es nuevo si su id no existe ya en los otros eventos
        * Es actualizado si su id consiste con alguno
        """
        self.db_load()
        # Si el ID del evento no es válido (es None o no es int) se aborta
        if type(self.id) != int:
            print(f'Evento no pudo ser creado por ID inválido')
            return
        # Se actualiza evento si ID ya existe
        for index, event in enumerate(self.getAll()):
            if event.id == self.id:
                self.db[XweekEvent.MODEL_NAME_IN_JSON][index] = self.json_serializable_dict()
                self.db_save()
                print(f'Evento {event.id} actualizado')
                return
        # Se crea evento si ID no existe
        self.db[XweekEvent.MODEL_NAME_IN_JSON].append(self.json_serializable_dict())
        self.db_save()
        print(f'Evento {self.id} creado')

    # SECTION ------------ DATA OPERATIONS -----------------
    
    def get_version(self):
        return self.location_abbreviation + "-" + cardinal_to_ordinal(self.version)
        
    def summary(self) -> str:
        """Devuelve un pequeño resumen de una instancia del evento

        Returns:
            str: Resumen de la instancia del evento
        """
        return f'{self.id}: {self.name} {self.location}, versión: {self.version}, modified: {self.modified}'
