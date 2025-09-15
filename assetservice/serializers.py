from django.contrib.auth import get_user_model
from rest_framework import serializers

from insuranceservice.models import AssetInsurance
from .models import (
    AssetHistory, AssetType, Breed, Color, VaccinationStatus,
    DewormingStatus
)

User = get_user_model()


class AssetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetType
        fields = ['id', 'name']


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['id', 'name', 'description']


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'description']


class VaccinationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccinationStatus
        fields = ['id', 'name', 'description']


class DewormingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DewormingStatus
        fields = ['id', 'name', 'description']

class AssetHistorySerializer(serializers.ModelSerializer):
    changed_by = serializers.StringRelatedField()

    class Meta:
        model = AssetHistory
        fields = '__all__'


from rest_framework import serializers
from .models import Asset


class AssetListSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()  # Show owner name (or another related field like mobile number)
    asset_type = serializers.StringRelatedField()  # Show asset type name
    breed = serializers.StringRelatedField()  # Show breed name
    color = serializers.StringRelatedField()  # Show color name
    vaccination_status = serializers.StringRelatedField()  # Show vaccination status name
    deworming_status = serializers.StringRelatedField()  # Show deworming status name

    # Media fields with absolute URL
    muzzle_video = serializers.SerializerMethodField()
    left_side_image = serializers.SerializerMethodField()
    right_side_image = serializers.SerializerMethodField()
    challan_paper = serializers.SerializerMethodField()
    vet_certificate = serializers.SerializerMethodField()
    chairman_certificate = serializers.SerializerMethodField()
    special_mark = serializers.SerializerMethodField()
    image_with_owner = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = ['id', 'owner', 'asset_type', 'breed', 'color', 'age_in_months', 'weight_kg', 'height',
                  'vaccination_status', 'last_vaccination_date', 'deworming_status', 'last_deworming_date',
                  'is_active', 'remarks', 'gender', 'reference_id', 'created_at', 'updated_at',
                  'muzzle_video', 'left_side_image', 'right_side_image', 'challan_paper', 'vet_certificate',
                  'chairman_certificate', 'special_mark', 'image_with_owner', 'purchase_date' , 'purchase_from' , 'purchase_amount']

    def get_media_url(self, obj, field_name):
        """Helper method to get the absolute URL of media files."""
        request = self.context.get('request')
        media_file = getattr(obj, field_name, None)
        if media_file and hasattr(media_file, 'url'):
            return request.build_absolute_uri(media_file.url)
        return None

    # Serializer Method Fields for media
    def get_muzzle_video(self, obj):
        return self.get_media_url(obj, 'muzzle_video')

    def get_left_side_image(self, obj):
        return self.get_media_url(obj, 'left_side_image')

    def get_right_side_image(self, obj):
        return self.get_media_url(obj, 'right_side_image')

    def get_challan_paper(self, obj):
        return self.get_media_url(obj, 'challan_paper')

    def get_vet_certificate(self, obj):
        return self.get_media_url(obj, 'vet_certificate')

    def get_chairman_certificate(self, obj):
        return self.get_media_url(obj, 'chairman_certificate')

    def get_special_mark(self, obj):
        return self.get_media_url(obj, 'special_mark')

    def get_image_with_owner(self, obj):
        return self.get_media_url(obj, 'image_with_owner')


class AssetSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), required=False)
    asset_type = serializers.PrimaryKeyRelatedField(queryset=AssetType.objects.all(), required=True)
    breed = serializers.PrimaryKeyRelatedField(queryset=Breed.objects.all(), required=True)
    color = serializers.PrimaryKeyRelatedField(queryset=Color.objects.all(), required=True)
    vaccination_status = serializers.PrimaryKeyRelatedField(queryset=VaccinationStatus.objects.all(), required=True)
    deworming_status = serializers.PrimaryKeyRelatedField(queryset=DewormingStatus.objects.all(), required=True)
    muzzle_video = serializers.FileField(required=True)
    left_side_image = serializers.ImageField(required=True)
    right_side_image = serializers.ImageField(required=True)
    challan_paper = serializers.FileField(required=True)
    vet_certificate = serializers.FileField(required=True)
    chairman_certificate = serializers.FileField(required=True)
    special_mark = serializers.FileField(required=True)
    image_with_owner = serializers.FileField(required=True)

    class Meta:
        model = Asset
        fields = '__all__'
        read_only_fields = ['created_by', 'updated_by', 'created_at', 'updated_at']

    def validate(self, attrs):
        user = self.context['request'].user

        # Check if all mandatory fields are present
        mandatory_fields = ['asset_type', 'breed', 'color', 'vaccination_status', 'deworming_status']
        for field in mandatory_fields:
            if field not in attrs or not attrs[field]:
                raise serializers.ValidationError({field: f"{field.replace('_', ' ').capitalize()} is mandatory."})


        if user.is_superuser:
            # If the user is not an owner (role.id != 1), the 'owner' must be explicitly passed in the request body
            if 'owner' not in attrs or not attrs['owner']:
                raise serializers.ValidationError({"owner": "Owner must be provided for users who are not owners."})

            # Optionally, you can add extra validation to ensure the passed owner is a valid user
            if attrs['owner'] == user:
                raise serializers.ValidationError({"owner": "You cannot assign the asset to yourself."})
        elif user.role.id == 1:
            # If the user is an owner (role.id == 1), automatically set owner to the current user
            attrs['owner'] = user
        else:
            # If the user is not an owner (role.id != 1), the 'owner' must be explicitly passed in the request body
            if 'owner' not in attrs or not attrs['owner']:
                raise serializers.ValidationError({"owner": "Owner must be provided for users who are not owners."})

            # Optionally, you can add extra validation to ensure the passed owner is a valid user
            if attrs['owner'] == user:
                raise serializers.ValidationError({"owner": "You cannot assign the asset to yourself."})

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        validated_data['updated_by'] = user

        # Create the asset
        asset = super().create(validated_data)

        return asset

    def update(self, instance, validated_data):
        user = self.context['request'].user
        instance.updated_by = user

        # Perform ownership validation during update as well
        if user.role.id == 1:
            if 'owner' in validated_data and validated_data['owner'] != user:
                raise serializers.ValidationError({"owner": "You cannot change the owner to another user."})
            validated_data['owner'] = user
        else:
            if 'owner' not in validated_data or not validated_data['owner']:
                raise serializers.ValidationError({"owner": "Owner must be provided for this role."})

        # Define fields that are allowed to be updated
        updatable_fields = [
            'age_in_months', 'weight_kg',
            'vaccination_status', 'last_vaccination_date', 'deworming_status',
            'last_deworming_date', 'health_issues', 'is_active',
            'remarks', 'muzzle_video', 'left_side_image',
            'right_side_image', 'challan_paper', 'vet_certificate',
            'chairman_certificate'
        ]

        # Iterate through the validated data and update only the allowed fields
        for field in updatable_fields:
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        # Save the updated instance
        instance.save()

        return instance

