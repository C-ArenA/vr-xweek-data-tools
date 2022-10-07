import enum

DB_FILE_PATH = "./xweekdatatools/db.json"
class AppActions(enum.Enum):
    SELECT_ACTION = enum.auto()
    # COMPLETE_PROCESS = enum.auto()
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
    
    def message(self):
        action_message = {
			AppActions.SELECT_ACTION: "Seleccionar una acción",
			#AppActions.COMPLETE_PROCESS: "Realizar el procedimiento completo",
			AppActions.CREATE_NEW_EVENT: "Crear nuevo evento",
			AppActions.UPDATE_EVENT_DATA: "Actualizar datos del evento",
			AppActions.FIND_EVENT_DOCS: "Encontrar docs del evento",
			AppActions.UPDATE_EVENT_DOCS_LIST: "Actualizar lista de docs del evento",
			AppActions.FIND_EVENT_IMAGES: "Encontrar imágenes del evento",
			AppActions.COLLECT_EVENT_IMAGES: "Recolectar imágenes del evento en una carpeta",
			AppActions.CONVERT_DOCS2TXT: "Convertir docs a texto plano (prenormalizado)",
			AppActions.NORMALIZE_TXT: "Normalizar lista de txts manualmente",
			AppActions.CONVERT_TXT2DATA: "Convertir txts a datos",
			AppActions.GEN_EVENT_JSON: "Generar JSON del evento",
			AppActions.GEN_EVENT_CSV: "Generar CSV de URLs del evento",
			AppActions.GEN_EVENT_XLSX: "Generar Excel de URLs del evento",
			AppActions.GEN_EVENT_QRS: "Generar QRs del evento",
			AppActions.EXIT: "SALIR DE LA APLICACIÓN",
		}
        return action_message[self]


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

