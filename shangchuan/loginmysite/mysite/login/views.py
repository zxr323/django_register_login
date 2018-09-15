from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
import hashlib
import datetime
from mysite import settings
# Create your views here.


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user)
    return code


def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives
    subject = '来自www.baidu.com的注册确认邮件'

    text_content = '''感谢注册www.baidu.com，这里是百度搜索站点，专注于网络知识的分享搜索和分享！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.baidu.com</a>，\
                    这里是百度搜索站点，专注于网络知识的分享搜索和分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def index(request):
    pass
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('login_in', None):
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请填写所有字段'  # 虽然由于html5帮我们防住了不会显示，但也得做，避免别人跳过浏览器发请求
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = models.User.objects.get(name=username)
                if not user.has_confirmed:
                    message = '用户还未通过邮件确认'
                    return render(request, 'login/login.html', locals())
            except:
                message = '用户不存在'
                return render(request, 'login/login.html', locals())
            if user.password == hash_code(password):
                request.session['login_in'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = '密码错误'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('login_in', None):
        return redirect('/index/')
    if request.method == 'POST':
        message = '请检查填写内容'
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:
                message = '两次密码输入不同，请重新输入'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在，请重新设置'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '邮箱已经被注册，请填写其他邮箱'
                    return render(request, 'login/register.html', locals())
            new_user = models.User()
            new_user.name = username
            new_user.password = hash_code(password1)
            new_user.email = email
            new_user.sex = sex
            new_user.save()

            code = make_confirm_string(new_user)
            send_email(email, code)
            message = '请前往注册邮箱确认'

            return render(request, 'login/confirm.html', locals())

    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session['login_in']:  # 如果不在登录状态
        return redirect('/index/')
    request.session.flush()  # 用户所有会话里的信息将被删除
    return redirect('/index/')


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求'
        return render(request, 'login/confirm.html', locals())

    created_time = confirm.created_time
    now = datetime.datetime.now()
    if now > created_time + datetime.timedelta(days=settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '你的邮件已过期，请重新注册'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())
