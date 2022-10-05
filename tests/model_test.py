from xweekdatatools.models import Model
from pathlib import Path
import unittest

from xweekdatatools.models.xweek_event import XweekEvent

def json_correspondance_test():
    print(Model.json_dict_correspondace(Model.get_current_db_state()["xweekevents"][0]))
    
def decode_json_test():
    m = Model()
    assert(m.decode_json_attr(0, "int") == 0)

class TestModel(unittest.TestCase):
    def test_decode_json_int(self):
        m = Model()
        inputs_list = [0,1,-1,"5", "a", None, {"a":4}, [1,2,3], Path("f:/")]
        gen_list = [m.decode_json_attr(value, "int") for value in inputs_list]
        expect_list = [0,1,-1,5,None, None, None, None, None]
        self.assertListEqual(gen_list, expect_list)
    def test_decode_json_str(self):
        m = Model()
        inputs_list = [0,1,-1,"5", "a", True, None, {"a":4}, [1,2,3], Path("f:/"), "f:/"]
        gen_list = [m.decode_json_attr(value, "str") for value in inputs_list]
        expect_list = ["0","1","-1","5","a", "True", None, None, None, None, "f:/"]
        self.assertListEqual(gen_list, expect_list)
    def test_decode_json_path(self):
        m = Model()
        inputs_list = [0,1,-1,"5", "a", True, None, {"a":4}, [1,2,3], Path("f:/"), "f:/"]
        gen_list = [m.decode_json_attr(value, "Path") for value in inputs_list]
        expect_list = [None,None,None,Path("5"),Path("a"),None,None,None,None,Path("f:/"), Path("f:/")]
        self.assertListEqual(gen_list, expect_list)
    def test_decode_json_list(self):
        m = Model()
        inputs_list = [0,1,-1,"5", "a", True, None, {"a":4}, [1,2,3], Path("f:/"), "f:/"]
        gen_list = [m.decode_json_attr(value, "list[]") for value in inputs_list]
        expect_list = [list(),list(),list(),list(),list(),list(),list(),list(),[1,2,3],list(), list()]
        self.assertListEqual(gen_list, expect_list)
    def test_decode_json_list_int(self):
        m = Model()
        inputs_list = [0,1,-1,"5", "a", True, None, {"a":4}, [1,2,3], Path("f:/"), "f:/"]
        gen_list = [m.decode_json_attr(value, "list[int]") for value in inputs_list]
        expect_list = [list(),list(),list(),list(),list(),list(),list(),list(),[1,2,3],list(), list()]
        self.assertListEqual(gen_list, expect_list)
    def test_decode_json_list_events(self):
        m = Model()
        e = XweekEvent.getAll()[-1]
        inputs_list = [0,     1,     -1,    "5",   "a",   True,  None,  {"a":4}, [1,2,3], Path("f:/"), "f:/",  [e.json_serializable_dict()]]
        gen_list = [m.decode_json_attr(value, "list[XweekEvent]") for value in inputs_list]
        expect_list = [list(),list(),list(),list(),list(),list(),list(),list(),  list(),  list(),      list(), [e]]
        self.assertListEqual(gen_list, expect_list)
    
if __name__ == "__main__":
	unittest.main()