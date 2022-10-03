import enum


class AppActions(enum.Enum):
    COMPLETE_PROCESS = enum.auto()
    CREATE_NEW_EVENT = enum.auto()
    


print(list(AppActions))
