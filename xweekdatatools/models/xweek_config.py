from __future__ import annotations
from dataclasses import asdict, dataclass, field, fields
from mimetypes import init
from pathlib import Path

from xweekdatatools.models.xweek_restaurant import XweekRestaurant
from xweekdatatools.models import Model
from xweekdatatools.utils import make_valid_path, json_serializable_path

@dataclass
class XweekConfig(Model):
    MODEL_NAME_IN_JSON = "xweekconfig"
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
    
    @classmethod
    def getAll(cls) -> dict:
        db = cls.get_current_db_state()
        events = []
        for event in db[XweekConfig.MODEL_NAME_IN_JSON]:
            # Sólo se añaden a la lista si son datos válidos
            try:
                events.append(cls(**event))
            except:
                pass                
        return events
