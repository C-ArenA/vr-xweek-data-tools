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

TXT_FORMAT = """🍽️ Tamarindo Smokey Bomb 
🍔 Pan Brioche artesanal, rúcula, Hamburguesa de cortes premium a la parrilla, queso cheddar y mermelada de tamarindo, queso provolone derretido con aceite de oliva y orégano y albahaca; tomates deshidratados y tocino crocante. 
🍟 Papas o Camotes Curly. 
🍺 Huari Tradicional o Huari Miel o Huari Chocolate o Pepsi o Pepsi Light o 7Up 
🥤 Huari Tradicional 
💵 Precio: Bs. 55 
🍽️ CHEESERoom 
🍔 Pan Brioche artesanal, cheese burger americana, lechuga, tomate y cheddar; carne premium de hamburguesa a la parrilla, shroom burger: hamburguesa empanizada con hongos crocantes y rellena de dos tipos de queso, cheddar y mozzarella, acompañada de salsa especial. 
🍟 Papas o Camotes Curly. 
🍺 Huari Tradicional o Huari Miel o Huari Chocolate o Pepsi o Pepsi Light o 7Up 
🥤 Huari Chocolate 
💵 Precio: Bs. 55 
🍽️ Veggieroom 
🍔 Pan Brioche artesanal, lechuga, tomate y cheddar con una shroom burger: hamburguesa empanizada con hongos crocantes y rellena de dos tipos de queso, cheddar y mozzarella, acompañada de salsa especial. 
🍟 Papas o Camotes Curly. 
🍺 Huari Tradicional o Huari Miel o Huari Chocolate o Pepsi o Pepsi Light o 7Up 
🥤 Huari Miel 
💵 Precio: Bs. 55 
📍 Av. San Martín, esquina Leonardo Nava, entre 3er y 4to anillo. Av. Cuarto Anillo, entre Av. Beni y av. Banzer, en Patio de Comidas Con Tenedores Norte 
☎️ 75552233 Cuarto Anillo: 69203924 
⏰ Lunes a domingos 11:00 a 23:30 
🚚 PedidosYa y Yaigo
"""