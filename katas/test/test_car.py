import unittest
from python_katas.car import Car


class TestCarL1(unittest.TestCase):
    def test_car_attributes(self):
        my_car = Car("Toyota", 2010)
        self.assertEqual(my_car.model, "Toyota")
        self.assertEqual(my_car.year, 2010)
        self.assertFalse(my_car.is_rented())

    def test_rent_car(self):
        my_car = Car("Toyota", 2010)
        my_car.rent_car()
        self.assertTrue(my_car.is_rented())

    def test_return_car(self):
        my_car = Car("Toyota", 2010)

        with self.assertRaises(RuntimeError):
            my_car.return_car()

        my_car.rent_car()
        self.assertTrue(my_car.is_rented())

        my_car.return_car()
        self.assertFalse(my_car.is_rented())


if __name__ == '__main__':
    unittest.main()
