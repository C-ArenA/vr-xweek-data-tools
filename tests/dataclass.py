from dataclasses import asdict, dataclass


@dataclass
class DataClass:
    a: str
    b: int
    c: str
    
    def to_dict(self):
        return asdict(self)

dc = DataClass(
    input("ingrese a:"),
    input("ingrese b:"),
    input("ingrese c:")
)

print(dc.to_dict())