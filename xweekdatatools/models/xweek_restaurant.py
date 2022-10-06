# For TYPE CHECKING ------------------
from __future__ import annotations
from typing import TYPE_CHECKING, Any, Union
if TYPE_CHECKING:
    from xweekdatatools.models.xweek_event import XweekEvent
# ------------------------------------
from dataclasses import asdict, dataclass, field
from xweekdatatools.models.model import Model
from xweekdatatools.models.xweek_dish import XweekDish


@dataclass
class XweekRestaurant(Model):
    # Class Attributes
    MODEL_NAME_IN_JSON = "restaurants"
    # Instance Attributes
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
    event_id: int = None
    event: XweekEvent = field(default=None, repr=False)
    
    # SECTION ------------ DB OPERATIONS (CRUD) -----------------
    # CREATE / UPDATE
    def save(self):
        """Guarda el restaurant (nuevo o actualizado) en la base de datos
        """
        self.load()
        # Primero verifico que pertenezca a algún evento. De otra forma es imposible
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
    # READ
    # ANCHOR: getAll() is MANDATORY
    @classmethod
    def getAll(cls) -> list[XweekRestaurant]:
        cls.db_load()
        rests = []
        for event in cls.db[XweekEvent.MODEL_NAME_IN_JSON]:
            for rest in event[XweekRestaurant.MODEL_NAME_IN_JSON]:
                # Sólo se añaden a la lista si son datos válidos
                try:
                    rests.append(cls(**rest))
                except:
                    pass                
        return rests
    
    @classmethod
    def getAllInEvent(cls, event_id:int) -> list[XweekRestaurant]:
        cls.db_load()
        rests = list()
        event = XweekEvent.getById(event_id)
        if event is not None:
            rests = event.restaurants
        return rests

    

    # DELETE
    def remove(self) -> bool:
        self.db_load()
        db_events = self.db[XweekEvent.MODEL_NAME_IN_JSON]
        for db_event in db_events:
            db_restaurants:list = db_event[XweekRestaurant.MODEL_NAME_IN_JSON]
            for index, db_restaurant in enumerate(db_restaurants):
                if self.id == db_restaurant["id"]:
                    db_restaurants.pop(index)
                    return True
        return False
    @classmethod
    def removeById(cls, id):
        cls.db_load()
        index_to_remove = None
        for index, instance in enumerate(cls.getAll()):
            if instance.id == id:
                print("Eliminar: " + instance.summary())
                
        cls.db_save()

    @classmethod
    def reset_all_in_event(cls, event:XweekEvent):
        """Resetea toda la lista de eventos
        """
        cls.db = cls.get_current_db_state()
        cls.db["xweekevents"] = list()
        cls.db["xweekevents"].append(cls(id=0).to_end_dict())
        super().save(cls)

    

    # SECTION ------------ DATA OPERATIONS -----------------

    def summary(self) -> str:
        """Devuelve un pequeño resumen de una instancia del restaurante

        Returns:
            str: Resumen de la instancia del restaurante
        """
        return f'{self.id}: {self.name} -> {self.post_url} Evento: '