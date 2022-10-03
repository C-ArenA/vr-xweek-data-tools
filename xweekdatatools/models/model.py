# For TYPE CHECKING ------------------
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from xweekdatatools.views import View
# ------------------------------------
# ********** IMPORTS ***********
# ------------ STANDARD LIBRARIES ---------------
import os, sys, json
from pathlib import Path
# ------------ THIRD PARTY LIBRARIES ------------
# ------------ LOCAL IMPORTS --------------------


class Model:
    def __init__(self, view:View, db_file_path:Path) -> None:
        self.view = view
        self.db_file_path: Path = Path(db_file_path) if type(db_file_path) == str else db_file_path
        try:
            # with open(self.db_file_path, "r", encoding="utf-8") as db_file:
            #     self.db = json.load(db_file)
            with self.db_file_path.open("r", encoding="utf-8") as db_file:
                self.db = json.load(db_file)
        except:
            self.db = {}
            self.view.no_model(self.db_file_path)
            sys.exit("No se puede continuar sin una conexión a la base de datos")
        else:
            self.xweekconfig = self.db["xweekconfig"]
            self.xweekevents = self.db["xweekevents"]
            self.view.has_model(self.db_file_path)
            
            
    def get_config(self):
        return self.xweekconfig
    def get_last_event(self):
        return self.xweekevents[-1]
    def get_last_event_data(self):
        return self.get_last_event()["data"]
    def get_last_event_paths(self):
        return self.get_last_event()["paths"]
    def get_last_event_now(self):
        return self.get_last_event()["now"]

    def save(self):
        with open(self.db_file_path, "w", encoding="utf-8") as db_file:
            json.dump(self.db, db_file, ensure_ascii=False, indent=4)
        