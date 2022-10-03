from dataclasses import dataclass
import datetime


@dataclass
class XweekEvent:
    name: str
    name_abbreviation: str
    location: str
    event_location_abbreviation: str
    event_version: int
    event_domain: str
    event_media_url: str
    event_long_description: str
    event_short_description: str
    event_calendar: str
    restaurants: list
    created: str = datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")
    
    
