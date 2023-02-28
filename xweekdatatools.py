from xweekdatatools import App

import logging
# Para modificar el formato tenemos los atributos en: https://docs.python.org/3/library/logging.html#logrecord-attributes
logging.basicConfig(
    format='💮 %(levelname)s: %(module)s [%(lineno)s] %(funcName)s():\n➡️  %(message)s',
    level=logging.INFO,
	encoding="utf-8"
)

logging.info("App inicia")
app = App()
logging.info("App termina")
