import hashlib
import uuid
from django.shortcuts import render

# Create your views here.
import math
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# In-memory storages
points_dict = {} #stores "id" : points
receipts_map = {} #stores "hashed receipt" : "id"

#Converting receipts to str and hashing the receipt for easy storage
def receipts_hashing(receipt):
    receipt_tostr = str(receipt).encode('utf-8')
    return hashlib.sha256(receipt_tostr).hexdigest()


def calculate_points(receipt):
    
    points = 0

    #retailer = receipt.get('retailer', None)
    #items_list = receipt.get('items', [])
    #total = receipt.get('total', None)
    #print("TESTTTTTTTTTTT")
    #print("TESTTTTTTTTTTT")

    #if (retailer == None) or (items_list == []) or (total == None):
        #raise ValueError("Receipts is missing required details")


    # calculating points for the alphanumeric char in retailer name 
    retailer_tuple = tuple(char for char in receipt['retailer'] if char.isalnum()== True)
    points += len(retailer_tuple)

    total = float(receipt['total'])

    # checking if total is a round dollar amount
    if total.is_integer():
        points += 50

    # checking if total is a multiple of 0.25
    if total % 0.25 == 0:
        points += 25

    # calculating points for every two items using integer division
    points += (len(receipt['items']) // 2) * 5

    # checking if the striped description length is a multiple of 3
    for product in receipt['items']:
        descrp = product['shortDescription'].strip()
        if len(descrp) % 3 == 0:
            price = float(product['price'])
            points += math.ceil(price * 0.2)

    # checking if purchase day is odd using datetime function
    purchase_date = datetime.strptime(receipt['purchaseDate'], '%Y-%m-%d')
    if purchase_date.day % 2 != 0:
        points += 6

    # checking if purchase time is between 2:00pm - 4:00pm using the datetime function
    purchase_time = datetime.strptime(receipt['purchaseTime'], '%H:%M')
    if 14 <= purchase_time.hour < 16:
        points += 10

    return points
    
 
# API class to post the json receipt and get the ID for the receipt
class ProcessReceiptsView(APIView):
    def post(self, request):
        receipt = request.data
        # I am hashing all the receipts initially 
        hash_bill = receipts_hashing(receipt)

        # checking if a receipt is already uploaded to avoid duplication, unnecessary id creation and calculation.
        if hash_bill in receipts_map:
            id = receipts_map[hash_bill]
            return Response({"id": id, "message": "Receipt already uploaded."}, status=status.HTTP_200_OK)
        
        else:
            receipt_id = str(uuid.uuid4())
            receipts_map[hash_bill] = receipt_id
            points = calculate_points(receipt)
            points_dict [receipt_id] = points
            return Response({"id": receipt_id}, status=status.HTTP_200_OK)
        
# API class to get the points for the ID.
class GetPointsView(APIView):
    def get(self, request, id):
        points = points_dict[id]
        if points is None:
            return Response({"error": "Receipt not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"points": points}, status=status.HTTP_200_OK)

