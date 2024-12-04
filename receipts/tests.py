import math
from django.test import TestCase
from receipts import views
# Create your tests here.

class CalculatePointsTestCase(TestCase):
    
    # Test case to check if the exception raises when the receipt is empty
    def test_cal_points_exception(self):
        input = {}
        with self.assertRaises(ValueError) as ve:
            views.calculate_points(input)
        self.assertEqual(str(ve.exception), "Receipt is missing required details. Upload the complete receipt with retailer, items, total, and date.")

    # Test case to check if the exception raises when the receipt is missing only one key
    def test_exception_no_retailer(self):
        receipt = {"purchaseDate": "2022-01-01",
                   "purchaseTime": "13:01",
                   "items": [{"shortDescription": "Mountain Dew 12PK","price": "6.49"},
                             {"shortDescription": "Emils Cheese Pizza","price": "12.25"}],
                    "total": "35.35"}
        with self.assertRaises(ValueError) as ve:
            views.calculate_points(receipt)
        self.assertEqual(str(ve.exception), "Receipt is missing required details. Upload the complete receipt with retailer, items, total, and date.")

    #Test case to check alphanumeric retailer name points
    def test_alphanumeric_retailer_points(self):
        receipt = {
            "retailer": "Forever21", 
            "purchaseDate": "2022-01-04",
            "purchaseTime": "13:01",
            "items": [{"shortDescription": "Mountain","price": "1"}],
            "total": "0.2"
        }
        points = views.calculate_points(receipt)
        self.assertEqual(points, 9)

    # Test case to check non alphanumeric retailer points
    def test_non_alphanumeric_retailer_points(self):
        receipt = {
            "retailer": "F@rever!! 21$",
            "purchaseDate": "2022-01-04",
            "purchaseTime": "13:01",
            "items": [{"shortDescription": "Mountain","price": "1"}],
            "total": "0.2"
        }
        points = views.calculate_points(receipt)
        self.assertEqual(points, 8)

    # Test case to check round dollar total amount and multiple of 0.25 points
    def test_total_round_amount_multiple(self):
        receipt = {
            "retailer": "$@!!$",
            "purchaseDate": "2022-01-04",
            "purchaseTime": "13:01",
            "items": [{"shortDescription": "Mountain","price": "1"}],
            "total": "20.00"
        }
        points = views.calculate_points(receipt)
        self.assertEqual(points, 75)

    # Test case to check only multiple of 0.25 points
    def test_multiple(self):
        receipt = {
            "retailer": "$@!!$",
            "purchaseDate": "2022-01-04",
            "purchaseTime": "13:01",
            "items": [{"shortDescription": "Mountain","price": "1"}],
            "total": "10.75"
        }
        points = views.calculate_points(receipt)
        self.assertEqual(points, 25)

    # Test case to check item pairs points
    def test_item_pairs(self):
        receipt = {
            "retailer": "$@!!$",
            "purchaseDate": "2022-01-04",
            "purchaseTime": "13:01",
            "items": [{"shortDescription": "Mountain","price": "1"}, {"shortDescription": "Mountain","price": "1"}],
            "total": "0.2"
        }
        points = views.calculate_points(receipt)
        self.assertEqual(points, 5)

    # Test case to check item description length multiple of 3 
    def test_item_desc_len(self):
        receipt = {
            "retailer": "$@!!$",
            "purchaseDate": "2022-01-04",
            "purchaseTime": "13:01",
            "items": [{"shortDescription": "Dew","price": "4.50"}],
            "total": "0.2"
        }
        points = views.calculate_points(receipt)
        self.assertEqual(points, math.ceil(4.50 * 0.2))

    # Test case to check the purchase date and see if points are added in case of odd day
    def test_odd_day(self):
        receipt = {
            "retailer": "$@!!$",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [{"shortDescription": "MountainDew","price": "4.50"}],
            "total": "0.2"
        }
        points_odd = views.calculate_points(receipt)
        self.assertEqual(points_odd, 6)

    # Test case to check the purchase time between 2:00pm - 4:00pm 
    def test_time_points(self):
        receipt = {
            "retailer": "$@!!$",
            "purchaseDate": "2022-01-04",
            "purchaseTime": "14:05",
            "items": [{"shortDescription": "MDew","price": "4.50"}],
            "total": "0.2"
        }
        points = views.calculate_points(receipt)
        self.assertEqual(points, 10)