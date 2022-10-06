from pathlib import Path
import unittest
from xweekdatatools.models import XweekRestaurant
from xweekdatatools.models.model import Model
from xweekdatatools.models.xweek_event import XweekEvent
from xweekdatatools.views.view import View
view = View()

def createRestaurantTest():
    xwr = XweekRestaurant(view=view)
    print(xwr)


class XweekRestaurantTest(unittest.TestCase):
    def test_instantiate(self):
        xwr = XweekRestaurant(view=view)
        self.assertIsInstance(xwr, XweekRestaurant)
        self.assertIsInstance(xwr, Model)
        self.assertNotIsInstance(xwr, XweekEvent)
    
    def test_post_init(self):
        xwr = XweekRestaurant(id="3", name="PizzaTower", dishes=5, event_id=4)
        print("--------\n")
        print(xwr)
        print("--------\n")
        self.assertEqual(xwr.id, 3)
        self.assertEqual(xwr.name, "PizzaTower")
        self.assertEqual(xwr.dishes, list())
        
    def test_create_restaurant(self):
        xwr = XweekRestaurant(name="Pizza Tower Ñandú", dishes=5, view=view)
        xwr.address = "Avenida Patito"
        xwr.save()
        
def test_create_restaurant():
    xwr = XweekRestaurant(name="Pizza Tower Ñandú", dishes=5, view=view)
    xwr.save(XweekEvent(id=5, name="Pizza Week", domain="pw.com", location="La Paz", location_abbreviation="lp", version=6))
    #xwr.save()
    print(xwr)

def print_keys():
    print([json_field.name for json_field in XweekRestaurant.to_json_fields()])
test_create_restaurant()
if __name__ == "__main__":
    # py -m unittest tests.modedls_tests.xweek_restaurant_test
    #unittest.main()
    pass