from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Zone


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'প্রথম নাম'
    }))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'শেষ নাম'
    }))
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'tel',
        'placeholder': 'মোবাইল নম্বর',
        'pattern': '[0-9+\\-\\s()]*',
        'inputmode': 'tel'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'আপনার ই-মেইল'
    }))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'ইউজারনেম'
    }))
    password1 = forms.CharField(label='পাসওয়ার্ড', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'পাসওয়ার্ড (কমপক্ষে ৮ অক্ষর)',
        'id': 'registerPassword1'
    }))
    password2 = forms.CharField(label='পাসওয়ার্ড নিশ্চিতকরণ', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'পাসওয়ার্ড আবার লিখুন',
        'id': 'registerPassword2'
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('এই ই-মেইল ইতিমধ্যে ব্যবহৃত হয়েছে।')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                role='customer',
                phone=self.cleaned_data.get('phone', '')
            )
        return user


class UserLoginForm(forms.Form):
    identifier = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control mb-3',
        'placeholder': 'Email বা Mobile Number'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control mb-3',
        'placeholder': 'পাসওয়ার্ড',
        'id': 'loginPassword'
    }))


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'প্রথম নাম'
    }))
    last_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'শেষ নাম'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'ই-মেইল'
    }))

    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city', 'avatar')
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ফোন নম্বর'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'ঠিকানা', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'শহর'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CheckoutForm(forms.Form):
    """Checkout form for order placement"""
    full_name = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'আপনার সম্পূর্ণ নাম *'
    }))
    
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'ই-মেইল ঠিকানা *'
    }))
    
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'tel',
        'placeholder': 'ফোন নম্বর (যেমন: 01700000000) *',
        'pattern': '[0-9+\\-\\s()]*',
        'inputmode': 'tel'
    }))
    
    delivery_address = forms.CharField(max_length=500, required=True, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'ডেলিভারি ঠিকানা *',
        'rows': 4
    }))
    
    zone = forms.ModelChoiceField(
        queryset=Zone.objects.filter(is_active=True),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='ডেলিভারি জোন নির্বাচন করুন *'
    )
    
    payment_method = forms.ChoiceField(
        choices=[
            ('cash', 'ক্যাশ অন ডেলিভারি (COD)')
        ],
        required=True,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        }),
        label='পেমেন্ট পদ্ধতি',
        initial='cash'
    )


class AdminRegisterForm(UserCreationForm):
    """Form for creating new admin users"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Admin ই-মেইল'
    }))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Admin ইউজারনেম'
    }))
    password1 = forms.CharField(
        label='পাসওয়ার্ড',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'পাসওয়ার্ড (কমপক্ষে ৮ অক্ষর)'
        })
    )
    password2 = forms.CharField(
        label='পাসওয়ার্ড নিশ্চিতকরণ',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'পাসওয়ার্ড আবার লিখুন'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('এই ইউজারনেম ইতিমধ্যে ব্যবহৃত হয়েছে।')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('এই ই-মেইল ইতিমধ্যে ব্যবহৃত হয়েছে।')
        return email
