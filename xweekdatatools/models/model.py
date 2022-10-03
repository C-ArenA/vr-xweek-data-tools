# For TYPE CHECKING ------------------
from __future__ import annotations
from typing import TYPE_CHECKING

from xweekdatatools.models.xweek_event import XweekEvent
if TYPE_CHECKING:
    from xweekdatatools.views import View
# ------------------------------------
# ********** IMPORTS ***********
# ------------ STANDARD LIBRARIES ---------------
import os
import sys
import json
from pathlib import Path
# ------------ THIRD PARTY LIBRARIES ------------
# ------------ LOCAL IMPORTS --------------------


class Model:
    def __init__(self, view: View, db_file_path: Path) -> None:
        self.view = view
        self.db_file_path: Path = Path(db_file_path) if type(
            db_file_path) == str else db_file_path
        # ------------- Database connection
        self.db = None
        self.load()
        # ------------- Database easy to access objects
        self.xweekconfig: dict = self.db["xweekconfig"]
        self.xweekevents: list = self.db["xweekevents"]
        self.last_event: dict = self.xweekevents[-1]

    def add_event(self, event:XweekEvent):
        self.load()
        self.xweekevents.append(event.to_dict())
        self.save()
        
        
    def get_current_db_state(self) -> dict:
        try:
            with self.db_file_path.open("r", encoding="utf-8") as db_file:
                return json.load(db_file)
        except:
            return None
        
        
        

    # THESE FUNCTIONS DOESN'T FOLLOW THE FUNCTIONAL PARADIGMS, they are dangerous:
    def load(self):
        self.db = self.get_current_db_state()
        if self.db is None:
            self.view.no_model(self.db_file_path)
            sys.exit("No se puede continuar sin una conexión a la base de datos")
        self.view.has_model(self.db_file_path)
        self.xweekconfig = self.db["xweekconfig"]
        self.xweekevents = self.db["xweekevents"]
        self.last_event = self.xweekevents[-1]

    def save(self):
        with open(self.db_file_path, "w", encoding="utf-8") as db_file:
            json.dump(self.db, db_file, ensure_ascii=False, indent=4)

