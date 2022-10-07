# For TYPE CHECKING ------------------
from __future__ import annotations
from pathlib import Path
import sys
from typing import TYPE_CHECKING, Any, Union
if TYPE_CHECKING:
    from xweekdatatools.models.xweek_event import XweekEvent
# ------------------------------------
from slugify import slugify
from dataclasses import asdict, dataclass, field
from xweekdatatools.models.model import Model
from xweekdatatools.models.xweek_dish import XweekDish


@dataclass
class XweekRestaurant(Model):
    # Class Attributes
    MODEL_NAME_IN_JSON = "restaurants"
    # Instance Attributes
    order: int = None
    name: str = ""
    address: str = ""
    phone: str = ""
    opening_hours: str = ""
    delivery: str = ""
    dishes: list[XweekDish] = field(default_factory=list)
    slugified_name: str = ""  # Versión slug de sólo el nombre del restaurante
    post_title: str = ""  # Título del post en Wordpress
    post_name: str = ""  # slug del post en Wordpress
    post_url: str = ""  # url completa del post
    logo_name: str = ""
    logo_ext: str = ".png"
    logo_url: str = ""

    def fill_automatic_fields(self, event: XweekEvent):
        self.slugified_name = slugify(
            self.name) if self.slugified_name == "" else self.slugified_name
        self.post_title = self.name + " " + \
            event.get_version() if self.post_title == "" else self.post_title
        self.post_name = slugify(self.post_title)
        self.post_url = event.domain + "/" + self.post_name
        self.logo_name = self.post_name if self.logo_name == "" else self.logo_name
        self.logo_url = event.media_url + "/" + self.logo_name + self.logo_ext

    # SECTION ------------ DB OPERATIONS (CRUD) -----------------
    # CREATE / UPDATE
    def save(self, event: XweekEvent) -> bool:
        """Guarda el restaurant (nuevo o actualizado) en la base de datos
        """
        self.db_load()
        self.fill_automatic_fields(event)
        # Primero verifico que pertenezca a algún evento existente. De otra forma es imposible
        # crear o actualizar este restaurante
        if not event.exists():
            print("No existe un evento real para este restaurante, no se puede proceder")
            return False
        # -------------------------------------------------------------------------------------

        # Si el ID del evento no es válido (es None o no es int) se aborta
        if type(self.id) != int:
            print(f'Restaurante no pudo ser creado por ID inválido')
            return False
        # Ahora añadimos este restaurante a nuestra instancia de evento ya verificada
        # Si hay un id similar entre los restaurantes del evento, se actualiza el restaurante:
        for index, rest in enumerate(event.restaurants):
            if rest.id == self.id:
                event.restaurants[index] = self
                event.save()
                print("Restaurant actualizado")
                return True
        # Sino se añade como nuevo restaurante (Tras verificar la unicidad del ID)
        for rest in self.getAll():
            if rest.id == self.id:
                self.id = self.next_id()
        event.restaurants.append(self)
        event.save()
        print("Restaurant creado")
        return True

    # READ
    # ANCHOR: getAll() is MANDATORY
    @classmethod
    def getAll(cls) -> list[XweekRestaurant]:
        from xweekdatatools.models.xweek_event import XweekEvent
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

    # DELETE
    def remove_from_event(self, event: XweekEvent) -> bool:
        self.db_load()
        for index, rest in enumerate(event.restaurants):
            if rest.id == self.id:
                event.restaurants.pop(index)
                event.save()
                print("Restaurante eliminado: " + self.id + self.name)
                return True
        return False

    @classmethod
    def reset_all_in_event(cls, event: XweekEvent) -> bool:
        """Resetea toda la lista de eventos
        """
        cls.db_load()
        event.restaurants = list()
        event.save()
        return True

    # SECTION ------------ DATA OPERATIONS AND TOOLS-----------------

    def summary(self) -> str:
        """Devuelve un pequeño resumen de una instancia del restaurante

        Returns:
            str: Resumen de la instancia del restaurante
        """
        return f'{self.id}: {self.name} -> {self.post_url} Evento: '

    # SECTION ----------- FACTORY METHODS ---------------------
    @classmethod
    def from_text(cls, event: XweekEvent, text: str, photos_format=".jpg", logos_format=".png") -> XweekRestaurant:
        """Genera una instancia de Restaurante a partir de un str de datos 
        normalizado del restaurante que cumplen el formato especificado en
        xweekdatatools/app_constants/TXT_FORMAT

        Args:
            event (XweekEvent): Evento para el cual se genera este restaurante
            txt (Path): Path del txt con los datos crudos
            photos_format (str, optional): Formato por defecto de las fotos de restaurantes. Defaults to ".jpg".
            logos_format (str, optional): Formato por defecto de los logos de restaurantes. Defaults to ".png".

        Returns:
            XweekRestaurant: Instancia de XweekRestaurant con los datos del txt
        """
        import re
        from xweekdatatools.app_constants import REST_DATA_SEPARATORS, REST_DATA_SEPARATORS_DICT
        # ----------- POSTNORMALIZACIÓN --------------
        # El texto lo convierto en un array para poder analizar de forma más sencilla. 
        # El patrón para dividir el texto serán los emojis asignados como separadores
        # TODO: Hacer que sólo se tomen en cuenta los emojis al principio de cada línea
        
        # Para evitar problemas de compatibilidad remplazamos emojis
        # problemáticos con sus equivalentes:
        # TODO: Sacar esta parte de aquí
        text = text.replace('🍽️', '🍽')
        text = text.replace('☎️', '☎')
        # Generamos un regex string con todos los emojis relevantes para splitear
        # el texto del archivo
        regex = r"(["
        for rest_data_separator in REST_DATA_SEPARATORS:
            for emoji in rest_data_separator["emojis"]:
                regex += emoji
        regex += "])"
        text_array = [line_text.strip() for line_text in re.split(regex, text)]
        
        
        new_rest = cls(
            name=text_array[0]
        )
        new_rest.fill_automatic_fields(event)
        
        dish_data = {}
        
        for line, line_text in enumerate(text_array):
            if line_text in REST_DATA_SEPARATORS_DICT:
                # No se guarda lo que sigue al emoji si:
                # 1. Ya no hay más contenido en el texto después del emoji
                if line+1 > len(text_array):
                    continue
                # 2. Lo que sigue al emoji está vacío (No definido)
                if text_array[line+1] == "":
                    continue
                # 3. Lo que sigue al emoji es otro emoji (Contenido vacío)
                if text_array[line+1] in REST_DATA_SEPARATORS:
                    continue
                # ---------- AHORA SÍ -------------
                
                separator = REST_DATA_SEPARATORS_DICT[line_text]
                if separator["context"] == "restaurant":
                    setattr(new_rest, separator["key"], text_array[line+1])
                if separator["context"] == "dish":
                    if separator["emojis"][0] == "💵":
                        if text_array[line-1] == "" or text_array[line-1] in REST_DATA_SEPARATORS_DICT:
                            continue
                    dish_data[separator["key"]] = text_array[line+1]
                    if "💵" in separator["emojis"]:
                        dish_data["photo_name"] = new_rest.post_name + "_" + slugify(dish_data["name"])
                        dish_data["photo_ext"] = photos_format
                        dish_data["photo_url"] = event.media_url + "/" + dish_data["photo_name"] + dish_data["photo_ext"]
                        new_rest.dishes.append(dish_data)
                        dish_data = {}
        return new_rest
                    
                