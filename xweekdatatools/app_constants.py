import enum

DB_FILE_PATH = "./xweekdatatools/db.json"
class AppActions(enum.Enum):
    SELECT_ACTION = enum.auto()
    CREATE_NEW_EVENT = enum.auto()
    UPDATE_EVENT_DATA = enum.auto()
    FIND_EVENT_DOCS = enum.auto()
    UPDATE_EVENT_DOCS_LIST = enum.auto()
    COLLECT_IMAGES = enum.auto()
    SHOW_DISHES = enum.auto()
    COLLECT_EVENT_IMAGES = enum.auto()
    COLLECT_RESTAURANT_LOGO = enum.auto()
    COLLECT_DISH_PHOTO = enum.auto()
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
            AppActions.CREATE_NEW_EVENT: "Crear nuevo evento",
            AppActions.UPDATE_EVENT_DATA: "Actualizar datos del evento",
            AppActions.FIND_EVENT_DOCS: "Encontrar docs del evento",
            AppActions.UPDATE_EVENT_DOCS_LIST: "Actualizar lista de docs del evento",
            AppActions.COLLECT_IMAGES: "Recolectar imágenes en una carpeta",
            AppActions.SHOW_DISHES: "Ver platos del evento",
            AppActions.COLLECT_EVENT_IMAGES: "Recolectar imágenes del evento en una carpeta",
            AppActions.COLLECT_RESTAURANT_LOGO: "Recolectar logo del restaurante",
            AppActions.COLLECT_DISH_PHOTO: "Recolectar foto del plato",
            AppActions.CONVERT_DOCS2TXT: "Convertir docs a texto plano (prenormalizado)",
            AppActions.NORMALIZE_TXT: "Normalizar lista de txts manualmente",
            AppActions.CONVERT_TXT2DATA: "Convertir txts a datos",
            AppActions.GEN_EVENT_JSON: "Generar JSON del evento",
            AppActions.GEN_EVENT_CSV: "Generar CSV de URLs del evento",
            AppActions.GEN_EVENT_XLSX: "Generar Excel de URLs del evento",
            AppActions.GEN_EVENT_QRS: "Generar QRs del evento",
            AppActions.EXIT: "SALIR DE LA APLICACIÓN",
        }
        if self in action_message:
            return action_message[self]
        return "Acción no definida"


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
        "emojis": ["🍟"]
    },
    {
        "context": "dish",
        "key": "drinks",
        "emojis": ["🍺"]
    },
    {
        "context": "dish",
        "key": "pairing",
        "emojis": ["🥤"]
    },
    {
        "context": "dish",
        "key": "price",
        "emojis": ["💵"]
    },
    {
        "context": "restaurant",
        "key": "address",
        "emojis": ["📍"]
    },
    {
        "context": "restaurant",
        "key": "phone",
        "emojis": ["☎️", "☎"]
    },
    {
        "context": "restaurant",
        "key": "opening_hours",
        "emojis": ["⏰"]
    },
    {
        "context": "restaurant",
        "key": "delivery",
        "emojis": ["🚚"]
    }
]
REST_DATA_SEPARATORS_DICT = {
    "🍽": {
        "context": "dish",
        "key": "name",
        "emojis": ["🍽️", "🍽"]
    },
    "🍽️": {
        "context": "dish",
        "key": "name",
        "emojis": ["🍽️", "🍽"]
    },
    "🍔": {
        "context": "dish",
        "key": "description",
        "emojis": ["🍕", "🍔"]
    },
    "🍕": {
        "context": "dish",
        "key": "description",
        "emojis": ["🍕", "🍔"]
    },
    "🍟": {
        "context": "dish",
        "key": "accompaniment",
        "emojis": ["🍟"]
    },
    "🍺": {
        "context": "dish",
        "key": "drinks",
        "emojis": ["🍺"]
    },
    "🥤": {
        "context": "dish",
        "key": "pairing",
        "emojis": ["🥤"]
    },
    "💵": {
        "context": "dish",
        "key": "price",
        "emojis": ["💵"]
    },
    "📍": {
        "context": "restaurant",
        "key": "address",
        "emojis": ["📍"]
    },
    "☎": {
        "context": "restaurant",
        "key": "phone",
        "emojis": ["☎️", "☎"]
    },
    "☎️": {
        "context": "restaurant",
        "key": "phone",
        "emojis": ["☎️", "☎"]
    },
    "⏰": {
        "context": "restaurant",
        "key": "opening_hours",
        "emojis": ["⏰"]
    },
    "🚚": {
        "context": "restaurant",
        "key": "delivery",
        "emojis": ["🚚"]
    }
}

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