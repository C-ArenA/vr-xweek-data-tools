import sys
from pathlib import Path
ROOT_FOLDER = Path(__file__).parent.parent
sys.path.append(str(ROOT_FOLDER))

from xweekdatatools.views import View
from xweekdatatools.models import Model
from xweekdatatools.controllers import Controller

controller = Controller()
view = View(controller)
model = Model(view, "db.json")
