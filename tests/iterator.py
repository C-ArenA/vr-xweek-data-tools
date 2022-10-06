import sys
import json
from pathlib import Path
from pprint import pprint

def get_db_dict_from_json_file_path(json_file_path: Path) -> dict:
    try:
        with json_file_path.open("r", encoding="utf-8") as db_file:
            return json.load(db_file)
    except:
        sys.exit("No se pueded abrir la base de datos JSON: " +
                 str(json_file_path))


db = get_db_dict_from_json_file_path(
    Path("F:\\VReality\\XWeekTools\\xweekdatatools\\db.json"))


def event_generator(db):
    for i, v in enumerate(db["xweekevents"]):
        yield i, v


def xweek_generator(db: dict, json_key: str):
    yield_dict = {
        "db_xweekevent_index": None,
        "db_xweekevent": None,
        "db_restaurant_index": None,
        "db_restaurant": None,
        "db_dish_index": None,
        "db_dish": None,
        "db_index": None,
        "db_value": None
    }
    try:
        if isinstance(db["xweekevents"], list):
            for db_xweekevent_index, db_xweekevent in enumerate(db["xweekevents"]):
                yield_dict["db_index"] = yield_dict["db_xweekevent_index"] = db_xweekevent_index
                yield_dict["db_value"] = yield_dict["db_xweekevent"] = db_xweekevent
                if json_key == "xweekevents":    
                    yield yield_dict
                    continue                
                
                if isinstance(db_xweekevent["restaurants"], list):
                    for db_restaurant_index, db_restaurant in enumerate(db_xweekevent["restaurants"]):
                        yield_dict["db_index"] = yield_dict["db_restaurant_index"] = db_restaurant_index
                        yield_dict["db_value"] = yield_dict["db_restaurant"] = db_restaurant
                        if json_key == "restaurants":    
                            yield yield_dict
                            continue
                            
                        if isinstance(db_restaurant["dishes"], list):
                            for db_dish_index, db_dish in enumerate(db_restaurant["dishes"]):
                                yield_dict["db_index"] = yield_dict["db_dish_index"] = db_dish_index
                                yield_dict["db_value"] = yield_dict["db_dish"] = db_dish
                                if json_key == "dishes":    
                                    yield yield_dict
    except:
        pass                                
                            
    



print("\n")
pprint(db["xweekevents"])
for v in xweek_generator(db, "restaurants"):
    v["db_xweekevent"]["restaurants"][v["db_restaurant_index"]] = 7

print("\n")
pprint(db["xweekevents"])
