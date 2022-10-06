# For TYPE CHECKING ------------------
from __future__ import annotations
from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from xweekdatatools.views import View
# ------------------------------------
# ********** IMPORTS ***********
# ------------ STANDARD LIBRARIES ---------------
import os
import sys
import json
import datetime
from pathlib import Path
from dataclasses import Field, asdict, dataclass, field, fields
# ------------ THIRD PARTY LIBRARIES ------------
# ------------ LOCAL IMPORTS --------------------
from xweekdatatools.utils.path_helpers import json_serializable_path, make_valid_path
from xweekdatatools.utils.db_helpers import get_db_dict_from_json_file_path
from xweekdatatools.app_constants import DB_FILE_PATH


@dataclass
class Model():
    # Class Attributes
    db_file_path =Path(DB_FILE_PATH)
    db = get_db_dict_from_json_file_path(db_file_path)
    # Cualquier instancia de un modelo de datos necesita tener un ID
    # (A excepción del Model original que se deja en None)
    id: int = None
    created: str = datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")
    modified: str = datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")
    # In case we need a View for our instance:
    view: View = field(default=None, repr=False)

    def __post_init__(self):
        self.db_load()
        # Aquí nos aseguramos que todas las instancias de Model (y sus hijos) 
        # tengan atributos válidos en sus fields.
        for attr_field in fields(self):
            attr = getattr(self, attr_field.name)
            # Sólo es relevante si el campo es parte del init
            if attr_field.init:
                setattr(self, attr_field.name, Model.decode_json_attr(attr, attr_field.type))
        # Si no se proporciona un ID se genera automaticamente
        self.id = self.next_id() if self.id is None else self.id

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

    @classmethod
    def db_load(cls) -> dict:
        """Carga la base de datos en el dict "db"
        
        Se debe usar cada vez que se desee hacer una modificación o lectura 
        a la base de datos para hacerla sobre la versión más actualizada
        
        Returns:
            dict: Se retorna "db"
        """
        cls.db = get_db_dict_from_json_file_path(cls.db_file_path)
        if cls.db is None:
            sys.exit("No se puede continuar sin una base de datos válida")
        return cls.db

    @classmethod
    def db_save(cls) -> dict:
        """Guarda el dict "db" en la base de datos
        
        Se puede usar después de hacer cambios en el dict db para guardarlos 
        en la base de datos
        
        Cada modelo puede tener su propia implementación que asegure cambios
        relacionados a su modelo y que se esté trabajando sobre la versión más
        actualizada de la base de datos
        
        Returns:
            dict: Se retorna "db"
        """
        if input("Está a punto de guardar algo en la base de datos Cancelar:'c':") == "c":# TODO: Borrar esta línea de ayuda
            sys.exit("Saliendo para no dañar la base de datos")
        with open(cls.db_file_path, "w", encoding="utf-8") as db_file:
            json.dump(cls.db, db_file, ensure_ascii=False, indent=4)
    # SECTION ------------ DB OPERATIONS (CRUD) -----------------  
    # Read
    @classmethod
    def getAll(cls) -> list[Model]:
        # Should be implemented in child classes
        return list()          
    @classmethod
    def getById(cls, id) -> Model:
        cls.db_load()
        for instance in cls.getAll():
            if instance.id == id:
                return instance
        return None
    # SECTION ------------- UTILS -------------
    @classmethod
    def make_attr_json_serializable(cls, attr: Any, attr_field_type: str) -> Any:
        """Convierte un atributo de la clase en una variable serializable para JSON

        * Si se trata de un Objeto le pide serializarse si se puede
        * Si es un Path devuelve el string del path absoluto
        * Si no es un valor válido de acuerdo al Field correspondiente (o por otro motivo) devuelve None
        * Si no se sabe qué tipo de dato es de acuerdo al field, se devuelve None (Porque en este caso
        se considera mejor devolver algo que lanzar un error)

        En fin, convierte todo a tipos básicos de Python para serializar:
        str -> string, 
        int, float -> number, 
        dict -> object (JSON Object: cannot be a python instance of a class), 
        list -> array, 
        bool -> boolean, 
        None -> null

        For more information about JSON data types visit [this page](https://www.w3schools.com/js/js_json_datatypes.asp)

        Args:
            attr (Any): El valor del atributo a ser analizado
            attr_field (str): el dataclass.Field.type correspondiente al atributo

        Returns:
            Any: Representación serializable del atributo ingresado a la función
        """
        # Proceso de acuerdo al tipo de dato deseado por el field
        # ----- Any type
        if attr_field_type == "Any" or attr_field_type == "any" or attr_field_type == "":
            return str(attr)
        # ----- PATHs
        if attr_field_type == 'Path':
            return json_serializable_path(attr)
        # ----- strings
        if attr_field_type == "str":
            if type(attr) is not str:
                return None
            return attr
        # ----- integers
        if attr_field_type == "int":
            try:
                return int(attr)
            except:
                return None
        # ----- list[Path]
        if attr_field_type == "list[Path]":
            list_attr = list()
            if isinstance(attr, list):
                for path in attr:
                    list_attr.append(json_serializable_path(path))
            return list_attr
        # ----- list[XweekRestaurant]
        if attr_field_type == "list[XweekRestaurant]":
            list_attr = list()
            if isinstance(attr, list):
                for xweekRestaurant in attr:
                    try:
                        list_attr.append(xweekRestaurant.json_serializable_dict())
                    except:
                        pass
            return list_attr
        # ----- list[Any]
        if attr_field_type[:4] == "list":
            list_attr = list()
            if isinstance(attr, list):
                for item in attr:
                    try:
                        # En caso de que sea un modelo mío y tenga el método json_serializable_dict
                        list_attr.append(item.json_serializable_dict())
                    except:    
                        # Sino se seguirá intentando de forma recursiva
                        list_attr.append(cls.make_attr_json_serializable(item, attr_field_type[5:-1]))
            return list_attr
        return None
    
    @classmethod
    def decode_json_attr(cls, attr: Any, attr_field_type: str) -> Any:
        """Al revés del método make_attr_json_serializable, este método transforma 
        lo guardado en un atributo desde algún JSON en un tipo de dato de Python
        
        * Se manejan algunos casos específicos, por lo que esta función se debe 
        extender en las clases hijo para sus atributos
        
        * En algunos casos se pueden procesar los atributos de forma automática
        
        Este método se debe llamar por lo general dentro del __post_init__ ya que
        postprocesa los datos brindados al crear la instancia del modelo
        
        Si no se puede postprocesar se deja como está
        
        Args:
            attr (Any): El valor del atributo a ser analizado
            attr_field (str): el dataclass.Field.type correspondiente al atributo

        Returns:
            Any: Representación serializable del atributo ingresado a la función
        """
        from xweekdatatools.views import View
        # ----- Any type
        if attr_field_type == "Any" or attr_field_type == "any" or attr_field_type == "":
            return attr
        # ----- PATH
        if attr_field_type == 'Path':
            return make_valid_path(attr)
        # ----- str
        if attr_field_type == 'str':
            if isinstance(attr,str):
                return attr
            if isinstance(attr, int):
                return str(attr)
            if isinstance(attr, bool):
                return str(attr)
            return None
        # ----- int
        if attr_field_type == 'int':
            try:
                return int(attr)
            except:
                return None
        # ----- list[Any]
        if attr_field_type[:4] == "list":
            list_attr = list()
            if isinstance(attr, list):
                for item in attr:
                    # Se busca corresponder el item con algún modelo
                    item_converted = Model.json_dict_correspondance(item)
                    # Si no corresponde, se procesa el atributo de forma general y recursiva
                    if item_converted is None:
                        item_decoded = Model.decode_json_attr(item, attr_field_type[5:-1])
                        if item_decoded is not None:
                            list_attr.append(Model.decode_json_attr(item, attr_field_type[5:-1]))
                    # Si corresponde, se añade a la lista
                    else:
                        list_attr.append(item_converted)
                    
            return list_attr
        # ------- View
        if attr_field_type == "View":
            if isinstance(attr, View):
                return attr
            return None
        # Si no tenemos el tipo de dato validado aún, devolvemos un None
        return None
    
    @classmethod
    def json_dict_correspondance(cls, dict) -> Model:
        """Verifica si un diccionario se corresponde con algún modelo descendiente
        de Model. Si es así, retorna el modelo con los datos del diccionario, sino
        retorna None

        Args:
            dict (_type_): Diccionario a verificar

        Returns:
            Model: Retorna alguna instancia de alguna clase hija de Model o None
        """
        # Primero identifico los hijos de Model 
        # TODO: Hallar una forma más pythónica de hacerlo
        child_classes = Model.__subclasses__()
        # Primero obtenemos los keys del dict 
        # Puede que no se nos pase un dict, puede ser un int, str, bool, en
        # cuyo caso no se procede y se devuelve None
        try:
            dict_keys = list(dict.keys())
        except:
            return None
        # Con todos los hijos se verifican los keys
        for child in child_classes:
            my_keys = child.to_json_keys()
            # Si el diccionario tiene las mismas llaves que el json_serializable del modelo
            # se asume que, al menos, es posible crearse una instancia con este dict
            if my_keys == dict_keys:
                return child(**dict)
        # Si no se coincide con ningún modelo, se retorna None
        return None
    
    def exists(self) -> bool:
        """Verifica si esta instancia ya existe en la base de datos

        Se dice que existe si es que su id está presente en la base de datos
        Se ignora si los otros atributos coinciden o no
        
        Returns:
            bool: True si ya existe
        """
        existing_instances = self.getAll()
        for existing in existing_instances:
            if existing.id == self.id:
                return True
        return False
    
    def json_serializable_dict(self) -> dict:
        """Devuelve un diccionario del modelo listo para poblar la base de datos en JSON
        
        * Utiliza el atributo "repr" (=True) de los fields del dataclass para
        decidir qué atributos son aceptados
        * Los atributos se procesan para poder ser JSON serializables y para
        ser coherentes

        Returns:
            dict: Diccionario listo, completo y con el formato deseado JSON serializable
        """
        
        serializable_dict = {}
        # Se analiza cada campo del objeto
        for attr_field in fields(self):
            attr = getattr(self, attr_field.name)
            # Si el campo no tiene el repr en True, se omite del dict
            if not attr_field.repr:
                continue
            # Si el campo entra primero se convierte en JSON serializable y luego se guarda en el dict
            serializable_dict[attr_field.name] = self.make_attr_json_serializable(attr, attr_field.type)
        
        return serializable_dict
    
    def next_id(self) -> int:
        g_id = 0
        for event in self.getAll():
            if event.id > g_id:
                g_id = event.id
        return g_id + 1
    
    def to_dict(self):
        """Devuelve un diccionario con todos los atributos de la instancia del modelo
        """
        current_dict = asdict(self)
        return current_dict
    
    def summary(self):
        print("Modelo sin summary: " + self.id)
    
    @classmethod
    def to_json_fields(cls) -> list[Field]:
        """Devuelve los fields de los campos que van a la base de datos

        Returns:
            list[Field]: lista de fields de los campos del modelo que van al json
        """
        all_fields = fields(cls)
        return [raw_field for raw_field in all_fields if raw_field.repr==True]
    @classmethod
    def to_json_keys(cls) -> list[str]:
        """Devuelve las keys que el modelo lleva a la base de datos en json

        Returns:
            list[str]: lista de keys
        """
        return [json_field.name for json_field in cls.to_json_fields()]