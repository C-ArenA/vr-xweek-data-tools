from dataclasses import asdict, dataclass
from xweekdatatools.models.xweek_dish import XweekDish


@dataclass
class XweekRestaurant:
    order: int = 0
    name: str = ""
    address: str = ""
    phone: str = ""
    opening_hours: str = ""
    delivery: str = ""
    slugified_name: str = ""
    post_title: str = ""
    post_name: str = ""
    post_url: str = ""
    logo_name: str = ""
    logo_url: str = ""
    dishes: list[XweekDish] = None

    def to_dict(self):
        return asdict(self)
