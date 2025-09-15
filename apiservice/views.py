import jwt
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from assetservice.models import AssetType, Breed, Color, VaccinationStatus, DewormingStatus
from assetservice.serializers import AssetTypeSerializer, BreedSerializer, ColorSerializer, VaccinationStatusSerializer, \
    DewormingStatusSerializer, AssetSerializer, AssetListSerializer, AssetInsuranceListSerializer, CowSerializer
from insuranceportal.utils import IsSuperUser
from insuranceservice.serializers import AssetInsuranceSerializer, InsuranceClaimSerializer, \
    PaymentInformationSerializer, PaymentInformationDetailSerializer
from livestock_management_system.helper.livestock_management_helper_class import add_aseet_location
from livestock_management_system.helper.model_class import AssetLocationHistoryRequest
from .serializers import *
from .utils import *


class RoleListAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        try:
            return success_response("Roles Retrieved successfully.", data=serializer.data)

        except serializers.ValidationError as e:
            return handle_serializer_error(e)

class RoleListCreateAPIView(APIView):
    permission_classes = [IsSuperUser]
    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return success_response("Roles Created successfully.", data=serializer.data,status_code=status.HTTP_201_CREATED)

            except serializers.ValidationError as e:
                return handle_serializer_error(e)

        return validation_error_from_serializer(serializer)



class RoleRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsSuperUser]

    def get_object(self, pk):
        try:
            return Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return None

    def get(self, request, pk):
        role = self.get_object(pk)
        if role is not None:
            serializer = RoleSerializer(role)
            try:
                return success_response("Roles Retrieved successfully.", data=serializer.data, status_code=status.HTTP_201_CREATED)

            except serializers.ValidationError as e:
                return handle_serializer_error(e)
        return error_response("Role not found", status_code=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        role = self.get_object(pk)
        if role is not None:
            serializer = RoleSerializer(role, data=request.data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    return success_response("Roles Updated successfully.", data=serializer.data,
                                            status_code=status.HTTP_201_CREATED)

                except serializers.ValidationError as e:
                    return handle_serializer_error(e)

            return validation_error_from_serializer(serializer)
        return Response({"detail": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        role = self.get_object(pk)
        if role is not None:
            role.delete()
            return success_response("Roles Updated successfully.",
                                status_code=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Role not found"}, status=status.HTTP_404_NOT_FOUND)



class RegisterStep1(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = Step1Serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                serializer.save()
                return success_response("OTP sent successfully.")

            except serializers.ValidationError as e:
                return handle_serializer_error(e)

        return validation_error_from_serializer(serializer)


class VerifyOTP(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return success_response("OTP verified successfully.")
            except serializers.ValidationError as e:
                return handle_serializer_error(e)

        return validation_error_from_serializer(serializer)


class SetPassword(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return success_response("User registered successfully.")
            except serializers.ValidationError as e:
                return handle_serializer_error(e)

        return validation_error_from_serializer(serializer)


class Login(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                return success_response(
                    "User logged in successfully.",
                    data=serializer.validated_data
                )
            return validation_error_from_serializer(serializer)
        except Exception as e:
            return error_response(
                message=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class SetPersonalInfo(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SetPersonalInfoSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                serializer.save()
                return success_response("User's Personal Info Saved Successfully.")
            except serializers.ValidationError as e:
                return handle_serializer_error(e)

        return validation_error_from_serializer(serializer)

    def get(self, request):
        try:
            personal_info = UserPersonalInfo.objects.get(user=request.user)
            serializer = SetPersonalInfoSerializer(personal_info, context={'request': request})
            return success_response(data=serializer.data)
        except UserPersonalInfo.DoesNotExist:
            return Response({
                "statusCode": "404",
                "statusMessage": "Not Found",
                "data": {
                    "message": "Personal info not found for this user."
                }
            }, status=status.HTTP_404_NOT_FOUND)

class SetOrganizationInfo(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role.id == 1:
            messages = 'Organization info is not needed for this user.'
            return Response({
                "statusCode": "404",
                "statusMessage": "Not Found",
                "data": {
                    "message": f'{messages}'
                }
            }, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = SetOrganizationInfoSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                try:
                    serializer.save()
                    return success_response("User's Organization Info Saved Successfully.")
                except serializers.ValidationError as e:
                    return handle_serializer_error(e)

            return validation_error_from_serializer(serializer)

    def get(self, request):
        try:
            organization_info = OrganizationInfo.objects.get(user=request.user)
            serializer = SetOrganizationInfoSerializer(organization_info, context={'request': request})
            return success_response(data=serializer.data)
        except OrganizationInfo.DoesNotExist:
            messages = 'Organization info not found for this user.'
            if request.user.role.id == 1:
                messages = 'Organization info is not needed for this user.'
            return Response({
                "statusCode": "404",
                "statusMessage": "Not Found",
                "data": {
                    "message": f'{messages}'
                }
            }, status=status.HTTP_404_NOT_FOUND)

class SetFinancialInfo(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SetFinancialInfoSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                serializer.save()
                return success_response("User's Financial Info Saved Successfully.")
            except serializers.ValidationError as e:
                return handle_serializer_error(e)
        return validation_error_from_serializer(serializer)

    def get(self, request):
        try:
            financial_info = UserFinancialInfo.objects.get(user=request.user)
            serializer = SetFinancialInfoSerializer(financial_info)
            return success_response(data=serializer.data)
        except UserFinancialInfo.DoesNotExist:
            return Response({
                "statusCode": "404",
                "statusMessage": "Not Found",
                "data": {
                    "message": "Financial info not found for this user."
                }
            }, status=status.HTTP_404_NOT_FOUND)

class SetNomineeInfo(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.data)
        serializer = SetNomineeInfoSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                serializer.save()
                return success_response("User's Nominee Info Saved Successfully.")
            except serializers.ValidationError as e:
                return handle_serializer_error(e)
            except Exception as e:
                return Response({
                    "statusCode": "500",
                    "statusMessage": "Internal Server Error",
                    "data": {
                        "message": str(e)
                    }
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return validation_error_from_serializer(serializer)

    def get(self, request):
        try:
            nominee_info = UserNomineeInfo.objects.get(user=request.user)
            serializer = SetNomineeInfoSerializer(nominee_info)
            return success_response(data=serializer.data)
        except UserNomineeInfo.DoesNotExist:
            return Response({
                "statusCode": "404",
                "statusMessage": "Not Found",
                "data": {
                    "message": "Nominee info not found for this user."
                }
            }, status=status.HTTP_404_NOT_FOUND)
class VerifyTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({"detail": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
            return Response(payload, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({"detail": "Token expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"detail": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

class SubUsersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_user = request.user

        # Avoid AttributeError if role is None
        if current_user.is_superuser and current_user.role is None:
            return error_response(
                {"detail": "You are a superuser. Use the dedicated API to get all users."},
                status_code=status.HTTP_403_FORBIDDEN
            )

        if not current_user.role or current_user.role.id != 2:
            return error_response(
                {"detail": "You are not authorized to view sub-users."},
                status_code=status.HTTP_403_FORBIDDEN
            )

        sub_users = current_user.sub_users.all()
        serializer = SubUserSerializer(sub_users, many=True)
        return success_response("User List retrieved successfully.", data=serializer.data)

class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can change their password.

    def post(self, request):
        # Get the serializer with request data
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

        # Validate the serializer data
        if serializer.is_valid():
            user = request.user  # Get the currently logged-in user

            # Set the new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()  # Save the user with the updated password

            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class AssetTypeListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        assets = AssetType.objects.all()
        serializer = AssetTypeSerializer(assets, many=True)
        try:
            return success_response("Asset Type List Retrieved successfully", data=serializer.data,
                                    status_code=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return handle_serializer_error(e)

class BreedListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        breeds = Breed.objects.all()
        serializer = BreedSerializer(breeds, many=True)
        return success_response("Breed List Retrieved successfully", data=serializer.data, status_code=status.HTTP_200_OK)

class ColorListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        colors = Color.objects.all()
        serializer = ColorSerializer(colors, many=True)
        return success_response("Color List Retrieved  successfully", data=serializer.data,
                                status_code=status.HTTP_200_OK)

class VaccinationStatusListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        statuses = VaccinationStatus.objects.all()
        serializer = VaccinationStatusSerializer(statuses, many=True)
        return success_response("Vaccination Status List Retrieved successfully", data=serializer.data,
                                status_code=status.HTTP_200_OK)

class DewormingStatusListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        statuses = DewormingStatus.objects.all()
        serializer = DewormingStatusSerializer(statuses, many=True)
        return success_response("Deworming Status List Retrieved successfully", data=serializer.data,
                                status_code=status.HTTP_200_OK)

class AssetListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_superuser:
            assets = Asset.objects.all()
        else:
            assets = Asset.objects.filter(owner=request.user)

        serializer = AssetListSerializer(assets, many=True, context={'request': request})
        try:
            return success_response(
                "Asset List Retrieved successfully",
                data=serializer.data,
                status_code=status.HTTP_200_OK
            )
        except serializers.ValidationError as e:
            return handle_serializer_error(e)

class InsurancelistAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_superuser:
            assets = AssetInsurance.objects.all()
        else:
            assets = AssetInsurance.objects.filter(created_by=request.user)

        serializer = AssetInsuranceListSerializer(assets, many=True, context={'request': request})
        try:
            return success_response(
                "AssetInsurance List Retrieved successfully",
                data=serializer.data,
                status_code=status.HTTP_200_OK
            )
        except serializers.ValidationError as e:
            return handle_serializer_error(e)

class AssetCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AssetSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                #serializer.save()
                asset = serializer.save()

                #Asset Location Entry [By TAG]
                # Separate asset location logic
                self.add_location(asset, request)

                return success_response("Asset Created successfully.", data=serializer.data, status_code=status.HTTP_201_CREATED)
            except serializers.ValidationError as e:
                return handle_serializer_error(e)

        return validation_error_from_serializer(serializer)
    
    def add_location(self, asset, request):
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")

        if latitude and longitude:
            location_data = {
                "asset_id": asset.id,
                "latitude": latitude,
                "longitude": longitude,
                "by_user_id": request.user.id
            }
            response = add_aseet_location(location_data)
            status = response.get("status")

            if status != "success":
                raise serializers.ValidationError({
                    "detail": "Failed to add asset location. Error: " + response.get("error", "Unknown")
                })

class AssetDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Asset, pk=pk)

    def get(self, request, pk):
        try:
            if request.user.is_superuser:
                asset = self.get_object(pk)
            else:
                asset = Asset.objects.get(pk=pk, owner=request.user)

            serializer = AssetSerializer(asset)
            return success_response("Asset Details Retrieved successfully", data=serializer.data)

        except Asset.DoesNotExist:
            return error_response("Asset not found.", status_code=status.HTTP_404_NOT_FOUND)

        except AttributeError as e:
            return error_response(f"Attribute error: {str(e)}", status_code=status.HTTP_404_NOT_FOUND)

        except serializers.ValidationError as e:
            return handle_serializer_error(e)

    def put(self, request, pk):
        try:
            if request.user.is_superuser:
                asset = self.get_object(pk)
            else:
                asset = Asset.objects.get(pk=pk, owner=request.user)
            serializer = AssetSerializer(asset, data=request.data, context={'request': request})
            if serializer.is_valid():
                try:
                    serializer.save()
                    return success_response("Asset Updated successfully", data=serializer.data)
                except serializers.ValidationError as e:
                    return handle_serializer_error(e)
            return validation_error_from_serializer(serializer)
        except Asset.DoesNotExist:
            return error_response("Asset not found.", status_code=status.HTTP_404_NOT_FOUND)

        except AttributeError as e:
            return error_response(f"Attribute error: {str(e)}", status_code=status.HTTP_404_NOT_FOUND)

        except serializers.ValidationError as e:
            return handle_serializer_error(e)

    def delete(self, request, pk):
        try:
            if request.user.is_superuser:
                asset = self.get_object(pk)
            else:
                asset = Asset.objects.get(pk=pk, owner=request.user)
            asset.delete()
            return success_response("Asset Deleted successfully.", status_code=status.HTTP_204_NO_CONTENT)
        except Asset.DoesNotExist:
            return error_response("Asset not found.", status_code=status.HTTP_404_NOT_FOUND)

        except AttributeError as e:
            return error_response(f"Attribute error: {str(e)}", status_code=status.HTTP_404_NOT_FOUND)

        except serializers.ValidationError as e:
            return handle_serializer_error(e)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cow_by_reference(request):
    string_id = request.query_params.get('string_id', None)
    if not string_id:
        return Response({"error": "string_id parameter is required"}, status=400)

    try:
        cow_type = AssetType.objects.get(name__iexact='cow')
        cow = Asset.objects.get(asset_type=cow_type, reference_id__icontains=string_id)
        serializer = CowSerializer(cow, context={'request': request})
        return Response(serializer.data)
    except Asset.DoesNotExist:
        return Response({"error": "Cow not found"}, status=404)
    except AssetType.DoesNotExist:
        return Response({"error": "Cow asset type not found"}, status=404)
class CompanyWiseInsuranceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        companies = InsuranceCompany.objects.all()
        data = []

        for company in companies:
            # Company data
            company_data = {
                "id": company.id,
                "name": company.name,
                "logo": request.build_absolute_uri(company.logo.url) if company.logo else None,
                "insurance_categories": []
            }

            # Fetch all insurance products related to the company
            products = InsuranceProduct.objects.filter(insurance_company=company).select_related(
                'insurance_type', 'insurance_period', 'insurance_category'
            )

            # Group products by insurance category and type
            categories = {}
            for product in products:
                category_id = product.insurance_category.id
                type_id = product.insurance_type.id

                # Initialize the category if not already present
                if category_id not in categories:
                    categories[category_id] = {
                        "id": category_id,
                        "name": product.insurance_category.name,
                        "insurance_types": {}
                    }

                # Initialize the insurance type within the category if not already present
                if type_id not in categories[category_id]["insurance_types"]:
                    categories[category_id]["insurance_types"][type_id] = {
                        "id": type_id,
                        "name": product.insurance_type.name,
                        "periods": []
                    }

                # Prepare period data
                period_data = {
                    "id": product.insurance_period.id,
                    "name": product.insurance_period.name,
                    "premiums": [{
                        "id": product.id,
                        "percentage": product.premium_percentage
                    }]
                }

                # Add period data to the insurance type within the category
                categories[category_id]["insurance_types"][type_id]["periods"].append(period_data)

            # Convert the dictionary of insurance types to a list for each category
            for category in categories.values():
                category["insurance_types"] = list(category["insurance_types"].values())

            # Add categories to the company data
            company_data["insurance_categories"] = list(categories.values())
            data.append(company_data)

        return Response({
            "statusCode": str(status.HTTP_200_OK),
            "statusMessage": "Success",
            "data": data
        }, status=status.HTTP_200_OK)
# class CompanyWiseInsuranceAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request, *args, **kwargs):
#         companies = InsuranceCompany.objects.all()
#         data = []
#
#         for company in companies:
#             company_data = {
#                 "id": company.id,
#                 "name": company.name,
#                 "logo": request.build_absolute_uri(company.logo.url) if company.logo else None,
#                 "insurance_types": [],
#             }
#
#             insurance_types = InsuranceType.objects.filter(category__company=company)
#
#             for insurance_type in insurance_types:
#                 type_data = {
#                     "id": insurance_type.id,
#                     "name": insurance_type.name,
#                     "periods": []
#                 }
#
#                 insurance_periods = InsurancePeriod.objects.filter(
#                     type__category__company=company,
#                 )
#
#                 for period in insurance_periods:
#                     premiums = PremiumPercentage.objects.filter(
#                         insurance_period__type__category__company=company,
#                     )
#
#                     premium_list = []
#                     for premium in premiums:
#                         premium_list.append({
#                             "id": premium.id,
#                             "percentage": premium.percentage
#                         })
#
#                     type_data["periods"].append({
#                         "id": period.id,
#                         "name": period.name,
#                         "premiums": premium_list
#                     })
#
#                 company_data["insurance_types"].append(type_data)
#
#             data.append(company_data)
#
#         return Response({
#             "statusCode": str(status.HTTP_200_OK),
#             "statusMessage": "Success",
#             "data": data
#         }, status=status.HTTP_200_OK)
#

class AssetInsuranceCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        is_many = isinstance(request.data, list)
        serializer = AssetInsuranceSerializer(data=request.data, many=is_many, context={'request': request})

        if serializer.is_valid():
            try:
                serializer.save(created_by=request.user)
                return success_response(
                    "Asset Insurance(s) created successfully.",data=serializer.data,
                    status_code=status.HTTP_201_CREATED
                )
            except serializers.ValidationError as e:
                return handle_serializer_error(e)

        return validation_error_from_serializer(serializer)
class InsuranceClaimCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = InsuranceClaimSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            try:
                # Save the claim with the created_by field
                insurance_claim = serializer.save(created_by=request.user)

                # Handle file uploads for claim documents
                if request.FILES.getlist('claim_documents'):
                    for file in request.FILES.getlist('claim_documents'):
                        document = ClaimDocument.objects.create(
                            asset_insurance=insurance_claim.asset_insurance,
                            file=file,
                            file_name=file.name  # Save the file name
                        )
                        insurance_claim.claim_documents.add(document)

                insurance_claim.save()

                return success_response(
                    message="Asset Insurance Claimed successfully.",
                    data=InsuranceClaimSerializer(insurance_claim,context={'request': request}).data,
                    status_code=status.HTTP_201_CREATED
                )

            except ValidationError as e:
                return Response(
                    {"status": "error", "message": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return Response(
                    {"status": "error", "message": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # Return serializer errors if validation fails
        return validation_error_from_serializer(serializer)


from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def PaymentInformationCreateView(request):
    serializer = PaymentInformationSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Payment information created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentInformationDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        payment = get_object_or_404(PaymentInformation, pk=pk)
        serializer = PaymentInformationDetailSerializer(payment, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentByInsuranceAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, insurance_id):
        payments = PaymentInformation.objects.filter(assetInsuranceId=insurance_id)
        serializer = PaymentInformationDetailSerializer(payments, many=True, context={'request': request})
        return Response(serializer.data)

class ForgotPasswordRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response(serializer.save())
        return Response(serializer.errors, status=400)


class ForgotPasswordVerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordVerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.save())
        return Response(serializer.errors, status=400)


class ForgotPasswordSetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSetNewSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.save())
        return Response(serializer.errors, status=400)
