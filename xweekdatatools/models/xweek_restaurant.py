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
    def save(self) -> bool:
        """Guarda el restaurant (nuevo o actualizado) en la base de datos
        """
        self.load()
        # Primero verifico que pertenezca a algún evento existente. De otra forma es imposible
        # crear o actualizar este restaurante
        if not self.attach_to_an_event():
            print("No existe un evento real para este restaurante, no se puede proceder")
            return False
        # -------------------------------------------------------------------------------------

        # Si el ID del evento no es válido (es None o no es int) se aborta
        if type(self.id) != int:
            print(f'Restaurante no pudo ser creado por ID inválido')
            return False
        # Ahora añadimos este restaurante a nuestra instancia de evento ya verificada 
        # Si hay un id similar entre los restaurantes del evento, se actualiza el restaurante:
        for index, rest in enumerate(self.event.restaurants):
            if rest.id == self.id:
                self.event.restaurants[index] = self
                self.event.save()
                print("Restaurant actualizado")
                return True
        # Sino se añade como nuevo restaurante (Tras verificar la unicidad del ID)
        for rest in self.getAll():
            if rest.id == self.id:
                self.id = self.next_id()
        self.event.restaurants.append(self)
        self.event.save()
        print("Restaurant creado")
        return True
        
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
        if not self.attach_to_an_event():
            print("No existe un evento real para este restaurante. No se puede proceder")
            return False
        
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

    

    # SECTION ------------ DATA OPERATIONS AND TOOLS-----------------

    def summary(self) -> str:
        """Devuelve un pequeño resumen de una instancia del restaurante

        Returns:
            str: Resumen de la instancia del restaurante
        """
        return f'{self.id}: {self.name} -> {self.post_url} Evento: '
    
    def attach_to_an_event(self) -> bool:
        """Verifica que el restaurant pertenezca a algún evento existente. De otra forma es imposible
        realizar ciertas operaciones, ya que todo restaurante depende de algún evento

        Returns:
            bool: Indica si el restaurante fue conectado exitosamente a un evento existente
        """
        
        # Si el id del evento existe se actualiza el evento con ese id
        if self.event_id is not None:
            self.event = XweekEvent.getById("event_id")
            return True
        # Si no hay id pero hay evento, se actualiza el mismo evento con los datos más recientes y el id
        elif self.event is not None:
            self.event: XweekEvent = XweekEvent.getById(self.event.id)
            self.event_id = self.event.id
            return True
        # Si después de lo anterior no hay evento existente salimos con Falso
        if self.event is None:
            return False
        # Pero si el evento sí existe, salimos con True
        return True