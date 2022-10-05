from __future__ import annotations
from dataclasses import asdict, dataclass, field, fields
from mimetypes import init
from pathlib import Path
import datetime
from xweekdatatools.models.xweek_restaurant import XweekRestaurant
from xweekdatatools.models import Model
from xweekdatatools.utils import make_valid_path, json_serializable_path

@dataclass
class XweekEvent(Model):
    MODEL_NAME_IN_JSON = "xweekevents"
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
        
    # SECTION ------------ DB OPERATIONS -----------------

    @classmethod
    def getAll(cls) -> list[XweekEvent]:
        db = cls.get_current_db_state()
        events = []
        for event in db[XweekEvent.MODEL_NAME_IN_JSON]:
            # Sólo se añaden a la lista si son datos válidos
            try:
                events.append(cls(**event))
            except:
                pass                
        return events
    
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

    @classmethod
    def reset_all(cls):
        """Resetea toda la lista de eventos
        """
        cls.db = cls.get_current_db_state()
        cls.db["xweekevents"] = list()
        cls.db["xweekevents"].append(cls(id=0).to_end_dict())
        super().save(cls)

    def save(self):
        """Guarda el evento (nuevo o actualizado) en la base de datos
        """
        self.load()
        # Si el ID del evento no es válido (es None o no es int) se aborta
        if type(self.id) != int:
            print(f'Evento no pudo ser creado por ID inválido')
            return
        # Se actualiza evento si ID ya existe
        for index, event in enumerate(self.getAll()):
            if event.id == self.id:
                self.xweekevents[index] = self.to_end_dict()
                super().save()
                print(f'Evento {event.id} actualizado')
                return
        # Se crea evento si ID no existe
        self.xweekevents.append(self.json_serializable_dict())
        super().save()
        print(f'Evento {self.id} creado')

    # SECTION ------------ DATA OPERATIONS -----------------
    
    def to_dict(self):
        """Devuelve un diccionario con todos los atributos a 
        excepción de aquellos de la clase padre"""
        current_dict = asdict(self)
        for key in super().__dataclass_fields__.keys():
            del current_dict[key]
        return current_dict

    

    def summary(self) -> str:
        """Devuelve un pequeño resumen de una instancia del evento

        Returns:
            str: Resumen de la instancia del evento
        """
        return f'{self.id}: {self.name} {self.location}, versión: {self.version}, modified: {self.modified}'
