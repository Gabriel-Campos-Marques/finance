from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Account, CreditCard
from .serializers import AccountSerializer, CreditCardSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

class CreditCardViewSet(viewsets.ModelViewSet):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer
    permission_classes = [IsAuthenticated]
