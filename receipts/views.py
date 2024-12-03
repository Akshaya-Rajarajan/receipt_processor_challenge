from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import uuid
import math

receipts = {}

def calculate_points(receipt):
    points = 0

    # Rule 1: One point for every alphanumeric character in retailer name
    points += sum(char.isalnum() for char in receipt['retailer'])

    # Rule 2: 50 points if total is a round dollar amount
    total = float(receipt['total'])
    if total.is_integer():
        points += 50

    # Rule 3: 25 points if total is a multiple of 0.25
    if total % 0.25 == 0:
        points += 25

    # Rule 4: 5 points for every two items
    points += (len(receipt['items']) // 2) * 5

    # Rule 5: Points for item descriptions with trimmed length as a multiple of 3
    for item in receipt['items']:
        description = item['shortDescription'].strip()
        if len(description) % 3 == 0:
            price = float(item['price'])
            points += math.ceil(price * 0.2)

    # Rule 6: 6 points if purchase day is odd
    purchase_date = datetime.strptime(receipt['purchaseDate'], '%Y-%m-%d')
    if purchase_date.day % 2 != 0:
        points += 6

    # Rule 7: 10 points if purchase time is between 2:00pm and 4:00pm
    purchase_time = datetime.strptime(receipt['purchaseTime'], '%H:%M')
    if 14 <= purchase_time.hour < 16:
        points += 10

    return points

class ProcessReceiptsView(APIView):
    def post(self, request):
        receipt = request.data
        receipt_id = str(uuid.uuid4())
        points = calculate_points(receipt)
        receipts[receipt_id] = points
        return Response({"id": receipt_id}, status=status.HTTP_200_OK)

class GetPointsView(APIView):
    def get(self, request, id):
        points = receipts.get(id)
        if points is None:
            return Response({"error": "Receipt not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"points": points}, status=status.HTTP_200_OK)


