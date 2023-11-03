from django.contrib.auth.forms import UserChangeForm
from users.models import CustomUser


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", "full_name", "phone_number", "is_superuser")
