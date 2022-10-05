from dataclasses import asdict, dataclass, fields


@dataclass
class DataClass:
    a: str
    b: int
    c: str
    
    def to_dict(self):
        return asdict(self)

# dc1 = DataClass(
#     input("ingrese t:"),
#     input("ingrese a:"),
#     input("ingrese b:"),
#     input("ingrese c:")
# )
dc_dict = {
	"a": 5,
	"b": 4,
	"c": 3,	
	"d": 2
}
dc = DataClass(**dc_dict)

print(dc.to_dict())

