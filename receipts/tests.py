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