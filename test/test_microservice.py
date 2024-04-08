import unittest
from src.microservice import query_properties

class TestMicroservice(unittest.TestCase):
    def test_query_with_no_filters(self):
        """Testear consulta de propiedades sin filtros."""
        results = query_properties({})
        self.assertIsInstance(results, list)

        for result in results:
            self.assertIn(result['state'], ['pre_venta', 'en_venta', 'vendido'])

    def test_query_with_filters(self):
        """Testear consulta de propiedades con filtros."""
        filters = {'city': 'bogota', 'state': 'en_venta'}
        results = query_properties(filters)
        self.assertIsInstance(results, list)
        for result in results:
            self.assertEqual(result['city'], 'bogota')
            self.assertEqual(result['state'], 'en_venta')

if __name__ == '__main__':
    unittest.main()
