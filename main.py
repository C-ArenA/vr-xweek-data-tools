# ----------------- EXTERNAL IMPORTS

import os
from pprint import pprint
from yachalk import chalk
from slugify import slugify
from InquirerPy import inquirer

# ---------------- MY IMPORTS (In order of usage)
# -----------------------------------------------------------------------


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(chalk.blue.bold("\n-------------------------------------------------------------"))
    print(chalk.blue.bold("|😀 Bienvenido. Esta pequeña aplicación te ayudará a extraer |"))
    print(chalk.blue.bold("|los datos de tu siguiente evento en un archivo JSON         |"))
    print(chalk.blue.bold("-------------------------------------------------------------\n"))
    # inicializo datos del Evento
    # Actualizar datos del Evento
    inquirer.confirm(message="Actualizar?").execute()
        
    # Indicar las carpetas de donde se extrae la información (docs, fotos, etc)

    # Recolecto docs
    # Recolecto fotos
    # Recolecto logos
    # Convierto docs a plain text
    # Prenormalizo txts
    # Normalizar txts manualmente
    # Listo los txts normalizados
    # Convierto los txts a JSON
    pass


def myquestions():
    a = os.path.normpath("F:\\VReality\\BurgerWeek\\BW_SC_6ta")
    questions = [

        inquirer.Checkbox("adj", "describe me", [
                          "great", "amazing", "woow"], "great"),
        inquirer.Path("new_docs_dir", message="Dónde se guardarán los docs?", path_type=inquirer.Path.ANY),
    
    ]
    answers = inquirer.prompt(questions)
    print(answers)

def updateEventInfo():
    basic_questions = [
        inquirer.List("event_name", "Nombre del Evento", ["Burger Week", "Pizza Week", "Restaurant Week", "Otro"]),
        inquirer.Text("event_name_other", "Escriba el nombre del evento", ""),
        inquirer.List("event_city", "Lugar del evento {event_name}", ["La Paz", "Santa Cruz", "Cochabamba", "ea", "pn", "bn", "or", "pt", "ch", "tj"]),
        inquirer.Text("event_version", "Versión del evento (Número)", "1", validate=lambda a,c: c.isnumeric()),
		inquirer.Text("event_domain", "Dominio del sitio web del evento", "https://"),
		inquirer.Text("event_media_url", "Url base de donde se guardan los medios (fotos, logos, etc)", "https://"),
		inquirer.Path("event_directory", message="Directorio donde están los archivos del evento en tu PC local (Puedes arrastrar la carpeta)", path_type=inquirer.Path.ANY)
	]
    other_questions = [
        inquirer.List("event_name", "Nombre del Evento", ["Burger Week", "Pizza Week", "Restaurant Week", "Otro"]),
        inquirer.List("event_city", "Lugar del evento", ["La Paz", "Santa Cruz", "Cochabamba", "ea", "pn", "bn", "or", "pt", "ch", "tj"]),
        inquirer.Text("event_version", "Versión del evento (Número)", "1", validate=lambda a,c: c.isnumeric()),
		inquirer.Text("event_domain", "Dominio del sitio web del evento", "https://"),
		inquirer.Text("event_media_url", "Url base de donde se guardan los medios (fotos, logos, etc)", "https://"),
		inquirer.Path("event_directory", message="Directorio donde están los archivos del evento en tu PC local (Puedes arrastrar la carpeta)", path_type=inquirer.Path.ANY)
	]
    return inquirer.prompt(basic_questions)

if __name__ == "__main__":
    main()
