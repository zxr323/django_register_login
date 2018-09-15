from django.db import models


# Create your models here.


class User(models.Model):

    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    name = models.CharField(max_length=128, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=256, verbose_name='用户密码')
    email = models.EmailField(unique=True, verbose_name='用户邮箱')
    sex = models.CharField(max_length=32, choices=gender, default='男', verbose_name='用户性别')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='用户创建时间')
    has_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class ConfirmString(models.Model):
    code = models.CharField(max_length=256, verbose_name='注册码')
    user = models.OneToOneField('User', verbose_name='关联的用户')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.user.name + ': '+self.code

    class Meta:
        ordering = ['-created_time']
        verbose_name = '确认码'
        verbose_name_plural = '确认码'
