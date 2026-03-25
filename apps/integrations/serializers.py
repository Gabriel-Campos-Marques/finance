from rest_framework import serializers

class TransactionImportSerializer(serializers.Serializer):
    institution = serializers.CharField(
        required=True,
        help_text="Nome da instituição financeira (ex: nubank, porto, inter, mobills)"
    )
    file_type = serializers.CharField(
        required=True,
        help_text="Formato do arquivo enviado (ex: ofx, csv, excel, pdf)"
    )
    file = serializers.FileField(
        required=True,
        help_text="O arquivo físico contendo as transações"
    )
