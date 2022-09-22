# ----------------- EXTERNAL IMPORTS
from configparser import ConfigParser
from email import message
import os
import json
from slugify import slugify
import datetime

import inquirer
import logging
# Para modificar el formato tenemos los atributos en: https://docs.python.org/3/library/logging.html#logrecord-attributes
logging.basicConfig(format='%(funcName)s(): %(levelname)s [%(lineno)s]:\n💮-> %(message)s', level=logging.DEBUG)

# ---------------- MY IMPORTS (In order of usage)
from get_rest_folders import get_rest_folders
from collect_docs import collect_docs
from docs2md import docs2md
from raw_data_to_dict import raw_data_to_dict
from gen_url_csv_xlsx import gen_url_csv, gen_url_xlsx
from gen_qr_codes import gen_qr_codes
from collect_images import collect_images
# --------------------------- RETRIEVING CONFIG  DATA -----------------

# config = ConfigParser()
# config.read("config.ini")

# DOMAIN = config["event"]["DOMAIN"]
# VERSION_SPECIFIER = config["event"]["VERSION_SPECIFIER"]
# EVENT_DIRECTORY = os.path.normpath(config["event"]["EVENT_DIRECTORY"])
# SRC_DIRECTORY = os.path.normpath(config["event"]["SRC_DIRECTORY"])
# SRC_IMG_DIRECTORY = os.path.normpath(config["event"]["src_img_directory"])
# WP_CONTENT_URL = config["event"]["WP_CONTENT_URL"]

# # ---- Defino paths de archivos temporales
# TEMP_DIRECTORY = os.path.join(EVENT_DIRECTORY, "TEMP")

# DOCS_DIRECTORY = os.path.join(
#     TEMP_DIRECTORY, "docs-" + datetime.datetime.now().strftime("%d%m%y_%H%M%S"))
# MDS_DIRECTORY = os.path.join(
#     TEMP_DIRECTORY, "mds-" + datetime.datetime.now().strftime("%d%m%y_%H%M%S"))
# IMGS_DIRECTORY = os.path.join(
#     TEMP_DIRECTORY, "imgs-" + datetime.datetime.now().strftime("%d%m%y_%H%M%S"))
# QRS_DIRECTORY = os.path.join(
#     TEMP_DIRECTORY, "qrs-" + datetime.datetime.now().strftime("%d%m%y_%H%M%S"))
# try:
#     LAST_DOCS_DIRECTORY = os.path.normpath(config["event"]["LAST_DOCS_DIRECTORY"])
#     LAST_MDS_DIRECTORY = os.path.normpath(config["event"]["LAST_MDS_DIRECTORY"])
# except:
#     LAST_DOCS_DIRECTORY = ""
#     LAST_MDS_DIRECTORY = ""
# try:
#     LAST_IMGS_DIRECTORY = os.path.normpath(config["event"]["last_imgs_directory"])
# except:
#     LAST_IMGS_DIRECTORY = ""
# try:
#     LAST_JSON_FILE = os.path.normpath(config["event"]["LAST_JSON_FILE"])
# except:
#     LAST_JSON_FILE = ""
    
# -----------------------------------------------------------------------

def main():
	questions = [
		
		inquirer.Checkbox("adj", "describe me", ["great", "amazing", "woow"], "great"),
		inquirer.Path("new_docs_dir", "f:/VReality/XWeekTools/", inquirer.Path.DIRECTORY,exists=False,normalize_to_absolute_path=True, message="Dónde se guardarán los docs?")
	]
	answers = inquirer.prompt(questions)
	print(answers)
	
if __name__ == "__main__":
	main()