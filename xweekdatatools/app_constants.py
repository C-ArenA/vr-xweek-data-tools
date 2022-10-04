import enum

DB_FILE_PATH = "./xweekdatatools/db.json"
class AppActions(enum.Enum):
    COMPLETE_PROCESS = enum.auto()
    CREATE_NEW_EVENT = enum.auto()
    UPDATE_EVENT_DATA = enum.auto()
    FIND_EVENT_DOCS = enum.auto()
    UPDATE_EVENT_DOCS_LIST = enum.auto()
    FIND_EVENT_IMAGES = enum.auto()
    COLLECT_EVENT_IMAGES = enum.auto()
    CONVERT_DOCS2TXT = enum.auto()
    NORMALIZE_TXT = enum.auto()
    CONVERT_TXT2DATA = enum.auto()
    GEN_EVENT_JSON = enum.auto()
    GEN_EVENT_CSV = enum.auto()
    GEN_EVENT_XLSX = enum.auto()
    GEN_EVENT_QRS = enum.auto()
    EXIT = enum.auto()


REST_DATA_SEPARATORS = [
    {
        "context": "dish",
        "key": "name",
        "emojis": ["🍽️", "🍽"]
    },
    {
        "context": "dish",
        "key": "description",
        "emojis": ["🍕", "🍔"]
    },
    {
        "context": "dish",
        "key": "accompaniment",
        "emoji": "🍟"
    },
    {
        "context": "dish",
        "key": "drinks",
        "emoji": "🍺"
    },
    {
        "context": "dish",
        "key": "pairing",
        "emoji": "🥤"
    },
    {
        "context": "dish",
        "key": "price",
        "emoji": "💵"
    },
    {
        "context": "restaurant",
        "key": "address",
        "emoji": "📍"
    },
    {
        "context": "restaurant",
        "key": "phone",
        "emojis": ["☎️", "☎"]
    },
    {
        "context": "restaurant",
        "key": "opening_hours",
        "emoji": "⏰"
    },
    {
        "context": "restaurant",
        "key": "delivery",
        "emoji": "🚚"
    }
]
