from django import forms
from django.contrib.auth.models import User
from .models import Profile

class SignUpForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if Profile.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Phone number already exists. Please use a different one.")
        return phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            # ❌ REMOVE THIS: Profile.objects.create(user=user, phone_number=self.cleaned_data["phone_number"])
        return user
