from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers import TransactionImportSerializer

class TransactionImportView(APIView):
    """
    Endpoint para realizar o upload e importação de dados de transações (CSV, OFX, Excel, PDF)
    para diferentes instituições (Nubank, Porto Seguro, Banco Inter, Mobills).
    """
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(
        request=TransactionImportSerializer,
        responses={200: dict},
        description="Realiza a importação de planilhas/arquivos contendo transações financeiras."
    )
    def post(self, request, *args, **kwargs):
        institution = request.data.get('institution')
        file_type = request.data.get('file_type')
        upload_file = request.FILES.get('file')

        # Validação básica
        if not institution or not file_type or not upload_file:
            return Response(
                {"error": "É necessário informar 'institution', 'file_type' e enviar um 'file'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # TODO: Crie a função genérica ou roteador nos services do app integrations
        # Exemplo comentado:
        #
        # from apps.integrations.services.importer import process_import
        # try:
        #     process_import(institution=institution, file_type=file_type, file=upload_file)
        # except Exception as e:
        #     return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "message": "Arquivo recebido com sucesso.",
                "institution": institution,
                "file_type": file_type,
                "filename": upload_file.name
            },
            status=status.HTTP_200_OK
        )
