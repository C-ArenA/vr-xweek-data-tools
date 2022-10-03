from dataclasses import asdict, dataclass
import datetime


@dataclass
class XweekEvent:
    name: str
    name_abbreviation: str
    location: str
    location_abbreviation: str
    version: int
    domain: str
    media_url: str
    long_description: str
    short_description: str
    calendar: str
    restaurants: list
    created: str = datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")

    def to_dict(self):
        return asdict(self)
