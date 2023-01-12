import unittest
import urllib.request
import sqlite3
from app import hello_world, init_db, upsert_product, get_products, set_products



class UnitTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect("file::memory:?cache=shared", uri=True)
        init_db("file::memory:?cache=shared")

    @classmethod
    def tearDownClass(cls):     
        cls.conn.close()  

    def test_hello(self):
        d = hello_world()
        self.assertEqual(d, "<p>Hello, World!</p>")

    def test_upsert_product(self):

        preexisting_abc = next(filter(lambda p: p["sku"]=="abc", get_products()), None)
        self.assertIsNone(preexisting_abc)

        abc = {
            "sku": "abc",
            "attributes": {
                "size": "small",
                "grams": "100",
                "foo": "bar"
            },
        }
        upsert_product(abc)

        inserted_abc = next(filter(lambda p: p["sku"]=="abc", get_products()), None)
        self.assertIsNotNone(inserted_abc)
        self.assertDictEqual(inserted_abc["attributes"], abc["attributes"])

        abc["attributes"]["grams"] = "101"

        upsert_product(abc)

        updated_abc = next(filter(lambda p: p["sku"]=="abc", get_products()), None)
        self.assertIsNotNone(updated_abc)
        self.assertEqual(updated_abc["attributes"]["grams"], "101")

    def test_set_products_get_products(self):
        new_products = [
            {
                "sku": "def",
                "attributes": {
                    "size": "medium",
                    "grams": "120",
                    "foo": "bag"
                    }
            },
            {
                "sku": "ghi",
                "attributes": {
                    "size": "large",
                    "grams": "140",
                    "bah": "bah"
                    }
            },
        ]
        set_products(new_products)

        products = get_products()
        products.sort(key=lambda p: p["sku"])
        self.assertEquals(len(products), 2)
        self.assertEqual(new_products[0]['sku'], products[0]['sku'])
        self.assertDictEqual(new_products[0]['attributes'], products[0]['attributes'])
        self.assertEqual(new_products[1]['sku'], products[1]['sku'])
        self.assertDictEqual(new_products[1]['attributes'], products[1]['attributes'])


class IntegrationTests(unittest.TestCase):

    def test_post_and_then_get(self):
        with urllib.request.urlopen('http://127.0.0.1:5000') as f:
            d = f.read().decode('utf-8')
        self.assertEqual(d, "<p>Hello, World!</p>")


if __name__ == '__main__':
    unittest.main()
    