"""tabditor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from tb_UI import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^(?P<dj_param01>\d+)$', views.func01, name='func01'),
    url(r'(?P<djvar_02>^\w+$)', views.func02, name='func02'),
    url(r'^rhyme/(?P<djvar_03>.+$)', views.func_rhyme, name='func_rhyme'),
    url(r'^rhyme/(?P<djvar_04>.+$)', views.func_rhyme, name='func_rhyme'),
]
