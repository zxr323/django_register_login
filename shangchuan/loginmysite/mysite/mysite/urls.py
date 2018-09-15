from django.contrib import admin
from django.conf.urls import url
from login import views as login_views
from django.conf.urls import include

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', login_views.index,),
    url(r'^login/', login_views.login,),
    url(r'^register/', login_views.register,),
    url(r'^logout/', login_views.logout,),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^confirm/$', login_views.user_confirm,),
]