class AssetInsuranceListSerializer(serializers.ModelSerializer):
    asset = serializers.StringRelatedField()  # Return asset name instead of ID
    insurance_provider = serializers.StringRelatedField()  # Return insurance provider name
    created_by = serializers.StringRelatedField()  # Return created by user name
    updated_by = serializers.StringRelatedField()  # Return updated by user name

    # Media field with absolute URL
    insurance_certificate = serializers.SerializerMethodField()
    claim_status = serializers.SerializerMethodField()

    class Meta:
        model = AssetInsurance
        fields = [
            'id', 'asset', 'insurance_provider', 'insurance_number', 'sum_insured', 'premium_amount',
            'insurance_start_date', 'insurance_end_date', 'insurance_status', 'policy_terms',
            'insurance_certificate', 'insurance_agent', 'renewal_reminder_sent',
            'created_by', 'updated_by', 'created_at', 'updated_at', 'remarks', 'claim_status'
        ]

    def get_insurance_certificate(self, obj):
        """Return the absolute URL of the insurance certificate."""
        request = self.context.get('request')
        if obj.insurance_certificate and hasattr(obj.insurance_certificate, 'url'):
            return request.build_absolute_uri(obj.insurance_certificate.url)
        return None

    def get_claim_status(self, obj):
        """Return the claim status if the insurance is claimed."""
        latest_claim = obj.claims.order_by('-created_at').first()
        if latest_claim:
            return latest_claim.claim_status
        return "No Claim"

from django.conf import settings
from urllib.parse import urljoin

class CowSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.mobile_number', read_only=True)
    breed_name = serializers.CharField(source='breed.name', read_only=True)
    color_name = serializers.CharField(source='color.name', read_only=True)
    vaccination_status_name = serializers.CharField(source='vaccination_status.name', read_only=True)
    deworming_status_name = serializers.CharField(source='deworming_status.name', read_only=True)

    muzzle_video = serializers.SerializerMethodField()
    left_side_image = serializers.SerializerMethodField()
    right_side_image = serializers.SerializerMethodField()
    challan_paper = serializers.SerializerMethodField()
    vet_certificate = serializers.SerializerMethodField()
    chairman_certificate = serializers.SerializerMethodField()
    image_with_owner = serializers.SerializerMethodField()

    def get_file_url(self, obj, attr):
        file = getattr(obj, attr, None)
        if file and hasattr(file, 'url'):
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(file.url)
            # fallback if request is not available in context
            return urljoin(settings.MEDIA_URL, file.url)
        return None

    def get_muzzle_video(self, obj):
        return self.get_file_url(obj, 'muzzle_video')

    def get_left_side_image(self, obj):
        return self.get_file_url(obj, 'left_side_image')

    def get_right_side_image(self, obj):
        return self.get_file_url(obj, 'right_side_image')

    def get_challan_paper(self, obj):
        return self.get_file_url(obj, 'challan_paper')

    def get_vet_certificate(self, obj):
        return self.get_file_url(obj, 'vet_certificate')

    def get_chairman_certificate(self, obj):
        return self.get_file_url(obj, 'chairman_certificate')

    def get_image_with_owner(self, obj):
        return self.get_file_url(obj, 'image_with_owner')

    class Meta:
        model = Asset
        fields = [
            'id',
            'reference_id',
            'owner_name',
            'breed_name',
            'color_name',
            'age_in_months',
            'weight_kg',
            'height',
            'vaccination_status_name',
            'last_vaccination_date',
            'deworming_status_name',
            'last_deworming_date',
            'health_issues',
            'pregnancy_status',
            'last_date_of_calving',
            'purchase_date',
            'purchase_from',
            'purchase_amount',
            'gender',
            'remarks',
            'created_at',
            'updated_at',
            'is_active',
            'muzzle_video',
            'left_side_image',
            'right_side_image',
            'challan_paper',
            'vet_certificate',
            'chairman_certificate',
            'image_with_owner'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
