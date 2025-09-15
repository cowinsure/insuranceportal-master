from datetime import datetime, timezone

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Role(TimestampModel):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class TempUser(TimestampModel):
    mobile_number = models.CharField(max_length=15, unique=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    otp = models.CharField(max_length=6)
    otp_request_count = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)


    def __str__(self):
        return self.mobile_number

    class Meta:
        indexes = [
            models.Index(fields=["mobile_number"]),
        ]

class UserManager(BaseUserManager):
    def create_user(self, mobile_number, password=None, **extra_fields):
        if not mobile_number:
            raise ValueError("Users must have a mobile number")
        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", None)
        extra_fields.setdefault("managed_by", None)
        extra_fields.setdefault("onboarded_by", None)
        return self.create_user(mobile_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    mobile_number = models.CharField(max_length=15, unique=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    managed_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sub_users',
        help_text="Must be a user with role_id = 2"
    )

    onboarded_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='onboarded_users',
        help_text="Only staff or superuser can onboard other users"
    )
    parent_enterprise = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='parent_enterprise_user',
        help_text="Only Enterprise user can be assigned"
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_insurecow_agent = models.BooleanField(default=False)
    is_insurance_agent = models.BooleanField(default=False)
    is_enterprise_agent = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    ekyc_status = models.IntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = "mobile_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.mobile_number

    class Meta:
        indexes = [
            models.Index(fields=["mobile_number"]),
        ]

    def clean(self):
        if self.is_superuser:
            return  # Skip validation for superusers

    def calculate_ekyc_status(self):
        """Calculate the eKYC completion status based on user role."""
        # Skip calculation for superusers
        if self.is_superuser:
            self.ekyc_status = 100
            return

        # Determine the required models based on the user role
        related_models = [
            hasattr(self, 'personal_info') and bool(self.personal_info.first_name) and bool(
                self.personal_info.last_name),
            hasattr(self, 'financial_info') and bool(self.financial_info.bank_name) and bool(
                self.financial_info.account_number),
            hasattr(self, 'nominee_info') and bool(self.nominee_info.nominee_name) and bool(self.nominee_info.nid),
        ]

        # If the user role is 2 or 3 (organization or business), include OrganizationInfo
        if self.role_id in [2, 3]:
            related_models.append(
                hasattr(self, 'organization_info') and bool(self.organization_info.name)
            )

        # Calculate the completion percentage
        completed_count = sum(1 for x in related_models if x)  # Count only True values
        total_count = len(related_models)
        self.ekyc_status = int((completed_count / total_count) * 100)

    def save(self, *args, **kwargs):
        self.full_clean()
        self.calculate_ekyc_status()# triggers clean()
        super().save(*args, **kwargs)

class OTPVerification(TimestampModel):
    mobile_number = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"OTP {self.otp_code} verification status: {self.is_verified}"

class LocationCategory(models.TextChoices):
    REGISTRATION = "registration", "Registration"
    PASSWORD_RESET = "password_reset", "Password Reset"
    LOGIN = "login", "Login"

class UserLocation(TimestampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=LocationCategory.choices)
    lat = models.FloatField()
    long = models.FloatField()

    def __str__(self):
        return f"{self.user.mobile_number} - {self.category} Location"

class UserPersonalInfo(TimestampModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="personal_info")
    profile_image = models.ImageField(null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    nid = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    nid_front = models.ImageField(null=True, blank=True)
    nid_back = models.ImageField(null=True, blank=True)
    update_count = models.PositiveIntegerField(default=0)
    thana = models.CharField(max_length=255)
    union = models.CharField(max_length=255)
    village = models.CharField(max_length=255)
    zilla = models.CharField(max_length=255)
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)

    tin = models.CharField("TIN", max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.mobile_number}"

class OrganizationInfo(TimestampModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="organization_info")
    logo = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=255)
    established = models.DateField(null=True, blank=True)
    tin = models.CharField("TIN", max_length=50, null=True, blank=True)
    bin = models.CharField("BIN", max_length=50, null=True, blank=True)
    update_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Profile of {self.user.mobile_number}"

class UserFinancialInfo(TimestampModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="financial_info")
    bank_name = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    update_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Financial Info for {self.user.mobile_number}"

class UserNomineeInfo(TimestampModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="nominee_info")
    nominee_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    nid = models.CharField(max_length=50)
    relationship = models.CharField(max_length=50)
    update_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Nominee Info for {self.user.mobile_number}"


from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError

User = get_user_model()

class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="token")
    access_token = models.TextField(blank=True, null=True)
    refresh_token = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_token_valid(self):
        """
        Check if the access token is valid and not expired.
        """
        try:
            token = AccessToken(self.access_token)

            # Check if the token has expired
            if datetime.fromtimestamp(token['exp'], timezone.utc) > datetime.now(timezone.utc):
                return True
            return False
        except TokenError:
            return False

    def generate_tokens(self, force=False):
        """
        Generate a new pair of access and refresh tokens.
        """


        if force or not self.access_token or not self.refresh_token or not self.is_token_valid():
            try:
                refresh = RefreshToken.for_user(self.user)
                self.access_token = str(refresh.access_token)
                self.refresh_token = str(refresh)
                self.save()
                print(f"Tokens successfully generated for {self.user.mobile_number}")
            except Exception as e:
                print(f"Error generating tokens for {self.user.mobile_number}: {e}")

    def __str__(self):
        return f"Token for {self.user.mobile_number}"


@receiver(post_save, sender=User)
def create_user_token(sender, instance, created, **kwargs):
    """
    Signal to create or update tokens when a User instance is created.
    """
    if created:
        token, token_created = Token.objects.get_or_create(user=instance)
        if token_created or not token.access_token or not token.refresh_token or not token.is_token_valid():
            token.generate_tokens()
            print(f"Tokens generated for {instance.mobile_number}")
