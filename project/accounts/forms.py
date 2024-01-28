import code
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone = self.cleaned_data['phone']
        last_user = User.objects.filter(code__isnull=False).order_by('-code').first()
        if last_user:
            user.code = last_user.code + 1
        else:
            user.code = 1100
        if commit:
            user.save()
        return user