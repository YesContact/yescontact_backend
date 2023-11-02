from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser



class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'phone_number', 'is_superuser')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'phone_number', 'is_superuser')