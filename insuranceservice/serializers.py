from rest_framework import serializers

from .models import InsurancePeriod, InsuranceCategory, InsuranceType, \
    PremiumPercentage, AssetInsurance, InsuranceClaim, ClaimDocument


class InsuranceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceCategory
        fields = '__all__'


class InsuranceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceType
        fields = '__all__'


class InsurancePeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsurancePeriod
        fields = '__all__'


class PremiumPercentageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremiumPercentage
        fields = '__all__'



class AssetInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetInsurance
        fields = '__all__'
        read_only_fields = ['created_by', 'insurance_number']


    def create(self, validated_data):
        created_by = self.context['request'].user
        if isinstance(validated_data, list):
            for item in validated_data:
                item['created_by'] = created_by
            return AssetInsurance.objects.bulk_create([
                AssetInsurance(**item) for item in validated_data
            ])
        validated_data['created_by'] = created_by
        return super().create(validated_data)





class ClaimDocumentSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = ClaimDocument
        fields = ['id', 'file', 'uploaded_at']

    def get_file(self, obj):
        request = self.context.get('request')
        if obj.file:
            return request.build_absolute_uri(obj.file.url)
        return None

class InsuranceClaimSerializer(serializers.ModelSerializer):
    claim_documents = ClaimDocumentSerializer(many=True, read_only=True)
    claim_muzzle = serializers.SerializerMethodField()
    settlement_documents = serializers.SerializerMethodField()

    class Meta:
        model = InsuranceClaim
        fields = '__all__'
        read_only_fields = ['created_by', 'updated_by', 'insured_asset']

    def get_claim_muzzle(self, obj):
        request = self.context.get('request')
        if obj.claim_muzzle:
            return request.build_absolute_uri(obj.claim_muzzle.url)
        return None

    def get_settlement_documents(self, obj):
        request = self.context.get('request')
        if obj.settlement_documents:
            return request.build_absolute_uri(obj.settlement_documents.url)
        return None

from rest_framework import serializers
from .models import PaymentInformation, TransactionDocument

class TransactionDocumentSerializer(serializers.ModelSerializer):
    document = serializers.SerializerMethodField()

    class Meta:
        model = TransactionDocument
        fields = ['id', 'document', 'uploaded_at']

    def get_document(self, obj):
        request = self.context.get('request')
        if obj.document and request:
            return request.build_absolute_uri(obj.document.url)
        elif obj.document:
            return obj.document.url
        return None

class PaymentInformationSerializer(serializers.ModelSerializer):
    trx_documents = serializers.ListField(
        child=serializers.FileField(),
        write_only=True
    )

    class Meta:
        model = PaymentInformation
        fields = [
            'trx_id', 'amount', 'trx_date', 'trx_type', 'trx_through', 'assetInsuranceId', 'remarks',
            'trx_documents'
        ]

    def create(self, validated_data):
        trx_documents = validated_data.pop('trx_documents', [])
        payment = PaymentInformation.objects.create(**validated_data, created_by=self.context['request'].user)

        for file in trx_documents:
            TransactionDocument.objects.create(payment=payment, document=file)

        return payment

class PaymentInformationDetailSerializer(serializers.ModelSerializer):
    trx_documents = TransactionDocumentSerializer(many=True, read_only=True)
    created_by = serializers.StringRelatedField()

    class Meta:
        model = PaymentInformation
        fields = [
            'id', 'trx_id', 'amount', 'trx_date', 'trx_type', 'trx_through','assetInsuranceId', 'remarks',
            'created_by', 'created_at', 'trx_documents'
        ]
