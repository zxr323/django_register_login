from django import forms
from captcha.fields import CaptchaField


class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='用户密码', max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # 后一项使html中的bootstrp的css起效果
    captcha = CaptchaField(label='验证码')

gender = (
        ('male', '男'),
        ('female', '女'),
    )


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='用户密码', max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='用户密码', max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender, )
    captcha = CaptchaField(label='验证码')