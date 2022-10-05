# For TYPE CHECKING ------------------
from __future__ import annotations
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from xweekdatatools.models.xweek_event import XweekEvent
# ------------------------------------
from dataclasses import asdict, dataclass, field
from xweekdatatools.models.model import Model
from xweekdatatools.models.xweek_dish import XweekDish


@dataclass
class XweekRestaurant(Model):
    MODEL_NAME_IN_JSON = "restaurants"
    id: int = None
    order: int = 0
    name: str = ""
    address: str = ""
    phone: str = ""
    opening_hours: str = ""
    delivery: str = ""
    slugified_name: str = ""
    post_title: str = ""
    post_name: str = ""
    post_url: str = ""
    logo_name: str = ""
    logo_url: str = ""
    dishes: list[XweekDish] = None
    event: XweekEvent = field(default=None, repr=False)
    
    # SECTION ------------ DB OPERATIONS -----------------

    @classmethod
    def getAll(cls) -> list[XweekEvent]:
        db = cls.get_current_db_state()
        rests = []
        for event in db[XweekEvent.MODEL_NAME_IN_JSON]:
            for rest in event[cls.MODEL_NAME_IN_JSON]:
                # Sólo se añaden a la lista si son datos válidos
                try:
                    rests.append(cls(**rest))
                except:
                    pass                
        return rests
    
    @classmethod
    def getAllInEvent(cls, event:XweekEvent) -> list[XweekEvent]:
        rests=[]
        for rest in event.restaurants:
            # Sólo se añaden a la lista si son datos válidos
            rests.append(rest)
        return rests

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
    def reset_all_in_event(cls, event:XweekEvent):
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
    def to_dict(self):
        return asdict(self)

    

    def summary(self) -> str:
        """Devuelve un pequeño resumen de una instancia del restaurante

        Returns:
            str: Resumen de la instancia del restaurante
        """
        return f'{self.id}: {self.name} -> {self.post_url} Evento: '