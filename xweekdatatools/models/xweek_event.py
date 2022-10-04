from __future__ import annotations
from dataclasses import asdict, dataclass, field
from pathlib import Path
import datetime
from xweekdatatools.models.xweek_restaurant import XweekRestaurant

from xweekdatatools.models import Model
import json
import sys


@dataclass
class XweekEvent(Model):
    # ********* Mandatory ***********:
    id: int = None
    name: str = ""
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
    created: str = datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")
    modified: str = datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")
    dst_path: Path = None
    docs_path_list: list[Path] = field(default_factory=list)
    txts_path_list: list[Path] = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()
        self.id = self.__next_id() if self.id is None else self.id

    @classmethod
    def getAll(cls) -> list[XweekEvent]:
        db = cls.get_current_db_state()
        return [cls(**event) for event in db["xweekevents"]]

    @classmethod
    def getById(cls, id) -> XweekEvent:
        db = cls.get_current_db_state()
        for event in db["xweekevents"]:
            if event["id"] == id:
                return cls(**event)
        return None
    
    @classmethod
    def removeById(cls, id):
        cls.db = cls.get_current_db_state()
        index_to_remove = None
        for i, event in enumerate(cls.db["xweekevents"]):
            if event["id"] == id:
                index_to_remove = i                
        cls.db["xweekevents"].pop(index_to_remove)
        super().save(cls)


    
    def to_dict(self):
        """Devuelve un diccionario con todos los atributos a 
        excepción de aquellos de la clase padre"""
        current_dict = asdict(self)
        for key in super().__dataclass_fields__.keys():
            del current_dict[key]
        return current_dict

    def to_end_dict(self):
        """Devuelve un diccionario del evento listo para poblar la base de datos
        * Utiliza el atributo "repr" (=True) de los fields del dataclass para
        decidir qué atributos son aceptados
        * Aquí se procesan los campos que automaticamente no dan algo coherente
        para la base de datos

        Returns:
            dict: Diccionario listo, completo y con el formato deseado
        """
        current_dict = asdict(self)
        for key in self.__dataclass_fields__:
            value = self.__dataclass_fields__[key]
            if value.type == 'Path':
                if getattr(self, key) is None:
                    current_dict[key] = ""
                else:
                    current_dict[key] = str(getattr(self, key).absolute())
            if not value.repr:
                del current_dict[key]
        return current_dict

    @classmethod
    def reset_all(cls):
        """Resetea toda la lista de eventos
        """
        cls.db = cls.get_current_db_state()
        cls.db["xweekevents"] = list()
        cls.db["xweekevents"].append(cls(id=0).to_end_dict())
        super().save(cls)

    def __next_id(self) -> int:
        g_id = 0
        for event in self.getAll():
            if event.id > g_id:
                g_id = event.id
        return g_id + 1
    
    def save(self):
        """Guarda el evento (nuevo o actualizado) en la base de datos
        """
        self.load()
        
        # Se actualiza evento si ID ya existe
        for index, event in enumerate(self.getAll()):
            if event.id == self.id:
                self.xweekevents[index] = self.to_end_dict()
                super().save()
                print(f'Evento {event.id} actualizado')
                return                
        # Se crea evento si ID no existe
        self.xweekevents.append(self.to_end_dict())     
        print(f'Evento {event.id} creado')
        super().save()
