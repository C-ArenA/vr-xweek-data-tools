from pathlib import Path
from typing import Union


def make_valid_path(path: Union[str, Path]) -> Union[Path, None]:
    """Convierte un path extrictamente a tipo Path si es válido o None si no es válido
    Si ya era Path sólo devuelve el mismo elemento (Más adelante podría hacer otras validaciones aquí
    como por ejemplo, que sólo sea válido si el path existe)

    Args:
        path (str|Path): El path que se desea normalizar

    Returns:
        Path|None: El Path normalizado o None si no es válido
    """
    # Si es un string vacío se asume que no tiene significado (A pesar de que 
    # la librería Path lo asume como ".")
    if path == "":
        return None
    # Si ya es una instancia de Path, pues sólo se retorna el Path
    if isinstance(path, Path):
        return path
    # Si era otra cosa, se vuelve Path y se retorna
    try:
        return Path(path)
    # En caso de no poder volverse Path se devuelve None
    except TypeError:
        return None
    
def json_serializable_path(path:Path):
    if isinstance(path, Path):
        return str(path.absolute())
    return None