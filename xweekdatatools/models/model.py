# For TYPE CHECKING ------------------
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xweekdatatools.views import View
# ------------------------------------
# ********** IMPORTS ***********
# ------------ STANDARD LIBRARIES ---------------
import os
import sys
import json
from pathlib import Path
from dataclasses import asdict, dataclass, field
# ------------ THIRD PARTY LIBRARIES ------------
# ------------ LOCAL IMPORTS --------------------
from xweekdatatools.app_constants import DB_FILE_PATH


@dataclass
class Model():
    db_file_path: Path = field(default=Path(DB_FILE_PATH), init=False, repr=False)
    db: dict = field(default_factory=dict, init=False, repr=False)
    view: View = field(default=None, init=False, repr=False)
    xweekconfig: dict = field(default_factory=dict, init=False, repr=False)
    xweekevents: dict = field(default_factory=dict, init=False, repr=False)
    last_event: dict = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self):
        self.load()

    def set_view(self, view):
        self.view = view

    @classmethod
    def get_current_db_state(cls) -> dict:
        try:
            with cls.db_file_path.open("r", encoding="utf-8") as db_file:
                return json.load(db_file)
        except:
            sys.exit("No se pueded abrir base de datos :(")
            print("No se puede abrir el JSON")
            return dict()
    # THESE FUNCTIONS DOESN'T FOLLOW THE FUNCTIONAL PARADIGMS, they are dangerous:

    def load(self):
        """Carga la base de datos en el dict "db" y en las variables de ayuda
        Las variables de ayuda son las que nos permiten acceder facilmente a
        config o a events.
        """
        self.db = self.get_current_db_state()
        if self.db is None:
            sys.exit("No se puede continuar sin una conexión a la base de datos")
        self.xweekconfig = self.db["xweekconfig"]
        self.xweekevents = self.db["xweekevents"]
        self.last_event = self.xweekevents[-1]

    def save(self):
        with open(self.db_file_path, "w", encoding="utf-8") as db_file:
            json.dump(self.db, db_file, ensure_ascii=False, indent=4)
