import sys
import json
from pathlib import Path


def get_db_dict_from_json_file_path(json_file_path:Path) -> dict:
	try:
		with json_file_path.open("r", encoding="utf-8") as db_file:
			return json.load(db_file)
	except:
		sys.exit("No se pueded abrir la base de datos JSON: " + str(json_file_path))