from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers import TransactionImportSerializer

from apps.integrations.functions.import_file import ImportFile

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
        account_id = request.data.get('account_id')
        year = request.data.get('year')

        # Validação básica
        if not institution or not file_type or not upload_file:
            return Response(
                {"error": "É necessário informar 'institution', 'file_type' e enviar um 'file'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if institution.lower() in ['porto', 'porto seguro'] and file_type.lower() == 'excel':
                if not account_id or not year:
                    return Response(
                        {"error": "Para a Porto Seguro, é necessário informar 'account_id' e 'year'."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                # Instantiate factory
                importer = ImportFile(upload_file)
                inserted_hashes = importer.porto_seguro_import(int(account_id), int(year))
                
                return Response(
                    {
                        "message": f"Fatura da Porto Seguro importada com sucesso. {len(inserted_hashes)} novas transações inseridas.",
                        "institution": institution,
                        "file_type": file_type,
                        "filename": upload_file.name
                    },
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "message": "Integração para este tipo de arquivo não implementada ou não aplicável.",
                "institution": institution,
                "file_type": file_type,
                "filename": upload_file.name
            },
            status=status.HTTP_400_BAD_REQUEST
        )

from django.http import HttpResponse
from datetime import datetime
from apps.integrations.functions.export_mobills import MobillsExporter

class MobillsExportView(APIView):
    """
    Endpoint para exportar transações no formato Mobills.
    """
    def get(self, request, *args, **kwargs):
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        
        start_date = None
        end_date = None
        
        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({"error": "Formato de data inválido. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
                
        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({"error": "Formato de data inválido. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            excel_file = MobillsExporter.export(start_date=start_date, end_date=end_date)
            
            response = HttpResponse(
                excel_file.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=Exportado_Mobills.xlsx'
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
