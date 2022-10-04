from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass
class XweekDish:
    name: str = ""
    description: str = ""
    accompaniment: str = ""
    drinks: str = ""
    pairing: str = ""
    price: str = ""
    photo_path: Path = None
    photo_name: str = ""
    photo_stem: str = ""
    photo_ext: str = ""
    photo_url: str = ""

    def to_dict(self):
        return asdict(self)
